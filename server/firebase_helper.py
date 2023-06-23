import firebase_admin
from firebase_admin import (credentials, auth)


cred = credentials.Certificate('./keys/block_research_key.json')
firebase_app = firebase_admin.initialize_app(cred)


uid_cache = {}


def authenticate_id_token(id_token: str):
    try:
        # Verify the ID token while checking if the token is revoked by
        # passing check_revoked=True.
        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        # Token is valid and not revoked.
        uid_cache[decoded_token['uid']] = decoded_token
        return decoded_token
    except auth.RevokedIdTokenError:
        # Token revoked, inform the user to reauthenticate or signOut().
        pass
    except auth.UserDisabledError:
        # Token belongs to a disabled user record.
        pass
    except auth.InvalidIdTokenError:
        # Token is invalid
        pass






