import os
import hmac
import hashlib
import base64
import boto3

cognito = boto3.client("cognito-idp")

def get_secret_hash(username):
    msg = username + os.environ["COGNITO_CLIENT_ID"]
    key = os.environ["COGNITO_CLIENT_SECRET"]
    dig = hmac.new(
        key.encode("utf-8"),
        msg.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()
