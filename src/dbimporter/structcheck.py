import pandas as pd
import json
import sys
import dbimporter.restructure as restructure
from dbimporter.logger import logger, change_logging_level
from dbimporter.expecteddata import ExpectedStruct
from dbimporter.issuetracker import Issues

class Check():

    def __init__(self,
                 filename: str = None,
                 console_loglevel: int = 0,
                 file_loglevel: int = 10,
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
        logging_list = [0,10,20,30,40,50,60]
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

        df = pd.ExcelFile(self.filename)

        self.check_sheets(df.sheet_names)
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

    def check_sheets(self, 
                     sheet_names: list):

        """
        Check if the sheets are the expected names, and mark as true if correct


        Parameters
        ----------

            sheet_names: list
                Names of the sheets of an excel file
        """

        if sheet_names == self.expected_structure.sheet_names:
            self.issues.sheet_names = True
        elif sheet_names != self.expected_structure.sheet_names:
            logger.warning(f"Sheet name incorrect, expected {self.expected_structure.sheet_names}. got {sheet_names}")
            self.issues.sheet_names = False
        else:
            logger.error("Sheets name check could not be determined")
            self.issues.sheet_names = False

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
            self.issues.sheet1_columns = True
            logger.info(f"Column names correct for sheet {sheet_name}")
        elif sorted(real_column_names) != sorted(expected_column_names):
            self.issues.sheet1_columns = False
            logger.warning(f"Column names incorrect in sheet {sheet_name}, expected {expected_column_names}, got {real_column_names}")
            unique_to_real = set(real_column_names) - set(expected_column_names)
            unique_to_expected = set(expected_column_names) - set(real_column_names)
            if len(unique_to_real) > 0:
                logger.error(f"The {unique_to_real} column not expected in {sheet_name}, but was found")
            if len(unique_to_expected) > 0:
                logger.warning(f"The {unique_to_expected} column expected in {sheet_name}, but wasn't found")
        else:
            logger.error("Column name check could not be determined")
            self.issues.sheet1_columns = False


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

        for i in range(len(checknan_list)):
            if checknan_list[i] == True:
                checknan = True
                wrong_column = columnname[i]
                error_msg = f"The column {wrong_column} in sheet {sheet_name} has no units"
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
            print(f"column names are {data_column_name}")
            expect_col_names = getattr(self.expected_structure, i)
            self.check_column_names(data_column_name, expect_col_names, i)

            try:
                unit_check = self.read_columns(1, sheets_data[i])
                self.check_units_nan(data_column_name, unit_check, i)
                unit_data = sheets_data[i].set_index(['Category'])
                units = [k for k in unit_data.xs("Unit")]
                print(units)
            except:
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
            json.dump(issue_dict, f2)
            

        self.output_message(sheet_names, sheets_data)

    def output_message(self, sheet_names, sheets_data):
        """
        Give results of check and ask to resolve issues
        """

        attrs = (getattr(self.issues, i) for i in self.issues.__dict__)

        if all(attrs) == False:
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
