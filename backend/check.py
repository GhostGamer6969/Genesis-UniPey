from stellar_sdk import Server
from stellar_sdk.exceptions import NotFoundError

# Initialize the server
server = Server("https://horizon-testnet.stellar.org")  # Use testnet for testing

def check_account_exists(public_key):
    try:
        # Load account details from Horizon server
        account = server.load_account(public_key)
        return True, account
    except NotFoundError:
        return False, None

# Example usage
public_key = "GBLL3CNU7AZK5ZOISBDEPRD74XUT6YTNRY6JNTCWIIZJRR6WCQJNNNTQ"
exists, account_details = check_account_exists(public_key)

if exists:
    print("Account exists!")
    print("Account details:", account_details)
else:
    print("Account does not exist.")
