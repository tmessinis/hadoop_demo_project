import sys
import json

from pymongo import MongoClient
from pprint import pprint

def calc_totals(json_dict):
    car_model_totals = []
    annual_totals = []
    data_dict = {}
    total = 0
    
    for doc in json_dict:
        for key in doc:
            if key == 'model_name':
                data_dict[key] = doc[key]
            else:
                for year in doc[key]:
                    total += doc[key][year]
    
        data_dict['total_sales'] = total
        car_model_totals.append(data_dict)
        data_dict = {}
        total = 0
    
    for key in json_dict[0]:
        if key == 'annual_sales':
            for year in json_dict[0][key]:
                data_dict[year] = 0
            break
    
    for doc in json_dict:
        for key in doc:
            if key == 'annual_sales':
                for year in doc[key]:
                    data_dict[year] += doc[key][year]
                
    for key in data_dict:
        temp_dict = {}
        temp_dict[key] = data_dict[key]
        annual_totals.append(temp_dict)
     
    pprint(car_model_totals)
    pprint(annual_totals)

data = open(sys.argv[1], 'r')
calc_totals(json.load(data))