import os
from cognito_utils import cognito

def handle_reset_password(email, new_password):
    cognito.admin_set_user_password(
        UserPoolId=os.environ["COGNITO_USER_POOL_ID"],
        Username=email,
        Password=new_password,
        Permanent=True
    )

    return {
        "message": "Password reset successfully "
    }
