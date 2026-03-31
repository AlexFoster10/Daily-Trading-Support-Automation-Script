import src.file_checker
import src.validator
import src.reconciliation
import src.reporter
import datetime
import pandas as pd

def main():
    parent_path = "input_data"
    exists, all_present = src.file_checker.arrival_loop(parent_path)
    if True:
        pd1 = src.validator.validate_pnl(f"{parent_path}/pnl_{datetime.datetime.now().strftime('%Y%m%d')}.csv")        
        pd2 = src.validator.validate_positions(f"{parent_path}/positions_{datetime.datetime.now().strftime('%Y%m%d')}.csv")     
        pd3 = src.validator.validate_trades(f"{parent_path}/trades_{datetime.datetime.now().strftime('%Y%m%d')}.csv")
        if pd3 is not False:
            src.reconciliation.yesterday_trade_comparison(f"previous_records/trades_{(datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')}.csv", pd3)
        report = src.reporter.generate_report()
        print(report)
        
if __name__ == "__main__":    
    main()