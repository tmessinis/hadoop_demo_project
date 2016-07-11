import sys
import xlrd
import pprint

# Script will attempt to convert vehicle sale data from an excel spreasheet from
# http://www.afdc.energy.gov/data/ , into a dict or json format to store in MongoDB.


def parse_file(spreadsheet):
    # Use xlrd module to import the spreadsheet into python. We then pull the data
    # from the first sheet in the file.
    workbook = xlrd.open_workbook(spreadsheet)
    sheet = workbook.sheet_by_index(0)
    
    # Initialize variables to be used by for loops below.
    data_dict = {}
    car_model = ''
    
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
                if len(sheet.cell_value(row, col)) > 30 or sheet.cell_value(row, col) == 'TOTAL':
                    continue
                else:
                    car_model = sheet.cell_value(row, col)
                    data_dict[car_model] = {}
            else:
                # Ignore totals.
                if sheet.cell_value(2, col) == 'Total':
                    continue
                else:
                    data_dict[car_model][int(sheet.cell_value(2, col))] = sheet.cell_value(row, col)
                
    pprint.pprint(data_dict)

# The spreadsheet needs to be passed as an argument from the cli.    
parse_file(sys.argv[1])