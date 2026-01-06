import pandas as pd
import datetime


#row 14 is starting row
#1-17

def datetimefix(column, min = 12, max = 23):
    for i in range(min,max):
        if type(column[i]) is datetime.time:
            date = datetime.datetime(2099, 12, 30).date()
            column[i] = date
        elif type(column[i]) is datetime.datetime:
            date = column[i].date()
            column[i] = date


df1 = pd.read_excel('data/SQ2024-1450 CAT SC_LCF Summary Data (100924).xlsx', sheet_name='Report Tables', keep_default_na=False)
df2 = pd.read_excel('data/SQ2024-1450 CAT SC_LCF Summary Data (100924).xlsx', sheet_name='Report Tables', keep_default_na=False)


collist = list(df1)
nums = [x for x in range(len(collist))]
df1.columns = nums

namelist = []

columnnames = df2.loc[9:11]
for i in columnnames:
    aname = columnnames.loc[9,i]+columnnames.loc[10,i]+columnnames.loc[11,i]
    namelist.append(aname) # list of column names

namelist = namelist[1:] # to get rid of the first empty element
example = df2.loc[12:23, 'Unnamed: 1':] # takes values WITHOUT name of columns
example = example.reset_index(drop = True) # starts new row index at 1
example.columns = namelist # renames the columns to the original name (but one line)

#NEWER EXAMPLE
with pd.ExcelWriter("test2.xlsx") as writer:
    example.to_excel(writer)


col17 = df1.loc[12:23,17] # start date
col18 = df1.loc[12:23,18] # end date


datetimefix(col17)
datetimefix(col18)

#OLD EXAMPLE
with pd.ExcelWriter("test.xlsx", date_format="YYYY-MM-DD") as writer:
    df1.to_excel(writer)  


#mystring = 'RT01'
#mystring = 'SMaRT Contract Number:'
mystring = 'SMaRT Programme Owner:' 
#SMaRT Programme Owner string works but the SMaRT Contract Number string doesn't
# Define a search function
def search_string(s, search):
    return search in str(s)

# should return only the row with rt01
mask = df2.apply(lambda x: x.map(lambda s: search_string(s,mystring)))


# Filter the DataFrame based on the mask
filtered_df = df2.loc[mask.any(axis=1)]
#print(filtered_df)


print(df2.iat[0,12])
print(df2.iat[0,15])

#gives project manager and name
print(df2.iat[1,12])
print(df2.iat[1,15])