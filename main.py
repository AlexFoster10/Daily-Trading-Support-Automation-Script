import src.file_checker
import src.validator
import datetime

def main():
    parent_path = "input_data"
    #exists, all_present = src.file_checker.arrival_loop(parent_path)
    if True:
        src.validator.validate_pnl(f"{parent_path}/pnl_{datetime.datetime.now().strftime('%Y%m%d')}.csv")        
        src.validator.validate_positions(f"{parent_path}/positions_{datetime.datetime.now().strftime('%Y%m%d')}.csv")     
        src.validator.validate_trades(f"{parent_path}/trades_{datetime.datetime.now().strftime('%Y%m%d')}.csv") 
        
if __name__ == "__main__":    
    main()