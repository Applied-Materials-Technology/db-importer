import pandas as pd
import json
import sys
from dbimporter.logger import logger, change_logging_level, set_log_formatter
from typing import List
from dbimporter.issuescheck import Issues
from dbimporter.fix_structure import Default
from dbimporter.printing import Printer
from dataset import structpaths

printer = Printer()

class Check():

    """
        Check the file

        Parameters
        -------

            filename : str
                The name of the json file that contains the expected data structure
                for the provided file
            console_loglevel: int | str
                Lowest level of logs to display in the console
                Defaults to 0 (show all logs)
            file_loglevel: int | str
                Lowest level of logs to write to the log file
                Defaults to 10 (Write all logs)
            no_restructure: bool
                Turn off asking attempts to restructure files that failed checks
                Defaults to False
            issues
                Class that checks issues and stores default
            file_type
                Name of the file type
            expected_json
                Structure info about specific file type specified
            no_log_colour: bool
                Turn off colouring of logs in console.
                Defaults to False
            automatic_start: bool
                Whether the checker runs after the Checker has been created

    """

    def __init__(self,
                 filename: str = None,
                 console_loglevel: int | str = 0,
                 file_loglevel: int | str = 10,
                 no_restructure: bool = False,
                 issues = None,
                 file_type = None,
                 expected_json = None,
                 no_log_colour: bool = False,
                 automatic_start: bool = False):
        
        self.filename = filename
        self.console_loglevel = self.loglevelcheck(console_loglevel)
        self.file_loglevel = self.loglevelcheck(file_loglevel)
        self.no_restructure = no_restructure
        self.issues = issues
        self.file_type = file_type
        self.expected_json = expected_json
        self.no_log_colour = no_log_colour
        self.automatic_start = automatic_start

        if self.no_log_colour is True:
            set_log_formatter()

        if self.issues == None:
            self.issues = Issues(general_output="my_output.json")

        if self.expected_json is None:
            filename, expected_json = self.get_expected_json()
            self.expected_json = expected_json
            logger.warning(f"json has been set as {self.expected_json}")

        if self.file_loglevel > 30:
            logger.error("Log file must be set to severity threshold 30 or lower, setting to 30")
            self.file_loglevel = 30

        if self.issues.output_type is None:
            self.issues.output_type = Default(filename=self.filename)

        if self.automatic_start == True:
            self.start(self.filename)


    def get_expected_json(self):


        """
        Chooses the associated json settings for the file type provided.

        Returns
        -------

            filename : Path
                The name of the json file that contains the expected data structure
                for the provided file
            json_data : dict
                The data from the settings json file
        """

        if self.file_type == None:
            logger.warning(f"file structure not set, defaulting to option BADDATA")
            filename = structpaths.Jsonfile.BADDATA.value
        elif self.file_type == "one":
            filename = structpaths.Jsonfile.FILE1.value
        elif self.file_type == "two":
            filename = structpaths.Jsonfile.FILE2.value
        elif self.file_type == "baddata":
            filename = structpaths.Jsonfile.BADDATA.value
        elif self.file_type == "tensiledata":
            filename = structpaths.Jsonfile.TENSILEDATA.value
        else:
            logger.warning(f"file structure could not be determined, defaulting to option BADDATA")
            filename = structpaths.Jsonfile.BADDATA.value

        try:
            with open(filename) as file:
                json_data = json.load(file)
        except:
            logger.error(f"Json file {filename} could not be opened")
            json_data = None
            
        return filename, json_data


    def loglevelcheck(self, 
                      loglevel: int | str):

        """
        Checks if the logging level set by the user is valid level. Returns this value
        if valid, and returns a default value if it is not.

        Parameters
        ----------

            loglevel: int | str
                The logging level specified by the user

        Returns
        -------

            loglevel : int | str
                A logging level that has been verified to be a valid logging
                level
        """

        logging_list = [0,10,20,30,40,50,60,
                        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        if loglevel not in logging_list:
            logger.error(f"Logger must be a valid logging level, defaulting to 40")
            loglevel = 40

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
            df = pd.read_csv(self.filename, on_bad_lines='skip')
        elif self.filename.lower().endswith('.xlsx'):
            df = pd.ExcelFile(self.filename)

        try:
            self.issues.check_sheets(df.sheet_names, self.expected_json)
            sheets = {}
            sheet_names = df.sheet_names
            for i in sheet_names:
                sheets[i] = df.parse(i)
        except AttributeError:
            logger.info("File format has no sheets")
            sheet_names = [self.filename]
            sheets = {self.filename: df}

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

            try:
                expect_col_names = self.expected_json[i]
            except AttributeError:
                logger.debug(f"still in testing mode: sheet names have no associated data")
                expect_col_names = ["Entry", "Material", "Heat", "Product", "Sub-product", "Test_Lab", "Specimen ID", "Internal ID"]

            self.issues.check_column_names(data_column_name, expect_col_names, i)

            try:
                unit_check = self.read_columns(1, sheets_data[i])
                self.issues.check_units_nan(data_column_name, unit_check, i)
                unit_data = sheets_data[i].set_index(['Category'])
                units = [k for k in unit_data.xs("Unit")]
            except (IndexError, KeyError): # may need to capture more errors...
                logger.error(f"Units could not be found in sheet {i}")

        self.write_results(sheet_names, sheets_data)


    def write_results(self, 
                      sheet_names: dict, 
                      sheets_data: pd.core.frame.DataFrame):
        
        """

        Write the results of the issue tracker class to a text file

        Parameters
        ----------

            sheet_names: dict
                Path to excel file to be checked for importing
            sheets_data: pd.core.frame.DataFrame
                Path to excel file to be checked for importing

                            sheet_names : list
                A list of the sheet names from the file being read
            sheets : dict
                A dictionary of the sheet_names and the pandas dataframe parsed from those sheets
        """

        with open("output.txt", "w") as f:
            for i in self.issues.__dict__:
                f.write(i+": "+str(self.issues.__dict__[i])+"\n")
            f.close()

        with open("output.json", "w") as f2:
            issue_dict = {}
            for i in self.issues.__dict__:
                if i != "output_type":
                    issue_dict[i] = self.issues.__dict__[i]
                else:
                    pass
            json.dump(issue_dict, f2)
            

        self.output_message(sheet_names, sheets_data)


    def output_message(self, 
                       sheet_names: dict, 
                       sheets_data: pd.core.frame.DataFrame):
        
        """
        Give results of check and ask to resolve issues
        """

        attrs = (getattr(self.issues, i) for i in self.issues.__dict__)

        if all(attrs) is False:
            printer.wrap_text_star("output.txt generated for overview results")
            printer.wrap_text_star("See example.log for details about report")

            try_restructure = input("Attempt to resolve issue automatically?")
            if try_restructure.upper() == "Y":
                printer.wrap_text_star("Attempting to resolve issues automatically...")
                self.issues.check_self(sheet_names, sheets_data, self.filename)
            else:
                pass

            new_attrs = (getattr(self.issues, i) for i in self.issues.__dict__)

            if all(new_attrs) is False:
                #if failed:
                printer.wrap_text_star("Could not resolve...")
                if try_restructure.upper() == "Y":
                    print(f"See resolution attempt at {self.issues.output_type.new_filename}")
                print("Please correct issues manually and try again")
        else:
            print("No issues found")
            print("May proceed to ingestion attempt")
