# A LOCAL STAND-IN for Google's sign-in, for the lesson only.
import secrets
import time
from urllib.parse import urlencode

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse

app = FastAPI(title="local stand-in for Google")
PRIVATE = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PUBLIC_PEM = PRIVATE.public_key().public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo,
).decode()
CLIENT_ID = "allcs-demo-client"
CLIENT_SECRET = "standin-client-secret-not-real"
CODES = {}


@app.get("/authorize")
def authorize(client_id: str, redirect_uri: str, state: str,
              scope: str = "", response_type: str = "code"):
    if client_id != CLIENT_ID:
        raise HTTPException(400, "unknown client")
    code = secrets.token_urlsafe(12)
    CODES[code] = "priya@example.com"   # the person "clicked Allow"
    query = urlencode({"code": code, "state": state})
    return RedirectResponse(f"{redirect_uri}?{query}")


@app.post("/token")
def token(code: str = Form(), client_id: str = Form(),
          client_secret: str = Form(), grant_type: str = Form(),
          redirect_uri: str = Form()):
    if client_secret != CLIENT_SECRET or code not in CODES:
        raise HTTPException(400, "invalid_grant")
    email = CODES.pop(code)
    now = int(time.time())
    claims = {
        "iss": "http://localhost:8272", "aud": client_id,
        "sub": "standin-1234", "email": email,
        "iat": now, "exp": now + 300,
    }
    id_token = jwt.encode(claims, PRIVATE, algorithm="RS256")
    return {"id_token": id_token, "token_type": "Bearer"}


@app.get("/public-key", response_class=PlainTextResponse)
def public_key():
    return PUBLIC_PEM
