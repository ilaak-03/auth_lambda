import json

from signup import handle_signup
from login import handle_login
from forgot_password import handle_forgot_password
from reset_password import handle_reset_password


# ---------------- RESPONSE HELPER ----------------

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


# ---------------- LAMBDA HANDLER ----------------

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if not body:  # None or empty
            body = "{}"
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                return response(400, {"message": "Invalid JSON in body"})

        action = body.get("action")
        email = body.get("email")

        if not action or not email:
            return response(400, {"message": "action and email required"})

        # -------- SIGNUP --------
        if action == "signup":
            password = body.get("password")
            if not password:
                return response(400, {"message": "password required"})
            return response(201, handle_signup(email, password))

        # -------- LOGIN --------
        if action == "login":
            password = body.get("password")
            if not password:
                return response(400, {"message": "password required"})
            return response(200, handle_login(email, password))

        # -------- FORGOT PASSWORD --------
        if action == "forgot_password":
            return response(200, handle_forgot_password(email))

        # -------- RESET PASSWORD --------
        if action == "reset_password":
            new_password = body.get("new_password")
            if not new_password:
                return response(400, {"message": "new_password required"})
            return response(200, handle_reset_password(email, new_password))

        # Invalid action
        return response(400, {"message": "Invalid action"})

    except Exception as e:
        return response(500, {"message": str(e)})
