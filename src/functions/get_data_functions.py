import requests

base_api_path = "https://demo.trading212.com/api/v0/"
equity_base_api_path = "/equity/"
auth_header = {"Authorization": "<YOUR_API_TOKEN>"}

# Get account equity info
def get_account_equity_info():
  equity_cash_api_endpoint = base_api_path + equity_base_api_path + "account/cash"
  account_equity_call = requests.get(equity_cash_api_endpoint, headers=auth_header)
  account_equity_call_json = account_equity_call.json()
  return(account_equity_call_json)

# Get account base currency
def get_account_base_currency():
  equity_info_api_endpoint = base_api_path + equity_base_api_path + "account/info"
  account_info_call = requests.get(equity_info_api_endpoint, headers=auth_header)
  account_info_data_json = account_info_call.json()
  account_currency = account_info_data_json.get('currencyCode')
  return(account_currency)

# Get portfolio positions
def get_portfolio_positions():
  portfolio_api_endpoint = base_api_path + equity_base_api_path + "portfolio"
  portfolio_call = requests.get(portfolio_api_endpoint, headers=auth_header)
  portfolio_data_json = portfolio_call.json()
  return(portfolio_data_json)