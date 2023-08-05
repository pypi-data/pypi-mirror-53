import threading
from YahooFinanceDataLoader.asset_data.download_asset_data import download_asset_data

class ThreadedDataLoader(threading.Thread):
    """Threaded File Downloader"""
    def __init__(self, queue, start_date, end_date, interval, data_directory):
        """Initialize the thread"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data_directory = data_directory
        
        self.failed_downloads = set()

    def run(self):
        """Run the thread"""
        while True:
            # gets the asset symbol from the queue
            aSymbol = self.queue.get()
            sdate = self.start_date
            edate = self.end_date
            interval = self.interval
            data_directory = self.data_directory
            
            # download asset data
            dStatus = download_asset_data(aSymbol, sdate, 
                                          edate, interval, data_directory)
            
            # if status not 0, add symbol to failed downloads list       
            if dStatus['status']:
                self.failed_downloads.add(aSymbol)            
         
            # send a signal to the queue that the job is done
            self.queue.task_done()  
            
            