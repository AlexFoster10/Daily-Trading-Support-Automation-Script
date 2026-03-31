import src.file_checker

def main():
    parent_path = input("Enter the path to the directory: ")
    exists, all_present = src.file_checker.arrival_loop(parent_path)
    print(exists)

if __name__ == "__main__":    
    main()