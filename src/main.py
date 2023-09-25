from functions.get_data_functions import *
from functions.time_functions import *

# Call functions from get_data_functions to get portfolio value and currency, add their outputs and print them
def final_portfolio_value():
    portfolio_amount_string = str(get_account_equity())
    portfolio_currency_string = str(get_account_base_currency())
    print(portfolio_amount_string + " " + portfolio_currency_string)

# Whilst the market is open (Between 9AM and 9PM BST/GMT (US/GB Market opening times roughly), print portfolio amount and currency, every 15 seconds
is_market_open = time_in_range(start, end, current)

while is_market_open:
    final_portfolio_value()
    sleep_function(seconds=15)
else:
    print("Both UK and US Markets closed! Account value will only change during opening hours (If any trades are open)")
    final_portfolio_value()
    sleep_function(seconds=15)