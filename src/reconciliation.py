import pandas as pd
import logging
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='mainLog.log', filemode='a')

def yesterday_trade_comparison(trades_file, trade_df : pd.DataFrame):
    try:
        yesterday_df = pd.read_csv(trades_file)
    except Exception as e:
        logger.error(f"ERROR reading input files: {e}")
        return False
    
    try:
        logger.info(f"RESULT: Yesterday's Trades: {yesterday_df.shape[0]}///Today's Trades: {trade_df.shape[0]}")
    except Exception as e:
        logger.error(f"ERROR comparing trade dataframes: {e}")
        return False
def notional_comparision():
    pass
def record_count_comparison(trade_df : pd.DataFrame):
    try:
        temp = trade_df.copy()
        temp['notional'] = temp['quantity'] * temp['price']
        logger.info(f"RESULT: Total Notional Value: {temp['notional'].sum()}")
    except Exception as e:
        logger.error(f"ERROR calculating notional value: {e}")
        return False