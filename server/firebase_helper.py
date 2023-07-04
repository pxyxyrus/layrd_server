import firebase_admin
from firebase_admin import (credentials, auth)
import json


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
    except (auth.RevokedIdTokenError, auth.InvalidIdTokenError) as e:
        # Token revoked, inform the user to reauthenticate or signOut().
        raise Exception({'error_code': 'reauthenticate',  'error_message': e.default_message}) from None
    except (auth.UserDisabledError) as e:
        raise Exception({'error_code': 'user_disabled', 'error_message': e.default_message}) from None
    except Exception as e:
        # TODO logging needed, including stacktrace
        raise Exception({
                'error_code': 'reauthenticate',
                'error_message': "internal_error" if hasattr(e, "default_message") else getattr(e, "default_message")
            }) from None

        





