import sys
import json

from pymongo import MongoClient
from pprint import pprint

def calc_totals(json_dict):
    # Initialize variables to be used by for loops below.
    car_model_totals = []
    annual_totals = []
    data_dict = {}
    total = 0
    
    # First loop through the json document to calculate the total sales
    # by car model.
    for doc in json_dict:
        for key in doc:
            if key == 'model_name':
                data_dict[key] = doc[key]
            else:
                for year in doc[key]:
                    total += doc[key][year]
        
        # Update totals, pass dict to car models list and reset variables.
        data_dict['total_sales'] = total
        car_model_totals.append(data_dict)
        data_dict = {}
        total = 0
    
    # Generate years as keys to be used to calculate annual totals.
    for key in json_dict[0]:
        if key == 'annual_sales':
            for year in json_dict[0][key]:
                data_dict[year] = 0
            break
    
    # Loop through json document to calculate the totals for each year.
    for doc in json_dict:
        for key in doc:
            if key == 'annual_sales':
                for year in doc[key]:
                    data_dict[year] += doc[key][year]
    
    # Append annual totals list so it can be used with MongoDB.
    for key in data_dict:
        temp_dict = {}
        temp_dict[key] = data_dict[key]
        annual_totals.append(temp_dict)
     
    pprint(car_model_totals)
    pprint(annual_totals)

data = open(sys.argv[1], 'r')
calc_totals(json.load(data))