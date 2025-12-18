import os
from botocore.exceptions import ClientError
from cognito_utils import cognito, get_secret_hash

def handle_login(email, password):
    try:
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

    except ClientError as e:
        # Handles:
        # - UserNotConfirmedException
        # - NotAuthorizedException
        # - UserNotFoundException
        return {"error": e.response["Error"]["Message"]}

    except Exception as e:
        return {"error": str(e)}
