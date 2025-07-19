import logging
import os
from functions.database_functions import *
from functions.get_data_functions import *
from functions.time_functions import *
from functions.transform_data_functions import *
from src.functions import logging as configurecustomlogging

# Configure logging
configurecustomlogging.configure_logging('database.log')
logging.info("Starting data pipeline script...")

# Set environment variable with fallback
retain_data_for_days = int(os.environ.get('RETAIN_DATA_FOR_DAYS', 1000))

# Get current date and time
write_date_time = get_current_date_and_time()

# === Portfolio Value ===
try:
    portfolio_value_db = "portfolio_value"
    portfolio_value_col = "portfolio_value"
    portfolio_value_value = overall_portfolio_value()
    portfolio_value_dict = {
        "portfolio_value": str(portfolio_value_value),
        "last_updated": str(write_date_time)
    }

    existing_document_id = check_if_document_exists_in_database(
        portfolio_value_db,
        portfolio_value_col,
        portfolio_value_dict,
        do_exclude_last_updated_key=False
    )

    insert_or_update_document_in_database(
        portfolio_value_db,
        portfolio_value_col,
        portfolio_value_dict,
        existing_document_id
    )
except Exception as e:
    logging.exception("Error processing portfolio value")

# === Profit & Loss ===
try:
    profit_loss_db = "profit_loss"
    profit_loss_col = "profit_loss"
    profit_loss_value = overall_profit_loss()
    profit_loss_dict = {
        "profit_loss_value": str(profit_loss_value),
        "last_updated": str(write_date_time)
    }

    existing_document_id = check_if_document_exists_in_database(
        profit_loss_db,
        profit_loss_col,
        profit_loss_dict,
        do_exclude_last_updated_key=True
    )

    insert_or_update_document_in_database(
        profit_loss_db,
        profit_loss_col,
        profit_loss_dict,
        existing_document_id
    )
except Exception as e:
    logging.exception("Error processing profit and loss")

# === Open Portfolio Positions ===
try:
    open_positions_db = "open_portfolio_positions"
    unformatted_open_positions_values = get_portfolio_positions()

    if not unformatted_open_positions_values:
        logging.warning("No open portfolio positions found.")
    else:
        for position in unformatted_open_positions_values:
            open_positions_dict = {
                "_id": str(position['ticker']),
                "quantity": str(position['quantity']),
                "averagePrice": str(position['averagePrice']),
                "currentPrice": str(position['currentPrice']),
                "ppl": str(position['ppl']),
                "fxPpl": str(position['fxPpl']),
                "initialFillDate": str(position['initialFillDate']),
                "frontend": str(position['frontend']),
                "maxBuy": str(position['maxBuy']),
                "maxSell": str(position['maxSell']),
                "pieQuantity": str(position['pieQuantity']),
                "last_updated": str(write_date_time)
            }

            # Handle each time frame
            timeframes = {
                "open_portfolio_positions_daily": is_a_weekday(),
                "open_portfolio_positions_weekly": is_end_of_week(),
                "open_portfolio_positions_monthly": is_end_of_month(),
                "open_portfolio_positions_quarterly": is_end_of_quarter(),
                "open_portfolio_positions_yearly": is_end_of_year()
            }

            for collection_name, should_run in timeframes.items():
                if should_run:
                    existing_document_id = check_if_document_exists_in_database(
                        open_positions_db,
                        collection_name,
                        open_positions_dict,
                        do_exclude_last_updated_key=False
                    )
                    insert_or_update_document_in_database(
                        open_positions_db,
                        collection_name,
                        open_positions_dict,
                        existing_document_id
                    )
except Exception as e:
    logging.exception("Error processing open portfolio positions")

# === Clean up old MongoDB data ===
try:
    clean_up_mongodb(time_limit_days=retain_data_for_days)
except Exception as e:
    logging.exception("Error during MongoDB cleanup")
