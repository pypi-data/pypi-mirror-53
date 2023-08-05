import unittest
from unittest.mock import Mock, patch

from YahooFinanceDataLoader.asset_data.assetDataRequest import AssetDataRequest
import requests

class TestClass_AssetDataRequest_request_download_permission(unittest.TestCase):
    def setUp(self):         
        self.symbol = 'MSFT'
        self.sdate = '2018-01-01'
        self.edate = '2018-01-31'
        self.interval = '1d'
    
    @patch.object(requests, 'get', side_effect=requests.exceptions.ConnectionError)
    def test_return_value_on_connection_error(self, requests):
        """ Description: verification of method return value when ConnectionError occurs
        """
        
        expected_resp = {
            "cookies": None,
            "crumb": None,
            "status_code": -1,
            "error": 1
            }

        # action
        asset_data_request = AssetDataRequest(self.symbol, self.sdate, 
                                              self.edate, self.interval)        
        resp = asset_data_request.request_download_permission()      
        # assertion   
        self.assertDictEqual(resp, expected_resp, 
            "The response is expected to be {}".format(expected_resp))  
        
        
    @patch.object(requests, 'get', side_effect=requests.exceptions.Timeout)
    def test_return_value_on_timeout_error(self, requests):
        """ Description: verification of method return value when Timeout error occurs
        """
    
        expected_resp = {
            "cookies": None,
            "crumb": None,
            "status_code": -1,
            "error": 1
            }
        # action
        asset_data_request = AssetDataRequest(self.symbol, self.sdate, 
                                              self.edate, self.interval)        
        resp = asset_data_request.request_download_permission()     
        # assertion    
        self.assertDictEqual(resp, expected_resp, 
            "The response is expected to be {}".format(expected_resp)) 
    
    
    @patch.object(requests, 'get')    
    def test_response_on_no_crumb_received(self, mock_requests_get):
        """ Description: verification of method return value when no crumb received
            (no download permission received)
        """
        
        empty_cookie_jar = requests.cookies.RequestsCookieJar()
        # expected response
        expected_resp = {
            "cookies": empty_cookie_jar,
            "crumb": None,
            "status_code": 200,
            "error": 2
            }
        
        # mocking a response from requests.get
        response = Mock()
        response.status_code = 200
        response.cookies = requests.cookies.RequestsCookieJar()
        response.content = bytes("There is no crumb!", "unicode-escape")
        mock_requests_get.return_value = response
        
        # action
        asset_data_request = AssetDataRequest(self.symbol, self.sdate, 
                                              self.edate, self.interval)        
        actual_resp = asset_data_request.request_download_permission()     
        # assertion   
        self.assertDictEqual(actual_resp, expected_resp, 
            "The response is expected to be {}".format(expected_resp)) 
        
        
    @patch.object(requests, 'get')    
    def test_response_on_success(self, mock_requests_get):
        """ Description: verification of method return value on success
        """
        # response cookies
        cookie_jar = requests.cookies.RequestsCookieJar()
        cookie_jar.set("download_permission_cookie", "welcome", domain='.yahoo.com')
        
        # crumb value found
        crumb = "crumb_value_found"

        # expected response
        expected_resp = {
            "cookies": cookie_jar,
            "crumb": crumb,
            "status_code": 200,
            "error": 0
            }
        
        # mocking a response from requests.get
        response = Mock()
        response.status_code = 200
        response.cookies = cookie_jar
        response.content = bytes('"CrumbStore":{"crumb":"crumb_value_found"}',
                                 'unicode-escape')
        mock_requests_get.return_value = response
        # action
        asset_data_request = AssetDataRequest(self.symbol, self.sdate, 
                                              self.edate, self.interval)        
        actual_resp = asset_data_request.request_download_permission()
        # assertion
        self.assertDictEqual(actual_resp, expected_resp, 
            "The response is expected to be {}".format(expected_resp))         
        
            