import unittest
from YahooFinanceDataLoader.asset_data.assetDataRequest import AssetDataRequest

class TestClass_AssetDataRequest_init(unittest.TestCase):
    def setUp(self):         
        self.asset_symbol = 'MSFT'
        self.interval = '1d'
        self.start_date = {
            'date':'2018-01-01',
            'ts': 1514764800
            }
        self.end_date = {
            'date':'2018-01-31',
            'ts': 1517356800
            }
        
    def test_initialize_with_correct_parameters(self):
        """ Description: initialization of AssetDataRequest object when parameters are correct
        """
        aSymbol = self.asset_symbol
        sdate  = self.start_date['date']
        edate = self.end_date['date']
        sts = self.start_date['ts']
        ets = self.end_date['ts']
        interval = self.interval
        
        ADR = AssetDataRequest(aSymbol, sdate, edate, interval)
        self.assertEqual(ADR.symbol, 'MSFT', 'Expected symbol is "MSFT"')
        self.assertEqual(ADR.interval, '1d', 'Expected interval is "1d"')
        self.assertEqual(ADR.start_date, sts, 
                         'Start date is expected to be equal {0}'.format(sts))
        self.assertEqual(ADR.end_date, ets, 
                         'End date is expected to be equal {0}'.format(ets))
        
        
    def test_initialize_with_wrong_dates(self):
        """Description: raise ValueError when start date is greater than end date
        """
        aSymbol = self.asset_symbol
        sdate  = self.end_date['date']
        edate = self.start_date['date']
        interval = self.interval
        
        self.assertRaises(ValueError, AssetDataRequest, aSymbol, sdate, edate, interval)
        
if __name__ == '__main__':
    unittest.main()
        
        
        