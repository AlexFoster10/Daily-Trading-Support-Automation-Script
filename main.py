import src.file_checker

def main():
    parent_path = input("Enter the path to the directory: ")
    result = src.file_checker.check_files_exist(parent_path)
    print(result)

if __name__ == "__main__":    
    main()