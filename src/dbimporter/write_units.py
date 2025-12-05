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
    data1 = data["Sheet1"].set_index('Category')
    for i in data1.loc["Entry"]:
        print(i)
    #write_new_data(new_df)