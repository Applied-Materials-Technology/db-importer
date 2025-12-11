import pandas as pd
import json
import sys
from enum import Enum
from dbimporter.logger import logger, change_logging_level
from dbimporter.expecteddata import ExpectedStruct
from typing import List
from dbimporter.issuescheck import Issues
        
class Check():

    def __init__(self,
                 filename: str = None,
                 console_loglevel: int | str = 0,
                 file_loglevel: int | str = 10,
                 no_restructure: bool = False,
                 issues = Issues(),
                 expected_structure = ExpectedStruct()):
        
        self.filename = filename
        self.console_loglevel = self.loglevelcheck(console_loglevel)
        self.file_loglevel = self.loglevelcheck(file_loglevel)
        self.no_restructure = no_restructure
        self.issues = issues
        self.expected_structure = expected_structure

        if self.file_loglevel > 30:
            print("Log file must be set to severity threshold 30 or lower")
            sys.exit()

        self.start(self.filename)

    def loglevelcheck(self, loglevel):
        #eventually allow for word levels...
        logging_list = [0,10,20,30,40,50,60,
                        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if loglevel not in logging_list:
            print("logging level must be a valid level")
            raise Exception(ValueError)
            sys.exit()
        return loglevel

    def read_data(self, 
                  filename: str):

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

        if self.filename.lower().endswith('.csv'):
            #df = pd.read_csv(self.filename, on_bad_lines='skip')
            #will eventually read csv...
            pass
        elif self.filename.lower().endswith('.xlsx'):
            df = pd.ExcelFile(self.filename)

        self.issues.check_sheets(df.sheet_names, self.expected_structure)
        sheets = {}
        sheet_names = df.sheet_names
        for i in sheet_names:
            sheets[i] = df.parse(i)

        return sheet_names, sheets

    def read_columns(self, 
                     location: str, 
                     sheet_data: pd.core.frame.DataFrame):

        """
        Read the name of the columns in a given sheet


        Parameters
        ----------

            location: int
                Integer position to read from df with iloc
            sheet_data: pandas.core.frame.DataFrame
                The data from the given sheet

        Returns
        -------

            columnlist : list
                A list of the column names from a given sheet
        """

        columnnames = sheet_data.iloc[location]
        columnlist = []
        for i in columnnames:
            columnlist.append(i)

        return columnlist

    def start(self, 
              filename: str):

        """
        Runs the checking methods on the excel file


        Parameters
        ----------

            filename: str
                Path to excel file to be checked for importing
        """

        change_logging_level(self.console_loglevel, self.file_loglevel)

        sheet_names, sheets_data = self.read_data(filename)

        for i in sheet_names:         

            data_column_name = self.read_columns(0, sheets_data[i])
            expect_col_names = getattr(self.expected_structure, i)
            self.issues.check_column_names(data_column_name, expect_col_names, i)

            try:
                unit_check = self.read_columns(1, sheets_data[i])
                self.issues.check_units_nan(data_column_name, unit_check, i)
                unit_data = sheets_data[i].set_index(['Category'])
                units = [k for k in unit_data.xs("Unit")]
            except (IndexError, KeyError): # may need to capture more errors...
                logger.error(f"Units could not be found in sheet {i}")

        self.write_results(sheet_names, sheets_data)


    def write_results(self, sheet_names, sheets_data):
        """
        Write the results of the issue tracker class to a text file
        """

        with open("output.txt", "w") as f:
            for i in self.issues.__dict__:
                f.write(i+": "+str(self.issues.__dict__[i])+"\n")
            f.close()

        with open("output.json", "w") as f2:
            issue_dict = {}
            for i in self.issues.__dict__:
                issue_dict[i] = self.issues.__dict__[i]
            print(issue_dict)
            json.dump(issue_dict, f2)
            

        self.output_message(sheet_names, sheets_data)

    def output_message(self, sheet_names, sheets_data):
        """
        Give results of check and ask to resolve issues
        """

        attrs = (getattr(self.issues, i) for i in self.issues.__dict__)

        if all(attrs) is False:
            print("******* output.txt generated for overview results *******")
            print("******* See example.log for details about report *******")

            try_restructure = input("Attempt to resolve issue automatically?")
            if try_restructure.upper() == "Y":
                print("******* Attempting to resolve issues automatically... *******")
                self.issues.check_self_beta(sheet_names, sheets_data)
                self.issues.check_self(sheet_names, sheets_data)
            else:
                pass
        
            #if failed:
            print("******* Could not resolve... *******")#fake
            print("Please correct issues manually and try again")
        else:
            print("No issues found")
            print("May proceed to ingestion attempt")
