import pandas as pd
import datetime
from dbimporter.expecteddata import ExpectedStruct
from dbimporter.logger import logger
from dbimporter.issuetracker import Issues
import numpy as np
import json

issues = Issues()

testfile = "data/baddata.xlsx"
skeleton = "data/importfileskel.xlsx"

def read_data(filename):
    """
    Read from excel file to check and return dict of sheetname: sheet_data
    """
    df = pd.ExcelFile(filename)

    check_sheets(df.sheet_names)

    sheets = {}
    for i in df.sheet_names:
        sheets[i] = df.parse(i)

    return sheets

def read_columns(column, sheet_data):
    """
    Read the name of the columns in a given sheet
    """
    columnnames = sheet_data.iloc[column]
    columnlist = []
    for i in columnnames:
        columnlist.append(i)

    return columnlist

def check_sheets(sheet_names):
    """
    Check if the sheets are the expected names, and check box if correct
    """
    if sheet_names == ExpectedStruct.sheet_names:
        issues.sheet_names = True
    elif sheet_names != ExpectedStruct.sheet_names:
        issues.sheet_names = False
    else:
        logger.error("Sheets name check could not be determined")
        issues.sheet_names = False

def check_column_names(column_names, sheet_data):
    """
    Check if the columns are the expected names, and check box if correct
    """
    if column_names == sheet_data:
        issues.sheet1_columns = True
    elif column_names != sheet_data:
        issues.sheet1_columns = False
    else:
        logger.error("Column name check could not be determined")
        issues.sheet1_columns = False

def check_units(unitlist):
    """
    Check if the columns are the expected names, and check box if correct
    """
    checknan = np.isnan(unitlist).any()#does not work...
    if checknan == True:
        issues.units = False
    elif checknan == False:
        issues.units == True
    else:
        logger.error("Unit existence check could not be determined")
        issues.units = False

def start(filename):

    sheets_data = read_data(filename)

    column_names1 = read_columns(0, sheets_data["Sheet1"])

    check_column_names(column_names1, ExpectedStruct.sheet_1_columns)

    unit_check = read_columns(1, sheets_data["Sheet1"])
    #check_units(unit_check)

def write_results():
    with open("output.txt", "w") as f:
        for i in issues.__dict__:
            f.write(i+": "+str(issues.__dict__[i])+"\n")
        f.close()

#start(testfile)
print(issues.__dict__)
write_results()
