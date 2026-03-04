import pandas as pd
import json
import sys
import os 
from enum import Enum
from pathlib import Path
from typing import List
from dbimporter.logger import logger

class Issues():

    def __init__(self,
                 output_type = None,
                 sheet_names: bool = None,
                 sheet1_columns: bool = None,
                 units: bool = None,
                 missing_units: dict = None,
                 file_overwrite: bool = False):
        
        self.output_type = output_type
        self.sheet_names = sheet_names
        self.sheet1_columns = sheet1_columns
        self.units = units
        self.missing_units = missing_units
        self.file_overwrite = file_overwrite


    def sheet_name(self):

        try:
            if self.sheet_names is True:
                self.printing_subject("sheet names")
                self.output_type.start_sheet_name()
                self.file_overwrite = True # change: read and make changes to new file from now

                return None
            else:
                return None
            
        except:
            logger.warning("Could not automatically fix sheet names")

            return None


    def sheet1_column(self):

        try:
            if self.sheet1_columns is True:
                self.printing_subject("sheet1 columns")
                self.output_type.start_sheet1_column()
                self.file_overwrite = True # change: read and make changes to new file from now

                return None
            else:
                return None
        except:
            logger.warning("Could not automatically fix sheet 1 names")

            return None


    def unit(self):

        """
        Checks if any issue with the units was detected, and attempts to fix them with
        the unti fixer

        Returns
        -------

            loglevel : int | str
                A logging level that has been verified to be a valid logging
                level
        """

        try:
            if self.units is True:
                self.printing_subject("units")
                self.output_type.start_missing_units()
                self.file_overwrite = True # change: read and make changes to new file from now

                return None
            else:
                return None
            
        except:
            logger.warning("Could not automatically fix units")

            return None


    def printing_subject(self, 
                         subject):
        
        """
        Indicate to the use what is currently being restructered
        """

        print(f"Attempting to fix {subject}....")

    # def fix_file(self, 
    #              filename, 
    #              issuesfile):
        
    #     for i in issuesfile:
    #         print(i)


    def check_self(self,
                   headers,
                   data,
                   original_file):
        

        if self.output_type.new_filename is None:
            self.output_type.new_filename = Path("newfile.xlsx")

        self.output_type.set_up_file()

        self.sheet_name()
        self.sheet1_column()
        self.unit()

         
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

        expected_sheet_names = expected_structure["sheet_names"]

        if sheet_names == expected_sheet_names:
            self.sheet_names = True
        elif sheet_names != expected_sheet_names:
            logger.warning(f"Sheet name incorrect, expected {expected_sheet_names}, got {sheet_names}")
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

        if checknan is True:
            self.units = False
        elif checknan is False:
            self.units = True
        else:
            logger.error("Unit existence check could not be determined")
            self.units = False

def fix_file(filename, 
             issuesfile):
    
    """
    
        Start the process of fixing issues with an issues json


        Parameters
        ----------

            filename: Path
                The path to the file to be restructured
            issuesfile: Path
                The path to the file that has the issues information

    """
    
    try:
        with open(issuesfile) as myissues:
            issues_json = json.load(myissues)
    except:
        logger.error(f"Json file {filename} could not be opened")
        issues_json = None

    issues = Issues()
    issues.sheet_names = issues_json["sheet_names"]
    issues.sheet1_columns = issues_json["sheet1_columns"]
    issues.units = issues_json["units"]
    issues.missing_units = issues_json["missing_units"]


    if filename.lower().endswith('.csv'):
        df = pd.read_csv(filename, on_bad_lines='skip')
    elif filename.lower().endswith('.xlsx'):
        df = pd.ExcelFile(filename)

    try:
        sheets = {}
        sheet_names = df.sheet_names
        for i in sheet_names:
            sheets[i] = df.parse(i)
    except AttributeError:
        logger.info("File format has no sheets")
        sheet_names = [filename]
        sheets = {filename: df}

    issues.check_self(sheet_names, sheets, filename)