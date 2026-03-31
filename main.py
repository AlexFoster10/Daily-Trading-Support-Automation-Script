import src.file_checker
import src.validator
import datetime
import pandas as pd

def main():
    parent_path = "input_data"
    #exists, all_present = src.file_checker.arrival_loop(parent_path)
    if True:
        pd1 = src.validator.validate_pnl(f"{parent_path}/pnl_{datetime.datetime.now().strftime('%Y%m%d')}.csv")        
        pd2 = src.validator.validate_positions(f"{parent_path}/positions_{datetime.datetime.now().strftime('%Y%m%d')}.csv")     
        pd3 = src.validator.validate_trades(f"{parent_path}/trades_{datetime.datetime.now().strftime('%Y%m%d')}.csv")

        print(pd3)
        
if __name__ == "__main__":    
    main()