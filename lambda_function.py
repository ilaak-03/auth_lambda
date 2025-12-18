import json
from signup import (
    handle_signup,
    handle_confirm_signup
)
from login import handle_login
from forgot_password import handle_forgot_password
from reset_password import handle_reset_password


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    try:
        path = event.get("resource") or event.get("path") or ""
        body = json.loads(event.get("body") or "{}")

        email = body.get("email")
        password = body.get("password")
        code = body.get("code")
        new_password = body.get("new_password")

        # -------- ROUTING --------
        if "/signup" in path:
            result = handle_signup(email, password)

        elif "/confirm-signup" in path:
            result = handle_confirm_signup(email, code)

        elif "/login" in path:
            result = handle_login(email, password)

        elif "/forgot-password" in path:
            result = handle_forgot_password(email)

        elif "/reset-password" in path:
            result = handle_reset_password(
                email,
                body.get("code"),
                body.get("new_password"))

        else:
            return response(404, {"message": "Invalid API path"})

        # -------- COMMON RESPONSE --------
        if "error" in result:
            return response(400, result)

        return response(200, result)

    except Exception as e:
        # Any missing fields, invalid JSON, or runtime errors end up here
        return response(500, {"message": str(e)})
