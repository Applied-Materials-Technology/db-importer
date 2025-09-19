import pandas as pd
import datetime

def read_data(filename):
    """
    Reads the data from an excel file and gets the headings
    """
    df = pd.ExcelFile(filename)
    data = df.parse()
    headers = data.columns.values

    return data, headers

#data, headers = read_data('data/realdataex.xlsx')

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

def write_units(units=None):
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

def test():
    print("module found")

#unit_struc = write_units()
#write_new_data(unit_struc)