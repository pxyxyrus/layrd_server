import firebase_admin
from firebase_admin import (auth, credentials)

cred = credentials.Certificate('./keys/block_research_key.json')
firebase_app = firebase_admin.initialize_app(cred)


decoded_token = auth.verify_id_token(id_token)
uid = decoded_token['uid']
print(decoded_token)


# print(user.custom_claims)
# print(user.disabled)
# print(user.display_name)
# print(user.email)
# print(user.email_verified)
# print(user.phone_number)
# print(user.photo_url)
# print(user.provider_data)
# print(user.provider_id)
# print(user.tenant_id)
# print(user.tokens_valid_after_timestamp)
# print(user.uid)
# print(user.user_metadata)
