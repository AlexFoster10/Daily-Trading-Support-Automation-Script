import pathlib
import sys
temp = pathlib.Path(__file__).parent.parent.resolve().as_posix()
sys.path.append(temp)
import unittest
from src import file_checker

class TestFileChecker(unittest.TestCase):

    def test_valid_path_main_bool(self):
        # Test with a valid file path
        var, all_files_exist = file_checker.check_files_exist("input_data")
        self.assertTrue(all_files_exist)

    def test_invalid_path_main_bool(self):
        # Test with an invalid file path
        var, all_files_exist = file_checker.check_files_exist("src")
        self.assertFalse(all_files_exist)
    
    def test_valid_path_dict(self):
        # Test with a valid file path
        var, all_files_exist = file_checker.check_files_exist("input_data")
        self.assertTrue(var["pnl"] and var["positions"] and var["trades"])

    def test_invalid_path_dict(self):
        # Test with an invalid file path
        var, all_files_exist = file_checker.check_files_exist("src")
        self.assertFalse(var["pnl"] and var["positions"] and var["trades"])

    def test_valid_path_arrival_loop(self):
        # Test with a valid file path
        var, all_files_exist = file_checker.arrival_loop("input_data")
        self.assertTrue(var["pnl"] and var["positions"] and var["trades"] and all_files_exist)

    def test_invalid_path_arrival_loop(self):
        # Test with an invalid file path
        var, all_files_exist = file_checker.arrival_loop("src")
        self.assertFalse(var["pnl"] and var["positions"] and var["trades"] and all_files_exist)


if __name__ == '__main__':
    unittest.main()