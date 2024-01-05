import requests
import os

# Set our required API Access Info
API_TOKEN = os.environ['T212_API_TOKEN']
BASE_API_PATH = os.environ['T212_BASE_API_PATH']
EQUITY_BASE_API_PATH = "/equity/"
AUTH_HEADER = {"Authorization": str(API_TOKEN)}

# Get account equity info
def get_account_equity():
  equity_cash_api_endpoint = BASE_API_PATH + EQUITY_BASE_API_PATH + "account/cash"
  account_equity_call = requests.get(equity_cash_api_endpoint, headers=AUTH_HEADER)
  account_equity_call_json = account_equity_call.json()
  account_equity = account_equity_call_json.get('total')
  return(account_equity)

# Get account base currency
def get_account_base_currency():
  equity_info_api_endpoint = BASE_API_PATH + EQUITY_BASE_API_PATH + "account/info"
  account_info_call = requests.get(equity_info_api_endpoint, headers=AUTH_HEADER)
  account_info_data_json = account_info_call.json()
  account_currency = account_info_data_json.get('currencyCode')
  return(account_currency)

# Get portfolio positions
def get_portfolio_positions():
  portfolio_api_endpoint = BASE_API_PATH + EQUITY_BASE_API_PATH + "portfolio"
  portfolio_call = requests.get(portfolio_api_endpoint, headers=AUTH_HEADER)
  portfolio_data_json = portfolio_call.json()
  return(portfolio_data_json)