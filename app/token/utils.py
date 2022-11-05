import os
import jwt
from fastapi import HTTPException
from app.token.config import JWT_ALGORITHM, JWT_SECRET, DOMAIN, API_AUDIENCE, ISSUER, ALGORITHMS, CLIENT_SECRET, CLIENT_ID

def set_up():

    config = {
    "DOMAIN": os.getenv("DOMAIN", DOMAIN),
    "API_AUDIENCE": os.getenv("API_AUDIENCE", API_AUDIENCE),
    "ISSUER": os.getenv("ISSUER", ISSUER),
    "ALGORITHMS": os.getenv("ALGORITHMS", ALGORITHMS),
    "CLIENT_ID": os.getenv("CLIENT_ID", CLIENT_ID),
    "CLIENT_SECRET": os.getenv("CLIENT_SECRET", CLIENT_SECRET),

    "JWT_ALGORITHM": os.getenv("MY_ALGORITHMS", JWT_ALGORITHM),
    "JWT_SECRET": os.getenv("SECRET", JWT_SECRET),
    }
    return config


class VerifyToken():

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes
        self.config = set_up()

        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify_auth0(self):

        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError:
            raise HTTPException(status_code=400, detail="error auth0 jwt")
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=400, detail="error decode auth0 jwt")

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception:
            raise HTTPException(status_code=400, detail="error auth0 jwt")

        if self.scopes:
            result = self._check_claims(payload, 'scope', str, self.scopes.split(' '))
            if result.get("error"):
                return result

        if self.permissions:
            result = self._check_claims(payload, 'permissions', list, self.permissions)
            if result.get("error"):
                return result

        return payload

    def _check_claims(self, payload, claim_name, claim_type, expected_value):

        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            result["status"] = "error"
            result["status_code"] = 400

            result["code"] = f"missing_{claim_name}"
            result["msg"] = f"No claim '{claim_name}' found in token."
            return result

        if claim_name == 'scope':
            payload_claim = payload[claim_name].split(' ')

        for value in expected_value:
            if value not in payload_claim:
                result["status"] = "error"
                result["status_code"] = 403

                result["code"] = f"insufficient_{claim_name}"
                result["msg"] = (f"Insufficient {claim_name} ({value}). You don't have "
                                 "access to this resource")
                return result
        return result

    def verify_my(self):
        try:
            payload = jwt.decode(
                self.token,
                JWT_SECRET,
                algorithms=JWT_ALGORITHM,
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
        return payload
