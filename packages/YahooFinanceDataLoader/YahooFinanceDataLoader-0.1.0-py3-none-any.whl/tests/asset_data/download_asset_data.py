import unittest
from unittest.mock import Mock, patch
import builtins
import os

from YahooFinanceDataLoader.asset_data.download_asset_data import download_asset_data
from YahooFinanceDataLoader.asset_data.assetDataRequest import AssetDataRequest

class TestClass_download_asset_data(unittest.TestCase):
    def setUp(self):         
        self.symbol = 'MSFT'
        self.sdate = '2018-01-01'
        self.edate = '2018-01-31'
        self.interval = '1d'
        
        self.data_file_name = ("_").join([self.symbol, self.sdate, self.edate,
                                        self.interval]) + ".csv"
    
    def test_download_directory_does_nont_exist(self): 
        """Description: download directory does not exist, raise FileNotFoundError
        """
        symbol = self.symbol
        sdate = self.sdate
        edate = self.edate
        interval = self.interval
        data_directory = 'does_not_exist'
        
        self.assertRaises(FileNotFoundError, download_asset_data,
                          symbol, sdate, edate, interval, data_directory)
      
    @patch('os.path.isdir')    
    @patch('os.path.isfile')
    def test_data_file_exists(self, mock_isfile, mock_isdir):
        """Description: test for return value when data file already exists
        """
        symbol = self.symbol
        sdate = self.sdate
        edate = self.edate
        interval = self.interval
        data_directory = 'mocked_directory'
        
        file_location = os.path.abspath( os.path.join(data_directory, self.data_file_name) )
        
        expected_value = {
            'status':0,
            'file_location': file_location
            }
        
        # mocking os.path.isdir method
        mock_isdir.return_value = True
        
        # mocking os.path.isfile method
        mock_isfile.return_value = True
        
        # action
        actual_value = download_asset_data(symbol, sdate, edate, interval, data_directory)
        
        # assertion
        self.assertDictEqual(actual_value, expected_value, 
            "The response is expected to be {}".format(expected_value))   
        
    @patch.object(AssetDataRequest, 'request_data_download')    
    @patch('os.path.isdir')    
    @patch('os.path.isfile')
    def test_on_data_download_error(self, mock_isfile, mock_isdir,
                                          mock_request_data_download):
        """Description: test for return value when data download response contains an error (-2, -1, 1, 2)
        """  
        symbol = self.symbol
        sdate = self.sdate
        edate = self.edate
        interval = self.interval
        data_directory = 'mocked_directory'

        
        expected_value = {
            'status': 1,
            'file_location': ''
            }        

        # mocking os.path.isdir method
        mock_isdir.return_value = True
        
        # mocking os.path.isfile method
        mock_isfile.return_value = False
        
        # mocking AssertDataDownload.request_data_download       
        errors = [{'error':-2}, {'error':-1}, {'error':1}, {'error':2} ] 
        mock_request_data_download.side_effect = errors
        
        # action
        cnt = 0
        for err in errors:
  
            actual_value = download_asset_data(symbol, sdate, edate, interval, data_directory)
            self.assertEqual(mock_request_data_download.call_count, cnt+1)
            self.assertDictEqual(actual_value, expected_value, 
                "The response is expected to be {}".format(expected_value)) 
                   
            cnt += 1
    
    @patch("builtins.open")        
    @patch.object(AssetDataRequest, 'request_data_download')    
    @patch('os.path.isdir')    
    @patch('os.path.isfile')
    def test_on_success(self, mock_isfile, mock_isdir,
                        mock_request_data_download, mock_open):
        """Description: test for return value on success
        """  
        symbol = self.symbol
        sdate = self.sdate
        edate = self.edate
        interval = self.interval
        data_directory = 'mocked_directory'
        
        file_location = os.path.abspath( os.path.join(data_directory, self.data_file_name) )
 
        expected_value = {
            'status': 0,
            'file_location': file_location
            } 
        
        # mocking os.path.isdir method
        mock_isdir.return_value = True
        
        # mocking os.path.isfile method
        mock_isfile.return_value = False
        
        # mocking AssertDataDownload.request_data_download    
        data_download_response = {
            'response_object': Mock(),
            'status_code': 200,
            'error':0
            }
        mock_request_data_download.return_value = data_download_response
        
        # mocking writing to file
        mock_file = Mock()
        mock_file.write.return_value = 0
        mock_open.return_value.__enter__ = mock_file

        # action
        actual_value = download_asset_data(symbol, sdate, edate, interval, data_directory)
        
        # assertion
        self.assertDictEqual(actual_value, expected_value, 
                        "The response is expected to be {}".format(expected_value)) 

     
