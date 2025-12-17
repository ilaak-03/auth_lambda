import os
from cognito_utils import cognito, get_secret_hash
from db import get_db_connection

def handle_signup(email, password):
    # Cognito sign up
    resp = cognito.sign_up(
        ClientId=os.environ["COGNITO_CLIENT_ID"],
        SecretHash=get_secret_hash(email),
        Username=email,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": email}
        ]
    )

    # Auto confirm user
    cognito.admin_confirm_sign_up(
        UserPoolId=os.environ["COGNITO_USER_POOL_ID"],
        Username=email
    )

    # Store metadata in Neon DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO data (cognito_sub, email) VALUES (%s, %s)",
        (resp["UserSub"], email)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "User created successfully"}
