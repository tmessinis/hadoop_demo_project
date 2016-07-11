import sys
import xlrd
import pprint

#datafile = "10301_hev_sales.xlsx"

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    
    data_dict = {}
    car_model = ''
    
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            #print(row, col)
            if row < 3 or col < 2:
                continue
            elif row >= 3 and col == 2:
                if len(sheet.cell_value(row, col)) > 30 or sheet.cell_value(row, col) == 'TOTAL':
                    continue
                else:
                    car_model = sheet.cell_value(row, col)
                    data_dict[car_model] = {}
            else:
                if sheet.cell_value(2, col) == 'Total':
                    continue
                else:
                    data_dict[car_model][int(sheet.cell_value(2, col))] = sheet.cell_value(row, col)
                
    pprint.pprint(data_dict)
    
parse_file(sys.argv[1])