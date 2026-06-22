from flask import jwt
import datetime
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "MON_SECRET_KEY_SUPER_SECURISE"


def generate_token(user):

    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() +
               datetime.timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except Exception as e:
        print("Erreur JWT :", e)
        return None
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token manquant"}), 401

        payload = verify_token(token)

        if not payload:
            return jsonify({"message": "Token invalide"}), 401

        return f(payload, *args, **kwargs)

    return decorated