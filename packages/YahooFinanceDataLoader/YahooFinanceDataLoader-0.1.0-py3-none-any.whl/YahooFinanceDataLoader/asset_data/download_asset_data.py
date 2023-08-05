import os
from .assetDataRequest import AssetDataRequest

def download_asset_data(symbol, sdate, edate, interval, data_directory):
    download_status = {
        'status':1,
        'file_location':''
    }
    
    # if data directory does not exist raise error
    if not os.path.isdir(data_directory):
        raise FileNotFoundError("Directory {0} does not exist".format(data_directory))
    
    # data file name
    fname = ('_').join([symbol, sdate, edate, interval]) + '.csv'
    datafile = os.path.join(data_directory, fname)
    
    # data file for asset already exists 
    if os.path.isfile(datafile):        
        download_status['status'] = 0
        download_status['file_location'] = os.path.abspath(datafile)
        return download_status
    
    # data for asset needs to be downloaded    
    d = AssetDataRequest(symbol, sdate, edate, interval)
    ro = d.request_data_download()
    
    if ro['error'] == 0:        
        with open(datafile, 'w') as out:
            out.write( ro['response_object'].text ) 
        download_status['status'] = 0
        download_status['file_location'] = os.path.abspath(datafile)
    
    return download_status
    
        