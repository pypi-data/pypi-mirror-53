import requests
import re

from requests.exceptions import ConnectionError, Timeout
from requests.exceptions import HTTPError
from YahooFinanceDataLoader.utils import set_time_point

class AssetDataRequest:
    def __init__(self, symbol, sdate, edate, interval, event = 'history'):
        self.symbol = symbol
        # dates validation
        if (sdate <= edate):
            self.start_date = set_time_point(sdate)
            self.end_date = set_time_point(edate)
        else:
            raise ValueError("Start date is less than or equal to the end date")
        
        self.interval = interval
        
        self.event = event
        
        # urls
        self.url_cookie = "https://finance.yahoo.com/quote/{0}/history".format(self.symbol)
        self.url_data = "https://query1.finance.yahoo.com/v7/finance/download/{0}".format(self.symbol)
        
        # headers
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        self.headers = {'User-Agent':user_agent}
        
        
    def request_download_permission(self):
        aSymbol = self.symbol
        headers = self.headers
        
        response = {
            "cookies": None,
            "crumb": None,
            "status_code": -1,
            "error": -100
            }

        url_cookie = self.url_cookie
        payload_cookie = {'p':aSymbol}
        
        # send request
        try:
            rPermissionData = requests.get(url_cookie, headers=headers, 
                                           params=payload_cookie)            
        except (ConnectionError, Timeout): #Error: ConnectionError or Timeout
            response['error'] = 1
            return response   
        
        # request status code
        status_code = rPermissionData.status_code  
        
        # cookies
        jar = rPermissionData.cookies
        
        # crumb
        rContent = rPermissionData.content.decode('unicode-escape')
        pattern = re.compile('"CrumbStore":{"crumb":"(.+?)"}')
        m = re.search(pattern, rContent)

        try:
            crumb = m.group(1)
        except AttributeError: #Error: failed to obtain crumb
            response['status_code'] = status_code
            response['cookies'] = jar
            response['error'] = 2
            return response
        
        response['status_code'] = status_code
        response['error'] = 0
        response['cookies'] = jar
        response['crumb'] = crumb
        
        return response
        
    def request_data_download(self):
        sdate = self.start_date
        edate = self.end_date
        interval = self.interval
        event = self.event
        
        headers = self.headers
        url_data = self.url_data
        
        response = {
            "response_object": None,
            "status_code": -1,
            "error": -100
            }
        
        permissionData = self.request_download_permission()
        if permissionData['error'] != 0:
            response['error'] = -permissionData['error']
            return response

        cookies = permissionData['cookies']
        crumb = permissionData['crumb']
        
        payload = {"period1": sdate,
                   "period2": edate,
                   "interval": interval,
                   "events": event,
                   "crumb": crumb
        }
        
        # sending request
        try:        
            rData = requests.get(url_data, headers=headers, 
                         cookies=cookies, params=payload, stream=True)
            response["status_code"] = rData.status_code
            
            if rData.status_code != 200:
                rData.raise_for_status()
            
        except HTTPError:            
            response["error"] = 2
            return response
        
        except (ConnectionError, Timeout):
            response["error"] = 1
            return response
        
        response["error"] = 0
        response["response_object"] = rData
        return response
    
        