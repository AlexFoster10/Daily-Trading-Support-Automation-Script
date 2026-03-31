import os.path
import os
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='mainLog.log', filemode='w')



def check_files_exist(parent_path):

    pnl = False
    positions = False
    trades = False

    for x in os.listdir(parent_path):
        file_path = os.path.join(parent_path, x)
        if os.path.isfile(file_path) and x.startswith("pnl_") and (".csv" in file_path):
            pnl = True
        elif os.path.isfile(file_path) and x.startswith("positions_") and (".csv" in file_path):
            positions = True
        elif os.path.isfile(file_path) and x.startswith("trades_") and (".csv" in file_path):
            trades = True

    if not pnl:
        logger.warning("pnl file is missing")
    if not positions:
        logger.warning("positions file is missing")
    if not trades:
        logger.warning("trades file is missing")

    var = {
        "pnl": pnl,
        "positions": positions,
        "trades": trades
    }

    return var

