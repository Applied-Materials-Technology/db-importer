import pandas as pd
import datetime
from dbimporter.expecteddata import ExpectedStruct
from dbimporter.logger import logger
from dbimporter.issuetracker import Issues
import numpy as np
import json
import math

class Check():

    def __init__(self,
                 filename: str = None,
                 issues = Issues()):
        
        self.filename = filename
        self.issues = issues

        self.start(self.filename)


    def read_data(self, filename):
        """
        Read from excel file to check and return dict of sheetname: sheet_data
        """
        df = pd.ExcelFile(self.filename)

        self.check_sheets(df.sheet_names)

        sheets = {}
        for i in df.sheet_names:
            sheets[i] = df.parse(i)

        return sheets

    def read_columns(self, column, sheet_data):
        """
        Read the name of the columns in a given sheet
        """
        columnnames = sheet_data.iloc[column]
        columnlist = []
        for i in columnnames:
            columnlist.append(i)

        return columnlist

    def check_sheets(self, sheet_names):
        """
        Check if the sheets are the expected names, and check box if correct
        """
        if sheet_names == ExpectedStruct.sheet_names:
            self.issues.sheet_names = True
        elif sheet_names != ExpectedStruct.sheet_names:
            logger.error("Sheets name incorrect")
            self.issues.sheet_names = False
        else:
            logger.error("Sheets name check could not be determined")
            self.issues.sheet_names = False

    def check_column_names(self, column_names, sheet_data):
        """
        Check if the columns are the expected names, and check box if correct
        """
        if column_names == sheet_data:
            self.issues.sheet1_columns = True
        elif column_names != sheet_data:
            self.issues.sheet1_columns = False
        else:
            logger.error("Column name check could not be determined")
            self.issues.sheet1_columns = False

    def check_units(self, unitlist, columnname):
        """
        Check if the columns are the expected names, and check box if correct
        """

        checknan_list = pd.Series(unitlist).isnull()

        for i in range(len(checknan_list)):
            if checknan_list[i] == True:
                checknan = True
                wrong_column = columnname[i]
                error_msg = f"The column {wrong_column} has no units"
                logger.error(error_msg)
            else:
                continue

        if checknan == True:
            self.issues.units = False
        elif checknan == False:
            self.issues.units = True
        else:
            logger.error("Unit existence check could not be determined")
            self.issues.units = False

    def start(self, filename):
        """
        Start the checks
        """

        sheets_data = self.read_data(filename)

        column_names1 = self.read_columns(0, sheets_data["Sheet1"])

        self.check_column_names(column_names1, ExpectedStruct.sheet_1_columns)

        unit_check = self.read_columns(1, sheets_data["Sheet1"])
        
        self.check_units(unit_check, column_names1)

        self.write_results()


    def write_results(self):
        """
        Write the results of the issue tracker class to a text file
        """
        with open("output.txt", "w") as f:
            for i in self.issues.__dict__:
                f.write(i+": "+str(self.issues.__dict__[i])+"\n")
            f.close()

