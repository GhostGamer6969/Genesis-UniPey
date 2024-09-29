from stellar_sdk import Keypair, Server, Network, TransactionBuilder, Asset
from stellar_sdk.exceptions import NotFoundError, BadRequestError
import requests

server = Server("https://horizon.stellar.org")
network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE  # Use Network.TESTNET_NETWORK_PASSPHRASE for testnet

def create_wallet():
    """Creates a new Stellar wallet"""
    keypair = Keypair.random()
    return {
        "public_key": keypair.public_key,
        "secret_key": keypair.secret
    }

def get_balance(public_key):
    """Fetches the balance of a Stellar wallet"""
    try:
        account = server.load_account(public_key)
        balances = {balance['asset_code']: balance['balance'] for balance in account.balances}
        return balances
    except NotFoundError:
        return None

def create_transaction(source_secret, destination_public, amount, asset_code='USDC'):
    """Creates a Stellar transaction"""
    source_keypair = Keypair.from_secret(source_secret)
    source_account = server.load_account(source_keypair.public_key)
    asset = Asset(asset_code, 'GABSHOJIHL7Q...')  # Replace with USDC issuer account ID

    transaction = TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100
    ).append_payment_op(
        destination=destination_public,
        amount=str(amount),
        asset=asset
    ).set_timeout(30).build()

    transaction.sign(source_keypair)
    return transaction

def submit_transaction(transaction):
    try:
        response = server.submit_transaction(transaction)
        return response
    except (BadRequestError, NotFoundError) as e:
        print(f"Transaction failed: {e}")
        return None

def get_conversion_rate():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USDC")
    data = response.json()
    return data["rates"]["USD"]

def convert_to_usd(balances):
    usd_rate = get_conversion_rate()
    usd_equivalent = {asset: float(balance) * usd_rate for asset, balance in balances.items()}
    return usd_equivalent
