import pandas as pd



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

    if filename.lower().endswith('.csv'):
        df = pd.read_csv(filename)
    elif filename.lower().endswith('.xlsx'):
        df = pd.ExcelFile(filename)
    sheets = {}
    sheet_names = df.sheet_names
    for i in sheet_names:
        sheets[i] = df.parse(i)

    return sheet_names, sheets

def get_headers(sheets, data):
    print("getting headers")

def get_units2(data):
    units = {}
    try:
        start = data.index("(")+1
        end = data.index(")")

        unit = data[start:end]
        units[data] = unit
    except ValueError:
        units[data] = None

    return units

def get_units(headers):
    """
    Finds the units in the headers and return them

        Parameters
    ----------

        headers:
            Headers of the excel file being read

    Returns
    -------

        units : dict
            Dictionary of units from headers
    """
    units = {}

    for i in headers:
        try:
            start = i.index("(")+1
            end = i.index(")")

            unit = i[start:end]
            units[i] = unit
        except ValueError:
            units[i] = None

    return units

def write_units(headers, data, units=None):
    """
    Write the units to the first row of the new dataframe

    Parameters
    ----------

        headers: str
            Headers of the excel file being read
        
        data: DataFrame
            The dataframe containing data of the excel file

        units: dict
            Dictionary of units from headers

    Returns
    -------

        df2 : DataFrame
            Dataframe of the units to be added to excel file
    """
    #units = get_units(headers)
    data1 = data["Sheet1"]
    print(data1.index)
    specific_row = data1.iloc[0]
    #print(specific_row)
    #print(data1.loc("0"))
    #units1 = get_units2(data1)
    #print(units1)
    #print(units)
    #df2 = pd.concat([pd.DataFrame([units]), data], axis=0)
    #print(pd.DataFrame([units]))
    #print(units)
    #print(headers)
    #print(data)
    #df3 = pd.concat([pd.DataFrame([units1]), data1], axis=0)
    df2 = True
    return df2

def write_new_data(data):
    """
    Write the new dataframe to a file

    Parameters
    ----------

        data: DataFrame
            The dataframe containing data of the excel file

    """

    with pd.ExcelWriter("test2.xlsx") as writer:
        data.to_excel(writer)


def start(filename):
    print("STARTING RESTRUCTURE ATTEMPT")
    headers, data = read_data(filename)
    headers2 = get_headers(headers, data)
    new_df = write_units(headers, data)
    print(new_df)
    #write_new_data(new_df)

