from boto3.session import Session
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add the arguments
parser.add_argument('--accessToken', dest="access_token", required=True, help="Access token to access AWS.")
parser.add_argument('--silent', '-s', action='store_true', dest="silent", help="Don't print debugging info")
parser.add_argument('--template', dest="template", default=None, help="Template to create configuration file.")
parser.add_argument('--start-url', dest="start_url", required=True, help="AWS authentication start url")
parser.add_argument('--region', dest="region", required=True, help="AWS region to create a session")

# Parse the command-line arguments
args = parser.parse_args()

start_url = args.start_url
region = args.region
access_token = args.access_token

# Get all accounts
session = Session(region_name=region)
sso = session.client('sso')
account_roles = sso.list_accounts(
    accessToken=access_token,
)

if not args.silent:
        print(f"[+] {account_roles}")

template = None
if args.template:
        with open(args.template, "r") as f:
                template = ''.join(f.readlines())

for account_role in account_roles['accountList']:
        account_id = account_role['accountId']
        account_name = account_role['accountName']

        if not args.silent:
                print(f"[+] Getting info for {account_name} ({account_id})")

        try:
                role_response = sso.get_role_credentials(
                        roleName='Infosec-VTC',
                        accountId=account_id,
                        accessToken=access_token,
                )
                
        except:
                if not args.silent:
                        print(f"[-] Unable to fetch for {account_id}")
                continue
        
        if not args.silent:
                print(f"[+] {role_response}")

        # Print the access key, secret access key, and session token
        if not args.template:
                print(f"Account ID: {account_id}")
                print(f"Access Key: {role_response['roleCredentials']['accessKeyId']}")
                print(f"Secret Access Key: {role_response['roleCredentials']['secretAccessKey']}")
                print(f"Session Token: {role_response['roleCredentials']['sessionToken']}")
        else:
                accountId = account_id
                accessKeyId = role_response['roleCredentials']['accessKeyId']
                secretAccessKey = role_response['roleCredentials']['secretAccessKey']
                sessionToken = role_response['roleCredentials']['sessionToken']
                line = template.format(sessionToken=sessionToken,accountId=accountId,accessKeyId=accessKeyId,secretAccessKey=secretAccessKey)
                print(line)