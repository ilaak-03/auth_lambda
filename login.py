import os
from cognito_utils import cognito, get_secret_hash

def handle_login(email, password):
    resp = cognito.initiate_auth(
        ClientId=os.environ["COGNITO_CLIENT_ID"],
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password,
            "SECRET_HASH": get_secret_hash(email)
        }
    )

    return {
        "message": "Login successful",
        "id_token": resp["AuthenticationResult"]["IdToken"],
        "access_token": resp["AuthenticationResult"]["AccessToken"],
        "refresh_token": resp["AuthenticationResult"]["RefreshToken"]
    }
