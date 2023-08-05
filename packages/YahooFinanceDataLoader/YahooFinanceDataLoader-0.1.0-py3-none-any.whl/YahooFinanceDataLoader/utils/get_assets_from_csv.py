import os
import csv

def get_assets_from_csv(csv_file, field_list = ['Symbol', 'Company']):
    """
        Input:
            csv_file: location of csv file containing a list of assets
            field_list: csv file field list, it has to contain a field names
                at the top, and a field named 'Symbol'.
                We will be reading assets from this field
        Returns a list of symbols read from csv file       
    """
    # check if csv file exists
    if os.path.isfile(csv_file):
        csvfile = csv_file
    else:
        raise FileNotFoundError
    
    assetlist = []
    
    fieldlist = field_list
    with open(csvfile) as datafile:
        reader = csv.DictReader(datafile, fieldnames = fieldlist)
        #ignore the first row
        next(reader) 
        for row in reader:
            assetlist.append(row['Symbol'].strip())
        
    return assetlist    
    
    