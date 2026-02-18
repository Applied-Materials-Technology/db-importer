import pandas as pd
import os

class Default():

    def __init__(self,
                 filename = None,
                 new_filename: str = None):
        
        self.filename = filename
        self.new_filename = new_filename

        if self.new_filename == None:
            self.new_filename = "newfile.xlsx"
        


    def set_up_file(self):

        """
        Checks if the file name used to write the fixed structure to already exists. Warns
        user of overwriting existing data and allows the user to input an alternative filename
        """

        exists = os.path.isfile(self.new_filename)

        if not exists:
            pass
        else:
            change_filename = input(f"File {self.new_filename} already exists. Contents will be overwritten. Press Y to give alternative filename\n")
            if change_filename.upper() == "Y":
                print("******* Attempting to resolve issues automatically... *******")
                new_filename = input("Enter new filename")
                if new_filename[-5:] != ".xlsx":
                    new_filename = new_filename + ".xlsx"
                self.new_filename = new_filename
                self.set_up_file()
            else:
                pass


    def read_data(self):

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
            df = pd.read_csv(self.filename)
        elif self.filename.lower().endswith('.xlsx'):
            df = pd.ExcelFile(self.filename)
        sheets = {}
        sheet_names = df.sheet_names
        for i in sheet_names:
            sheets[i] = df.parse(i)

        return sheet_names, sheets


    def get_units(self,
                  headers):

        """
        Finds the units in the headers and return them

            Parameters
        ----------

            headers:
                Headers of the excel file being read

        Returns
        -------

            units : dict
                Dictionary of units from headers
        """

        units = {}

        for i in headers:
            try:
                start = i.index("(")+1
                end = i.index(")")

                unit = i[start:end]
                units[i] = unit
            except ValueError:
                units[i] = None

        return units


    def make_new_df(self,
                    old_df_data,
                    units):

        """
        Writes the units found for each column in the "Units" row

        Parameters
        ----------

            old_df_data : DataFrame
                The dataframe to write units to
            units : dict
                The units which have been obtained and their corresponding column

        Returns
        -------

            new_df : DataFrame
                Dataframe which now contains the units
        """
        
        new_data = old_df_data.values.tolist()
        index_vals = old_df_data.index.values
        header_vals = old_df_data.columns.values

        new_units = [units[i] for i in units]
        for i in range(len(new_data[1])):
            new_data[1][i] = new_units[i]
            new_data[0][i] = new_data[0][i].replace(f"({new_units[i]})","")



        new_df = pd.DataFrame(new_data)
        new_df.index = index_vals
        new_df.columns = header_vals

        return new_df


    def create_new_excel(self,
                         data, 
                         sheet_name):

        """
        Write the new dataframe to a file

        Parameters
        ----------

            data: DataFrame
                Write new dataframe to a new Excel file

        """

        with pd.ExcelWriter(self.new_filename) as writer:
            data.to_excel(writer, sheet_name = sheet_name)


    def write_new_data(self,
                       data,
                       sheet_name,
                       new_filename=None):

        """
        Write the new dataframe to an exisiting Excel file

        Parameters
        ----------

            data: DataFrame
                The dataframe containing data of the excel file

        """

        try: 
            with pd.ExcelWriter(self.new_filename, mode='a', if_sheet_exists="replace") as writer:
                data.to_excel(writer, sheet_name = sheet_name)
        except FileNotFoundError as e:
            print(f"{FileNotFoundError} {e}, creating new Excel file")
            self.create_new_excel(data, sheet_name)
        except ValueError as e:
            print(f"{ValueError} {e}")


    def start_units(self):
        
        print("STARTING RESTRUCTURE ATTEMPT")
        headers, data = self.read_data()

        for i in data:
            try:
                my_data = data[i].set_index('Category')
                entry_info = my_data.loc["Entry"]
                units = self.get_units(entry_info)
                new_df = self.make_new_df(my_data, units)
                self.write_new_data(new_df, i)
            except KeyError:
                print("skipping sheet...")

        return 


    def test(self,
             custom_string="mydefault"):
        
        print(f"I am in default with {custom_string}")