from time import time, sleep
import webbrowser
from boto3.session import Session

import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add the arguments
parser.add_argument('--silent', '-s', action='store_true', dest="silent", help="Don't print debugging info")
parser.add_argument('--start-url', dest="start_url", help="AWS authentication start url")
parser.add_argument('--region', dest="region", help="AWS region to create a session")

# Parse the command-line arguments
args = parser.parse_args()

start_url = args.start_url
region = args.region

session = Session(region_name=region)
sso_oidc = session.client('sso-oidc')

client_creds = sso_oidc.register_client(
	clientName='myapp',
	clientType='public',
)

if not args.silent:
	print(f"[+] Retrieved Client Credentials")

device_authorization = sso_oidc.start_device_authorization(
	clientId=client_creds['clientId'],
	clientSecret=client_creds['clientSecret'],
	startUrl=start_url,
)

if not args.silent:
	print(f"[+] Retrieved Device authorization")

url = device_authorization['verificationUriComplete']
device_code = device_authorization['deviceCode']
expires_in = device_authorization['expiresIn']
interval = device_authorization['interval']

print(f"[+] Authorize device at {url}")

for n in range(1, expires_in // interval + 1):
	sleep(interval)
	try:
		token = sso_oidc.create_token(
			grantType='urn:ietf:params:oauth:grant-type:device_code',
			deviceCode=device_code,
			clientId=client_creds['clientId'],
			clientSecret=client_creds['clientSecret'],
		)
		break
	except sso_oidc.exceptions.AuthorizationPendingException:
		pass

access_token = token['accessToken']
print(f"[+] Login Successfull, use this token {access_token}")