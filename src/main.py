import threading
import subprocess
from flask import Flask
from functions.database_functions import *
from functions.get_data_functions import *
from functions.logging import configure_logging
from functions.time_functions import *
from functions.transform_data_functions import *

# Configure logging
configure_logging('main_application.log')

# Initialize Flask app
app = Flask(__name__)
app.config["DEBUG"] = True

# Constants
open_portfolio_positions_databases = ["open_portfolio_positions"]
open_portfolio_positions_collections = [
    "open_portfolio_positions",
    "open_portfolio_positions_weekly",
    "open_portfolio_positions_monthly",
    "open_portfolio_positions_quarterly",
    "open_portfolio_positions_yearly"
]

# Background thread for periodic database updates
def update_database_periodically():
    while True:
        if is_market_open():
            try:
                subprocess.run(["python", "/app/src/database.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running database update: {e}")
        time.sleep(60.0)


# Flask endpoints
@app.route('/portfolio_value', methods=['GET'])
def portfolio_value():
    return "test"

@app.route('/profit_loss', methods=['GET'])
def profit_loss():
    status = "THE MARKET IS OPEN!" if is_market_open() else "THE MARKET IS CLOSED!\nAS OF MARKET CLOSE!"
    return f"{status}\n{overall_profit_loss()}"

@app.route('/portfolio_positions', methods=['GET'])
def return_portfolio_positions():
    return get_portfolio_positions()

@app.route('/biggest_winner_daily', methods=['GET'])
def return_biggest_winner_daily():
    return get_biggest_winning_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_day_start_date(),
        get_day_end_date()
    )

@app.route('/biggest_winner_weekly', methods=['GET'])
def return_biggest_winner_weekly():
    return get_biggest_winning_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_week_start_date(),
        get_week_end_date()
    )

@app.route('/biggest_winner_monthly', methods=['GET'])
def return_biggest_winner_monthly():
    return get_biggest_winning_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_month_start_date(),
        get_month_end_date()
    )

@app.route('/biggest_winner_quarterly', methods=['GET'])
def return_biggest_winner_quarterly():
    return get_biggest_winning_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_quarter_start_date(),
        get_quarter_end_date()
    )

@app.route('/biggest_loser_daily', methods=['GET'])
def return_biggest_loser_daily():
    return get_biggest_losing_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_day_start_date(),
        get_day_end_date()
    )

@app.route('/biggest_loser_weekly', methods=['GET'])
def return_biggest_loser_weekly():
    return get_biggest_losing_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_week_start_date(),
        get_week_end_date()
    )

@app.route('/biggest_loser_monthly', methods=['GET'])
def return_biggest_loser_monthly():
    return get_biggest_losing_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_month_start_date(),
        get_month_end_date()
    )

@app.route('/biggest_loser_quarterly', methods=['GET'])
def return_biggest_loser_quarterly():
    return get_biggest_losing_position(
        open_portfolio_positions_databases,
        open_portfolio_positions_collections,
        get_quarter_start_date(),
        get_quarter_end_date()
    )

# Entry point
if __name__ == '__main__':
    # Start background thread for DB updates
    threading.Thread(target=update_database_periodically, daemon=True).start()

    # Run Flask app
    app.run(host='0.0.0.0', port=5000)