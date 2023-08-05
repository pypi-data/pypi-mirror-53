# YahooFinanceDataLoader

YahooFinanceDataLoader allows to download historical quotes data in bulk
from the YahooFinance website. The downloaded data is in csv format.

## API

#### Implemented methods:  
- download_bulk_data  
- get_assets_from_csv


**download_bulk_data** ( assetsList, start_date, end_date, interval, data_directory, maxNThreads=20, nTrials=3 )
	
Method description: downloads stocks historical data from YahooFinance in csv format.

**Return Value**: a list of symbols for which download has failed
	
###### Parameters:
- assetsList - list of assets, for example ['AAPL', 'MSFT', 'NVDA']
- start_date - start date for your download ('yyyy-mm-dd'), for example '2019-01-01'
- end_date - end date for your download ('yyyy-mm-dd'), for example '2019-01-31'
- interval - download interval, '1d' for daily, '1wk' for weekly, '1mo'
- data_directory - directory location to save downloaded data
	
###### Optional parameters:
- maxNThreads - maximum number of threads to use for data download, 
		the default value is 20.
- nTrials - number of trials to be used for download, the default
		value is 3. Explanation: due to connectivity issues your download may fail, 
		and it is worth trying to re-send your download request.
		
###### Example:

```python
from YahooFinanceDataLoader import download_bulk_data

assetsList = ['AAPL', 'ADBE', 'AMZN', 'CSCO', 'FB', 'GOOGL', 'FAKE'] 
start_date = '2018-01-01'
end_date = '2018-01-31'
interval = '1d'
data_directory = '/home/user_name/stock_price_data'
maxNThreads = 20
nTrials = 3

failed_downloads = download_bulk_data(assetsList, start_date, end_date, interval, 
					data_directory, maxNThreads, nTrials)
print('Failed downloads: ', failed_downloads)
```

**get_assets_from_csv** ( csv_file, field_list = ['Symbol', 'Company'] )

	
Method description: reads assets from the csv file and returns a list of assets.
	csv file has to have a header, and the column containing stock symbols has
	to be named 'Symbol'

**Return Value**: a list of asset symbols read from the csv file
	
###### Parameters:
- csv_file - path to the csv file containing assets data

###### Optional parameters:
- field_list - a list containing csv file header names, 
      for example ['Symbol', 'Company']
	
###### Example:

```python
from YahooFinanceDataLoader import download_bulk_data

assetsList = get_assets_from_csv('/home/user_name/assets.csv', ['Symbol', 'Company'])
start_date = '2018-01-01'
end_date = '2018-01-31'
interval = '1d'
data_directory = '/home/user_name/stock_price_data'
maxNThreads = 20
nTrials = 3

failed_downloads = download_bulk_data(assetsList, start_date, end_date, interval, 
					data_directory, maxNThreads, nTrials)
print('Failed downloads: ', failed_downloads)
```

