from fastapi import Request, HTTPException
from jose import jwt
import requests

SUPABASE_URL = "https://zizfygdqcfcxhonawffk.supabase.co"

JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"

# Fetch JWKS once (can cache later)
jwks = requests.get(JWKS_URL).json()


def get_user_id_from_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        token = auth_header.split(" ")[1]

        payload = jwt.decode(
            token,
            jwks,
            algorithms=["ES256"],   # ✅ FIXED
            options={"verify_aud": False}
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except Exception as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired token")