import sys
import xlrd
import json

from pprint import pprint
from pymongo import MongoClient

# Script will attempt to convert vehicle sale data from an excel spreasheet from
# http://www.afdc.energy.gov/data/ , into a dict or json format to store in MongoDB.
    
# Helper function which parses json whether it's from a json file or from a python dict.    
def parse_json(json_data, option):
    # Conditionals to check and see if the json_data parameter is a dict or not. It then
    # dictates whether a json file should be written (json_data == dict) or if a json file
    # should be read (json_data != dict).
    try:
        with open('data.json', option) as data:
            return json.dump(json_data, data)
    except Exception as error:
        print('There was an problem generating the data.json file.')
            
        return None 

def mongodb_import(data_lst):
    client = MongoClient("mongodb://pymongouser:123456@10.0.1.34/test_car_sales_db")
        
    db = client.test_car_sales_db
    
    for item in data_lst:
        db.car_sales.insert(item)
        
    print(db.car_sales.find())
    
    return None
            
def parse_file(spreadsheet):
    # Use xlrd module to import the spreadsheet into python. We then pull the data
    # from the first sheet in the file.
    workbook = xlrd.open_workbook(spreadsheet)
    sheet = workbook.sheet_by_index(0)
    
    # Initialize variables to be used by for loops below.
    data_dict = {}
    annual_sales_dict = {}
    temp_lst = []
    car_models_lst = []
    
    # Two for loops are used to cycle through the data from the spreadsheet. The outer
    # loop cycles through the rows and the inner loop cycles through the columns.
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            # Avoid cells before row 3 col 2 which do not hold any significance.
            if row < 3 or col < 2:
                continue
            # Rows 3 or greater under col 2 hold the model names.
            elif row >= 3 and col == 2:
                # Ignore totals and information that do not pertain to the car sales numbers.
                if len(sheet.cell_value(row, col)) > 30 or sheet.cell_value(row, col) == 'TOTAL' \
                or sheet.cell_value(row, col) == '':
                    continue
                else:
                    data_dict['model_name'] = sheet.cell_value(row, col)
            else:
                # Ignore totals.
                if sheet.cell_value(2, col) == 'Total':
                    data_dict['annual_sales'] = annual_sales_dict
                    temp_lst.append(data_dict)
                    data_dict = {}
                    annual_sales_dict = {}
                    continue
                else:
                    amount = None
                    if sheet.cell_value(row, col) == '':
                        amount = 0
                    else:
                        amount = sheet.cell_value(row, col)
                    
                    #data_dict[str(sheet.cell_value(2, col))[:-2]] = int(amount)
                    annual_sales_dict[str(sheet.cell_value(2, col))[:-2]] = int(amount)
    
    for item in temp_lst:
        if 'model_name' in item:
            car_models_lst.append(item)
    
    pprint(car_models_lst)
    parse_json(car_models_lst, 'w')
    #mongodb_import(car_models_lst)

# The spreadsheet needs to be passed as an argument from the cli.    
parse_file(sys.argv[1])