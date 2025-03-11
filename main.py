import pandas as pd
import datetime


#row 14 is starting row
#1-17

def datetimefix(column, min = 12, max = 23):
    for i in range(min,max):
        if type(column[i]) == datetime.time:
            date = datetime.datetime(2099, 12, 30).date()
            column[i] = date
        elif type(column[i]) == datetime.datetime:
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

# old example of renaming the columns to be numbers
#collist2 = list(example)
#nums2 = [x for x in range(len(collist2))]
#example.columns = nums2

#testcol17 = df2.loc[12:23,17] # start date
#testcol18 = df2.loc[12:23,18] # end date

#datetimefix(testcol17)
#datetimefix(testcol18)

with pd.ExcelWriter("test2.xlsx") as writer:
    example.to_excel(writer)

"""
col1 = df1.loc[:,"Unnamed: 1"]
col2 = df1.loc[:,"Unnamed: 2"]
col3 = df1.loc[:,"Unnamed: 3"]
col4 = df1.loc[:,"Unnamed: 4"]
col5 = df1.loc[:,"Unnamed: 5"]
col6 = df1.loc[:,"Unnamed: 6"]
col7 = df1.loc[:,"Unnamed: 7"]
col8 = df1.loc[:,"Unnamed: 8"]
col9 = df1.loc[:,"Unnamed: 9"]
col10 = df1.loc[:,"Unnamed: 10"]
col11 = df1.loc[:,"Unnamed: 11"]
col12 = df1.loc[:,"Unnamed: 12"]
col13 = df1.loc[:,"Unnamed: 13"]
col14 = df1.loc[:,"Unnamed: 14"]
col15 = df1.loc[:,"Unnamed: 15"]
col16 = df1.loc[:,"Unnamed: 16"]
col17 = df1.loc[:,"Unnamed: 17"]"""


#colrange = df1[df1.columns[15:18]]

col17 = df1.loc[12:23,17] # start date
col18 = df1.loc[12:23,18] # end date


datetimefix(col17)
datetimefix(col18)


with pd.ExcelWriter("test.xlsx", date_format="YYYY-MM-DD") as writer:
    df1.to_excel(writer)  



