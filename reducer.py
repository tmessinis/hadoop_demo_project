import sys
import json

from pymongo import MongoClient

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

def mongo_export(database, collection):
    return_lst = []
    client = MongoClient("mongodb://pymongouser:123456@10.0.1.34/test_car_sales_db")
    db = eval('client.{0}'.format(database))
    table = eval('db.{0}'.format(collection))
    
    for item in table.find():
        return_lst.append(item)
        
    return return_lst

def mongo_import(database, collection, data_lst):
    client = MongoClient("mongodb://pymongouser:123456@10.0.1.34/test_car_sales_db")
    db = eval('client.{0}'.format(database))
    table = eval('db.{0}'.format(collection))
    
    for item in data_lst:
        table.insert(item)
        
def parse_file(input_text):
    # Initialize variables to be used by for loops below.
    counter = 0
    data_dict = {}
    annual_sales_dict = {}
    car_models_lst = []
    years = ['', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    
    # Loop through the lines passed in through stdin.
    for line in input_text:
        data = line.split('\t')
        # Ignore the TOTAL col. Calculations will be performed by another script.
        #if data[0] == 'TOTAL':
        if data[0] == 'Vehicle':
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
                    if '\n' in amount:
                        amount = amount.strip('\n')
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
    
    
    mongo_import('test_car_sales_db', 'car_sales', car_models_lst)
    print(car_models_lst)
    
def calc_totals(json_dict):
    # Initialize variables to be used by for loops below.
    car_model_totals = []
    annual_totals = []
    data_dict = {}
    total = 0
    years = ['', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    
    # First loop through the json document to calculate the total sales
    # by car model.
    for doc in json_dict:
        for key in doc:
            if key == 'model_name':
                data_dict[key] = doc[key]
            elif key == 'annual_sales':
                for year in doc[key]:
                    total += doc[key][year]
        
        # Update totals, pass dict to car models list and reset variables.
        data_dict['total_sales'] = total
        car_model_totals.append(data_dict)
        data_dict = {}
        total = 0
    
    # Generate years as keys to be used to calculate annual totals.
    for year in years:
        if year == '':
            continue
        else:
            data_dict[year] = 0
            
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
     
    mongo_import('test_car_sales_db', 'car_model_totals', car_model_totals)
    mongo_import('test_car_sales_db', 'annual_totals', annual_totals)
    print(car_model_totals)
    print(annual_totals)
    
parse_file(sys.stdin)
calc_totals(mongo_export('test_car_sales_db', 'car_sales'))