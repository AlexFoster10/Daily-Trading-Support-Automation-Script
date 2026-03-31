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
                logger.error(f"Missing column: {col}")
                return False
    except Exception as e:
        logger.error(f"Error validating pnl file: {e}")
        return False
    
    try:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        if df['date'].isnull().any():
            logger.error("Invalid date format found in date column")
            return False
    except Exception as e:
        logger.error(f"Error converting date column to datetime: {e}")
        return False

    try:
        df.loc[:, 'realized_pnl'] = pd.to_numeric(df['realized_pnl'], errors='coerce')
        df.loc[:, 'unrealized_pnl'] = pd.to_numeric(df['unrealized_pnl'], errors='coerce')
        df.loc[:, 'total_pnl'] = pd.to_numeric(df['total_pnl'], errors='coerce')
        if df[['realized_pnl', 'unrealized_pnl', 'total_pnl']].isnull().any().any():
            logger.error("Non-numeric values found in pnl columns")
            return False
    except Exception as e:
        logger.error(f"Error converting pnl columns to numeric: {e}")
        return False
    
    try:
        if not df['currency'].apply(is_valid_currency).all():
            logger.error("Invalid currency codes found in currency column")
            return False
    except Exception as e:
        logger.error(f"Error validating currency codes: {e}")
        return False
    


    logger.info("pnl file validation successful")
    return True