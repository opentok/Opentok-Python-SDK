import OpenTokSDK

api_key = '5875231' # Replace with your OpenTok API key.
api_secret = '8f5cde4ade6b11ea22cfd73ea345c64b4e423d29'  # Replace with your OpenTok API secret.
session_address = '192.0.43.10' # Replace with the representative URL of your session.

opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret, staging=True)
session = opentok_sdk.create_session(session_address)

print session.session_id

connectionMetadata = 'username=Bob, userLevel=4'
token = opentok_sdk.generate_token(session.session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, connectionMetadata)

print token
