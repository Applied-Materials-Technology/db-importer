import pandas as pd
import datetime
import json


#data, headers = read_data('data/realdataex.xlsx')

def read_data(filename: str):

    """
    Read from excel file to check and return dict of sheetname: sheet_data


    Parameters
    ----------

        filename: str
            Path to excel file to be checked for importing

    Returns
    -------

        sheet_names : list
            A list of the sheet names from the file being read
        sheets : dict
            A dictionary of the sheet_names and the pandas dataframe parsed from those sheets
    """

    df = pd.ExcelFile(filename)
    sheets = {}
    sheet_names = df.sheet_names
    for i in sheet_names:
        sheets[i] = df.parse(i)

    return sheet_names, sheets

def get_units(headers):
    """
    Finds the units in the headers and 
    """
    units = {}

    for i in headers:
        try:
            start = i.index("(")+1
            end = i.index(")")

            unit = i[start:end]
            units[i] = unit
        except:
            units[i] = None

    return units

def write_units(headers, data, units=None):
    """
    Write the units to the first row of the new dataframe
    """
    units = get_units(headers)
    df2 = pd.concat([pd.DataFrame([units]), data], axis=0)
    return df2

def write_new_data(data):
    """
    Write the new dataframe to a file
    """
    with pd.ExcelWriter("test2.xlsx") as writer:
        data.to_excel(writer)

def find_me():
    print("module found")
    return True

def start(filename):
    print("STARTING RESTRUCTURE ATTEMPT")
    data, headers = read_data(filename)
    new_df = write_units(headers, data)
    write_new_data(new_df)

def test1():
    text1 = "test1 found"
    return text1

def test2():
    text2 = "test1 found"
    return text2

def test3(issues_data):
    print(issues_data)


def restructure(filename,
                detected_issues = None):
    
    test = {test1:"value1", test2:"value2"}

    for key, val in test.items():
        key()
    if detected_issues:
        with open (detected_issues, "r") as fi:
            my_issues = json.load(fi)

class Revamper():

    def __init__(self,
                test1: str = test1(),
                test2: str = test2(),
                test3: str = None):
    
        self.test1 = test1
        self.test2 = test2
        self.test3 = self.test3()

    def test3(self):
        test3text = "test3 found"
        return test3text