import unittest
import datetime
from YahooFinanceDataLoader.utils import set_time_point

class Test_SetTimePoint(unittest.TestCase):
           
    def test_return_timestamp_correct_date_1(self):
        """Description: we test function return value for known date and known timestamp
        """
        test_date = '2017-05-12'
        test_timestamp =  1494543600
        self.assertEqual(test_timestamp, set_time_point(test_date))
        
    def test_return_timestamp_correct_date_2(self):
        """Description: we test function return value for known date and known timestamp
        """
        test_date = '2018-02-01'
        test_timestamp =  1517443200
        self.assertEqual(test_timestamp, set_time_point(test_date))
       
    def test_raise_error_incorrect_date_nonexistent_1(self):
        """Description: the error is raised when provided date string is not actual date.
        """
        test_date = '2010-02-31'
        self.assertRaises(ValueError, set_time_point, test_date)
        
    def test_raise_error_incorrect_date_nonexistent_2(self):
        """Description: the error is raised when provided date string is not actual date.
        """
        test_date = '2015-15-03'
        self.assertRaises(ValueError, set_time_point, test_date)
               
        
        