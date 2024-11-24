from bson import json_util
from functions.get_data_functions import *
from functions.logging import *
from functions.time_functions import *
import json

# Logging config - This needs some work.
configure_logging('transform_data_functions.log')


# Call functions from get_data_functions to get portfolio equity (overall).
def overall_portfolio_value():
    portfolio_overall_equity = str(get_account_equity_info()['total'])
    return portfolio_overall_equity


# Call functions from get_data_function to get portfolio profit and loss (overall).
def overall_profit_loss():
    portfolio_profit_loss = str(get_account_equity_info()['ppl'])
    return portfolio_profit_loss


# Transform BSON data into JSON.
def bson_to_json(bson_data):
    return json.loads(json_util.dumps(bson_data))
