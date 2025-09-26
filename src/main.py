import logging
import threading
import time
import subprocess
from flask import Flask
from functions.logging_config import configure_logging
from functions.time_functions import *
from functions.database_functions import *

# -------------------------
# Configure shared logging
# -------------------------
configure_logging("application.log")
logging.info("Starting Flask application...")

# -------------------------
# Flask app initialization
# -------------------------
app = Flask(__name__)
app.config["DEBUG"] = True

# -------------------------
# Constants
# -------------------------
OPEN_PORTFOLIO_DB = ["open_portfolio_positions"]
OPEN_PORTFOLIO_COLLECTIONS = [
    "open_portfolio_positions",
    "open_portfolio_positions_weekly",
    "open_portfolio_positions_monthly",
    "open_portfolio_positions_quarterly",
    "open_portfolio_positions_yearly"
]

# -------------------------
# Background DB updater
# -------------------------
def update_database_periodically():
    logging.info("Background DB updater thread started.")
    while True:
        logging.info("DB updater heartbeat...")  # always log so we know it's alive
        try:
            if is_market_open():
                logging.info("Market is open — running database.py")
                try:
                    result = subprocess.run(
                        ["python", "database.py"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if result.stdout:
                        logging.info(f"[database.py STDOUT]\n{result.stdout}")
                    if result.stderr:
                        logging.error(f"[database.py STDERR]\n{result.stderr}")
                    logging.info("database.py completed successfully")
                except subprocess.CalledProcessError as e:
                    logging.exception(f"database.py failed with error: {e}")
            else:
                logging.info("Market closed — skipping database update")
        except Exception:
            logging.exception("Unexpected exception in background updater loop")
        finally:
            time.sleep(60)


# -------------------------
# Launch background thread immediately
# -------------------------
def launch_background_updater():
    logging.info("Launching DB updater thread (import-time)")
    thread = threading.Thread(
        target=update_database_periodically,
        name="DBUpdater",
        daemon=True
    )
    thread.start()

# Start it as soon as the module is imported
launch_background_updater()

# -------------------------
# Flask routes
# -------------------------
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
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_day_start_date(),
        get_day_end_date()
    )

@app.route('/biggest_winner_weekly', methods=['GET'])
def return_biggest_winner_weekly():
    return get_biggest_winning_position(
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_week_start_date(),
        get_week_end_date()
    )

@app.route('/biggest_winner_monthly', methods=['GET'])
def return_biggest_winner_monthly():
    return get_biggest_winning_position(
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_month_start_date(),
        get_month_end_date()
    )

@app.route('/biggest_winner_quarterly', methods=['GET'])
def return_biggest_winner_quarterly():
    return get_biggest_winning_position(
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_quarter_start_date(),
        get_quarter_end_date()
    )

@app.route('/biggest_loser_daily', methods=['GET'])
def return_biggest_loser_daily():
    return get_biggest_losing_position(
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_day_start_date(),
        get_day_end_date()
    )

@app.route('/biggest_loser_weekly', methods=['GET'])
def return_biggest_loser_weekly():
    return get_biggest_losing_position(
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_week_start_date(),
        get_week_end_date()
    )

@app.route('/biggest_loser_monthly', methods=['GET'])
def return_biggest_loser_monthly():
    return get_biggest_losing_position(
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_month_start_date(),
        get_month_end_date()
    )

@app.route('/biggest_loser_quarterly', methods=['GET'])
def return_biggest_loser_quarterly():
    return get_biggest_losing_position(
        OPEN_PORTFOLIO_DB,
        OPEN_PORTFOLIO_COLLECTIONS,
        get_quarter_start_date(),
        get_quarter_end_date()
    )

# -------------------------
# Entry point (local runs)
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=False)