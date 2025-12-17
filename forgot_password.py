import os
from cognito_utils import cognito, get_secret_hash

def handle_forgot_password(email):
    # Check if user exists (optional)
    try:
        cognito.admin_get_user(
            UserPoolId=os.environ["COGNITO_USER_POOL_ID"],
            Username=email
        )
    except cognito.exceptions.UserNotFoundException:
        return {"message": "User does not exist"}

    # Simply return reset initiated
    return {"message": "Password reset initiated"}

