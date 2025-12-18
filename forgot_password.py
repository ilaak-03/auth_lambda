import os
from cognito_utils import cognito, get_secret_hash

def handle_forgot_password(email):
    try:
        cognito.forgot_password(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email
        )

        return {
            "message": "Password reset code sent to registered email"
        }

    except Exception as e:
        return {"error": str(e)}
