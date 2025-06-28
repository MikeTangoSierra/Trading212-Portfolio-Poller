from functions.logging import *
import os
import requests
import time

# Setup logging.
configure_logging('get_data_functions.log')

# Set our required API Access Info.
API_TOKEN = os.environ['T212_API_TOKEN']
BASE_API_PATH = os.environ['T212_BASE_API_PATH']
EQUITY_BASE_API_PATH = "equity/"
AUTH_HEADER = {"Authorization": str(API_TOKEN)}


# Get account equity info.
def get_account_equity_info():
    try:
        equity_cash_api_endpoint = BASE_API_PATH + EQUITY_BASE_API_PATH + "account/cash"
        account_equity_call = requests.get(equity_cash_api_endpoint, headers=AUTH_HEADER)
        account_equity_call_json = account_equity_call.json()

        while account_equity_call.status_code != 200 or account_equity_call_json.contains(None):
            time.sleep(10)
            account_equity_call = requests.get(equity_cash_api_endpoint, headers=AUTH_HEADER)
            account_equity_call_json = account_equity_call.json()

        return account_equity_call_json
    except:
        logging.error("ERROR:" + " " + "Failed to get account equity info")


# Get account base currency.
def get_account_base_currency():
    try:
        equity_info_api_endpoint = BASE_API_PATH + EQUITY_BASE_API_PATH + "account/info"
        account_info_call = requests.get(equity_info_api_endpoint, headers=AUTH_HEADER)
        account_info_data_json = account_info_call.json()
        account_currency = account_info_data_json.get('currencyCode')

        while account_info_call.status_code != 200 or account_currency == None:
            time.sleep(10)
            account_info_call = requests.get(equity_info_api_endpoint, headers=AUTH_HEADER)
            account_info_data_json = account_info_call.json()
            account_currency = account_info_data_json.get('currencyCode')

        return account_currency
    except:
        logging.error("ERROR:" + " " + "Failed to get account base currency")


# Get portfolio positions.
def get_portfolio_positions():
    try:
        portfolio_api_endpoint = BASE_API_PATH + EQUITY_BASE_API_PATH + "portfolio"
        portfolio_call = requests.get(portfolio_api_endpoint, headers=AUTH_HEADER)
        portfolio_data_json = portfolio_call.json()

        while portfolio_call.status_code != 200 or portfolio_data_json.contains(None):
            portfolio_call = requests.get(portfolio_api_endpoint, headers=AUTH_HEADER)
            portfolio_data_json = portfolio_call.json()

        return portfolio_data_json
    except:
        logging.error("ERROR:" + " " + "Failed to get portfolio positions")
