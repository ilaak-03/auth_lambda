import os
from cognito_utils import cognito, get_secret_hash

def handle_reset_password(email, code, new_password):
    try:
        cognito.confirm_forgot_password(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email,
            ConfirmationCode=code,
            Password=new_password
        )

        return {
            "message": "Password reset successful"
        }

    except Exception as e:
        return {"error": str(e)}
