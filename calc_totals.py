import sys
import json

from pymongo import MongoClient
from pprint import pprint

def calc_totals(json_dict):
    car_model_totals = []
    annual_totals = []
    data_dict = {}
    total = 0
    
    for key in json_dict:
        if key == 'model_name':
            data_dict[key] = json_dict[key]
        else:
            for year in json_dict[key]:
                total += json_dict[key][year]
    
    data_dict['total_sales'] = total
    car_model_totals.append(data_dict)
    data_dict = {}
    
    for key in json_dict:
        if key == 'annual_sales':
            for year in json_dict[key]:
                data_dict[year] = []
            break
    
    for key in json_dict:
        if key == 'annual_sales':
            for year in json_dict[key]:
                data_dict[year].append(json_dict[key][year])
                
    for key in data_dict:
        temp_dict = {}
        temp_dict[key] = sum(data_dict[key])
        annual_totals.append(temp_dict)
     
    pprint(car_model_totals)
    pprint(annual_totals)

data = open(sys.argv[1], 'r')
calc_totals(json.load(data))