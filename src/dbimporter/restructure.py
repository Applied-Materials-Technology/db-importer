import pandas as pd
import datetime

#df = pd.ExcelFile('data/realdataex.xlsx')


#data = df.parse()


#headers = data.columns.values


def read_data(filename):
    df = pd.ExcelFile(filename)
    data = df.parse()
    headers = data.columns.values

    return data, headers

data, headers = read_data('data/realdataex.xlsx')

def get_units(headers):

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
    units = get_units(headers)
    df2 = pd.concat([pd.DataFrame([units]), data], axis=0)
    return df2

units = get_units(headers)
df2 = pd.concat([pd.DataFrame([units]), data], axis=0)
print(df2)

def write_new_data(data):
    with pd.ExcelWriter("test2.xlsx") as writer:
        data.to_excel(writer)



#unit_struc = write_units()
#write_new_data(unit_struc)