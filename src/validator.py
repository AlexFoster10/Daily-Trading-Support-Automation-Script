import pandas as pd
import logging
from pydantic import ValidationError, BaseModel
from pydantic_extra_types.currency_code import Currency
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='mainLog.log', filemode='a')
class CurrencyModel(BaseModel):
    currency: Currency
def is_valid_currency(c):
        try:
            CurrencyModel(currency=c)
            return True
        except ValidationError:
            return False

def validate_pnl(file_path):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['date','realized_pnl','unrealized_pnl','total_pnl','currency']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"PNL file: missing column: {col}")
                return False
    except Exception as e:
        logger.error(f"Error validating pnl file: {e}")
        return False
    
    try:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        if df['date'].isnull().any():
            logger.error("PNL file: Invalid date format found in date column")
            return False 
    except Exception as e:
        logger.error(f"PNL file: Error converting date column to datetime: {e}")
        return False

    try:
        df.loc[:, 'realized_pnl'] = pd.to_numeric(df['realized_pnl'], errors='coerce')
        df.loc[:, 'unrealized_pnl'] = pd.to_numeric(df['unrealized_pnl'], errors='coerce')
        df.loc[:, 'total_pnl'] = pd.to_numeric(df['total_pnl'], errors='coerce')
        if df[['realized_pnl', 'unrealized_pnl', 'total_pnl']].isnull().any().any():
            logger.error("PNL file: Non-numeric values found in pnl columns")
            return False
    except Exception as e:
        logger.error(f"PNL file: Error converting pnl columns to numeric: {e}")
        return False
    
    try:
        if not df['currency'].apply(is_valid_currency).all():
            logger.error("PNL file: Invalid currency codes found in currency column")
            return False
    except Exception as e:
        logger.error(f"PNL file: Error validating currency codes: {e}")
        return False
    


    logger.info("PNL file validation successful")
    return df

def validate_positions(file_path):
    try:
        df = pd.read_csv(file_path)
        df_copy = df
        required_columns = ['symbol','quantity','avg_price','market_price','unrealized_pnl','currency']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Positions file: missing column: {col}")
                return False
    except Exception as e:
        logger.error(f"Positions file: Error validating positions file: {e}")
        return False
    df.dropna(inplace=True)

    try:
        symbol = df['symbol'].astype(str)

        symbol = symbol.str.contains(r"\s")

        if symbol.any():
            df = df[~symbol]
            logger.info("Positions file: Dropped rows with whitespace in symbol column")
    except Exception as e:
        logger.error(f"Positions file: Error validating symbol column: {e}")
        return False

    try:
        df.loc[:, 'quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df.loc[:, 'avg_price'] = pd.to_numeric(df['avg_price'], errors='coerce')
        df.loc[:, 'market_price'] = pd.to_numeric(df['market_price'], errors='coerce')
        df.loc[:, 'unrealized_pnl'] = pd.to_numeric(df['unrealized_pnl'], errors='coerce')
        if df.isnull().values.any():
            df.dropna(inplace=True)
            logger.info("Positions file: Dropped all non numeric rows")
    except Exception as e:
        logger.error(f"Positions file: Error converting numeric columns to numeric: {e}")
        return False
    
    try:
        valid_mask = df['currency'].apply(is_valid_currency)
        invalid_rows = df.loc[~valid_mask]
        if not invalid_rows.empty:
            logger.warning("Positions file: Dropped rows with invalid currency values")
        df = df.loc[valid_mask].copy()
                    
    except Exception as e:
        logger.error(f"Positions file: Error validating currency codes: {e}")
        return False


    logger.info("Positions file validation successful")
    dropped_rows = df_copy[~df_copy.index.isin(df.index)]
    if not dropped_rows.empty:
        logger.info(f"Positions file: Dropped rows due to invalid data:\n{dropped_rows}")
    return df

def validate_trades(file_path):
    try:
        df = pd.read_csv(file_path)
        df_copy = df
        required_columns = ['trade_id','timestamp','symbol','side','quantity','price','currency']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Trades file: missing column: {col}")
                return False
    except Exception as e:
        logger.error(f"Trades file: Error validating trades file: {e}")
        return False
    df.dropna(inplace=True)

    try:
        if not df['trade_id'].is_unique:
            logger.error("Trades file: Duplicate trade_id values found")
            return False
    except Exception as e:
        logger.error(f"Trades file: Error validating trade_id column: {e}")
        return False

    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
        invalid_timestamps = df['timestamp'].isnull()
        if invalid_timestamps.any():
            logger.info("Trades file: Dropped rows with invalid timestamps")
            df = df.loc[~invalid_timestamps].copy()
    except Exception as e:
        logger.error(f"Trades file: Error converting timestamp column to datetime: {e}")
        return False

    try:
        symbol = df['symbol'].astype(str)

        symbol = symbol.str.contains(r"\s")

        if symbol.any():
            df = df[~symbol]
            logger.info("Trades file: Dropped rows with whitespace in symbol column")
    except Exception as e:
        logger.error(f"Trades file: Error validating symbol column: {e}")
        return False

    try:
        side = df['side'].astype(str).str.lower()
        valid_sides = ['buy', 'sell']
        side_mask = side.isin(valid_sides)
        invalid_rows = df.loc[~side_mask]
        if not invalid_rows.empty:
            logger.warning("Trades file: Dropped rows with invalid side values")
        df = df.loc[side_mask].copy()
    except Exception as e:
        logger.error(f"Trades file: Error validating side column: {e}")
        return False

    try:
        df.loc[:, 'quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df.loc[:, 'price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(inplace=True)
        df = df[df['quantity'] % 1 == 0]
        #logger.info("Dropped all non numeric rows")
    except Exception as e:
        logger.error(f"Trades file: Error converting numeric columns to numeric: {e}")
        return False
    
    try:
        valid_mask = df['currency'].apply(is_valid_currency)
        invalid_rows = df.loc[~valid_mask]
        if not invalid_rows.empty:
            logger.warning("Trades file: Dropped rows with invalid currency values")
        df = df.loc[valid_mask].copy()
                    
    except Exception as e:
        logger.error(f"Trades file: Error validating currency codes: {e}")
        return False


    logger.info("Trades file validation successful")
    dropped_rows = df_copy[~df_copy.index.isin(df.index)]
    if not dropped_rows.empty:
        logger.info(f"Trades file: Dropped rows due to invalid data:\n{dropped_rows}")
    return df