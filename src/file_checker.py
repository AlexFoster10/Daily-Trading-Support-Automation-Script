import os.path
import os
import logging
import time
import datetime
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='mainLog.log', filemode='w')

#cuttoff_time = datetime.datetime.now().replace(hour=15, minute=10, second=0, microsecond=0)
cuttoff_time = datetime.datetime.now() + datetime.timedelta(seconds=2)

def check_files_exist(parent_path):

    pnl = False
    positions = False
    trades = False

    for x in os.listdir(parent_path):
        file_path = os.path.join(parent_path, x)
        if os.path.isfile(file_path) and x == f"pnl_{datetime.datetime.now().strftime('%Y%m%d')}.csv":
            logger.info("pnl file found")
            pnl = True
        elif os.path.isfile(file_path) and x == f"positions_{datetime.datetime.now().strftime('%Y%m%d')}.csv":
            logger.info("positions file found")
            positions = True
        elif os.path.isfile(file_path) and x == f"trades_{datetime.datetime.now().strftime('%Y%m%d')}.csv":
            logger.info("trades file found")
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

    all_files_exist = pnl and positions and trades


    return var, all_files_exist

def arrival_loop(parent_path):
    while True:
        print("Checking for file arrival...")
        now = datetime.datetime.now()
        if now >= cuttoff_time:
            exists, all_present = check_files_exist(parent_path)
            if exists["pnl"]:
                logger.info("pnl file has arrived on time")
            if exists["positions"]:
                logger.info("positions file has arrived on time")
            if exists["trades"]:
                logger.info("trades file has arrived on time")

            return exists, all_present
        time.sleep(1)

