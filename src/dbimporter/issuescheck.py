import pandas as pd
import json
import sys
from enum import Enum
from dbimporter.expecteddata import ExpectedStruct
from typing import List
from dbimporter.logger import logger

class Issues():

    def __init__(self,
                 #expected_structure = None,
                 sheet_names: bool = None,
                 sheet1_columns: bool = None,
                 units: bool = None,
                 missing_units: dict = None,):
        
        #self.expected_structure = expected_structure
        self.sheet_names = sheet_names
        self.sheet1_columns = sheet1_columns
        self.units = units
        self.missing_units = missing_units

    def sheet_name(self):
        print("I'm in sheet name")
        #if self.sheet_names == True:
        if self.sheet_names is True:
            self.printing("sheet_name")
            return None
        else:
            return None

    def sheet1_column(self):
        print("I'm in sheet1 column")
        if self.sheet1_columns is True:
            self.printing("sheet1_column")
            return None
        else:
            return None
        
    def unit(self):
        print("I'm in unit")
        if self.units is True:
            self.printing("units")
            return None
        else:
            return None

    def missing_unit(self):
        print(f"missing units are {self.missing_units}")
        
    def printing(self, subject):
        print(f"Trying to fix {subject}")

    def check_self_beta(self, headers, data):
        self.sheet_name()
        self.sheet1_column()
        self.unit()
        self.missing_unit()

    def check_self(self, headers, data):
        return None
         
    def check_sheets(self, 
                     sheet_names: list,
                     expected_structure):

        """
        Check if the sheets are the expected names, and mark as true if correct


        Parameters
        ----------

            sheet_names: list
                Names of the sheets of an excel file
        """

        if sheet_names == expected_structure.sheet_names:
            self.sheet_names = True
        elif sheet_names != expected_structure.sheet_names:
            logger.warning(f"Sheet name incorrect, expected {expected_structure.sheet_names}. got {sheet_names}")
            self.sheet_names = False
        else:
            logger.error("Sheets name check could not be determined")
            self.sheet_names = False

    def check_column_names(self, 
                        real_column_names: list, 
                        expected_column_names: list, 
                        sheet_name: str):


        """
        Check if the columns are the expected names, and specifiy missing or unexpected column
        checks box if correct,
        does not account for the order of columns


        Parameters
        ----------

            real_column_names: list
                The column names found in the specified sheet
            expected_column_names: list
                The column names that are expected to be in the df
            sheet_name: str
                The name of the sheet being looked at

        """

        if sorted(real_column_names) == sorted(expected_column_names):
            self.sheet1_columns = True
            logger.info(f"Column names correct for sheet {sheet_name}")
        elif sorted(real_column_names) != sorted(expected_column_names):
            self.sheet1_columns = False
            logger.warning(f"Column names incorrect in sheet {sheet_name}, expected {expected_column_names}, got {real_column_names}")
            unique_to_real = set(real_column_names) - set(expected_column_names)
            unique_to_expected = set(expected_column_names) - set(real_column_names)
            if len(unique_to_real) > 0:
                logger.error(f"The {unique_to_real} column not expected in {sheet_name}, but was found")
            if len(unique_to_expected) > 0:
                logger.warning(f"The {unique_to_expected} column expected in {sheet_name}, but wasn't found")
        else:
            logger.error("Column name check could not be determined")
            self.sheet1_columns = False

    def check_units_nan(self, 
                    columnname: str, 
                    unitlist: list, 
                    sheet_name: str):

        """
        Check if there are any nan units, checks box if there are none


        Parameters
        ----------

            columnname: str
                Names of the columns to look for look for units for
            unitlist: list
                The units that that are expected to be in the df
            sheet_name: str
                The name of the sheet being looked at

        """

        checknan = False

        checknan_list = pd.Series(unitlist).isnull()

        no_units = []

        for i in range(len(checknan_list)):
            if checknan_list[i] == True:
                checknan = True
                wrong_column = columnname[i]
                no_units.append(wrong_column)
                error_msg = f"The column {wrong_column} in sheet {sheet_name} has no units"
                logger.error(error_msg)
                self.missing_units = no_units
            else:
                continue

        #self.issues.missing_units = no_units

        if checknan is True:
            self.units = False
        elif checknan is False:
            self.units = True
        else:
            logger.error("Unit existence check could not be determined")
            self.units = False