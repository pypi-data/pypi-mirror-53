import threading
import logging
import os

from queue import Queue
from .threadedLoader import ThreadedDataLoader

# custom logger
def custom_logger(logfile):
    logger = logging.getLogger(__name__)
    # setting logging level
    logger.setLevel(logging.ERROR)
    # logging formatter
    logger_formatter = logging.Formatter('%(asctime)s - %(message)s')
    # setting logging file
    logger_handler = logging.FileHandler(logfile, mode='w')
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)
    
    return logger

def download_bulk_data(assetsList, start_date, end_date, interval, data_directory,
                maxNThreads=20, nTrials=3):
    
    logfile = os.path.join(data_directory, '_failed_downloads.log')
    logger = custom_logger(logfile)
    
    nThreads = min(len(assetsList), maxNThreads)
    print("Starting data download. Number of threads used: {}".format(nThreads))
    cnt = 0
    while assetsList:
        failed_downloads = _getBulkData(assetsList, start_date, end_date, interval, 
                                        data_directory, nThreads) 
        assetsList = failed_downloads
        cnt += 1
        print("Downloading assets data: Trial {0} is completed.".format(cnt))
        if cnt >= nTrials:
            break
    
    # Logging assets that failed to download
    msg = "Failed downloads: {}".format(", ".join(failed_downloads) )
    logger.error(msg)
    return failed_downloads

def _getBulkData(assetsList, start_date, end_date, interval, data_directory, 
                        nThreads):
    queue = Queue()
    threads = []
    failed_downloads = set()
    
    # give the queue assets data
    for asset in assetsList:
        queue.put(asset)
        
    # create a thread pool and give them a queue
    for i in range(nThreads):
        t = ThreadedDataLoader(queue, start_date, end_date, interval, data_directory)
        t.name = "Thread-{0}".format(i)
        
        threads.append(t)
        
        t.setDaemon(True)
        t.start()

    # wait for the queue to finish
    queue.join()
    
    for thread in threads:
        failed_downloads.update(thread.failed_downloads)
        
    failed_downloads_list = list(failed_downloads)
    failed_downloads_list.sort()
    
    return failed_downloads_list

    