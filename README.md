# aws-authentication
Scripts to automate authentication on aws and generate config files for aws enumeration tools.

## authorize_device.py
This scripts uses the `boto3` python lib to register a device to allow access to AWS account with `register_client` method.

It will provide the authorization link, that the user has to open in a browser to perform the authentication, and select _Allow_, to finish authorizing the device.

```text 
[+] Authorize device at https://device.sso.eu-west-1.amazonaws.com/?user_code=<code>
```
After providing this link, the script will continuasly poll the API with `create_token` to check if web browser authentication was performed.

Once the user Allows the device, the script will provide the _accessToken_ to be used in other scripts, such as `get_accounts.py`

```text
[+] Login Successfull, use this token <accessToken>
```

### Usage
Arguments:
* `--silent | -s` - Don't print debugging information.
* `--start-url` - AWS authentication start url.
* `--region` - AWS region to create a session for.

```bash
python3 authorized_device.py --region 'us-south-2' --start-url 'https://eu-west-1.console.aws.amazon.com/start#/' --silent
```

## get_accounts.py
This script uses the output (_accessToken_) from `authorize_device.py` to get information on all AWS accounts, and their respective access keys to use in other tools.

### Usage
Arguments:

* `--accessToken` - Access token to access AWS.
* `--silent | -s` - Don't print debugging information.
* `--template'` - Template to create configuration file.
* `--start-url` - AWS authentication start url.
* `--region` - AWS region to create a session for.

```bash
python3 get_accounts.py --region 'us-south-2' --start-url 'https://eu-west-1.console.aws.amazon.com/start#/' --silent --accessToken '<accessToken>' --template template_cloudlist.txt
```

### Templates
This script takes a `--template` as in put to output the required information to use in other tools such as the example for [cloudlist](https://github.com/projectdiscovery/cloudlist). The templates can have the following variables:
* accountId
* accessKeyId
* secretAccessKey
* sessionToken

The names are self explanatory, and the script will replace the variables with the proper information, and replicate the template entry for all accounts it can retrieve.