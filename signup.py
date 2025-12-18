import os
import boto3
from cognito_utils import get_secret_hash
from db import get_db_connection

# Cognito client
cognito = boto3.client("cognito-idp", region_name=os.environ.get("AWS_REGION", "ap-south-1"))

def handle_signup(email, password):
    conn = None
    cursor = None
    try:
        # ---- Cognito signup ----
        resp = cognito.sign_up(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}]
        )

        # ---- Store user metadata in DB ----
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO data (cognito_sub, email) VALUES (%s, %s)",
            (resp["UserSub"], email)
        )
        conn.commit()

        return {"message": "Signup successful. Please verify your email to continue."}

    except Exception as e:
        # Generalized Cognito / DB exception
        if conn:
            conn.rollback()
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def handle_confirm_signup(email, code):
    try:
        cognito.confirm_sign_up(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email,
            ConfirmationCode=code
        )
        return {"message": "Email confirmed successfully"}

    except Exception as e:
        # Generalized exception for any Cognito error
        return {"error": str(e)}
