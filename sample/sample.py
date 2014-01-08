import json
import time
import datetime
import OpenTokSDK

api_key = 'xxx' # Replace with your OpenTok API key.
api_secret = 'yyy'  # Replace with your OpenTok API secret.

opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)
session = opentok_sdk.create_session()

print session.session_id

connectionMetadata = 'username=Bob, userLevel=4'
token = opentok_sdk.generate_token(session.session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, connectionMetadata)

print token

'''
#Archiving sample, make sure you have a client connected to the session before start recording

session_id = session.session_id

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None

print "ALL ARCHIVES"
archives = opentok_sdk.get_archives(1, 2)
for archive in archives:
	print json.dumps(archive.json(), default=dthandler)

archive = opentok_sdk.start_archive(session_id, name="ndsfkls")

archive.stop()

while True:
	archive = opentok_sdk.get_archive(archive.id)
	if archive.status != "available":
		time.sleep(1)
	else:
		break

print "ARCHIVE AVAILABLE"
print json.dumps(archive.json(), default=dthandler)

archive.delete()
'''
