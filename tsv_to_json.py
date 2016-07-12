import sys
import json

from pymongo import MongoClient
from pprint import pprint

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
    
    return None
        
def parse_file(input_text):
    # Initialize variables to be used by for loops below.
    counter = 0
    data_dict = {}
    annual_sales_dict = {}
    car_models_lst = []
    years = []
    
    # Loop through the lines passed in through stdin.
    for line in input_text:
        if counter == 0:
            # First grab all the year labels to use for each item in the dict.
            for year in line.split('\t'):
                years.append(year)
        else:
            data = line.split('\t')
            # Ignore the TOTAL col. Calculations will be performed by another script.
            if data[0] == 'TOTAL':
                continue
            # Each item in the dict will include the model name of the car.
            else:
                data_dict['model_name'] = data[0]
            
            # For look which adds the annual sales data for each model.
            for idx in range(len(years)):
                if idx == 0 or idx == 18:
                    continue
                else:
                    # Conditionals which clean the data passed through stdin. Empty cells
                    # are addedd as a 0, remove double quotes and commas.
                    if data[idx] == '':
                        annual_sales_dict[years[idx]] = 0
                    else:
                        amount = data[idx]
                        if '"' in amount:
                            amount = amount.strip('"')
                        if ',' in amount:
                            amount = amount.split(',')[0] + amount.split(',')[1]
                        annual_sales_dict[years[idx]] = int(amount)
            data_dict['annual_sales'] = annual_sales_dict
            
        # The dict items get added to a list. Dict items are reset and counter increases
        # by one.
        if data_dict != {}:
            car_models_lst.append(data_dict)
        data_dict = {}
        annual_sales_dict = {}
        counter += 1
    
    pprint(car_models_lst)
    parse_json(car_models_lst, 'w')
    mongodb_import(car_models_lst)

parse_file(sys.stdin)