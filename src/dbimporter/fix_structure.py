import pandas as pd

class Default():

    def __init__(self,
                 filename = None,
                 two: bool = None):
        
        self.filename = filename
        self.two = two


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

        if filename.lower().endswith('.csv'):
            df = pd.read_csv(filename)
        elif filename.lower().endswith('.xlsx'):
            df = pd.ExcelFile(filename)
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

        #print(units)

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
        print(header_vals)

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

        with pd.ExcelWriter("test2.xlsx") as writer:
            data.to_excel(writer, sheet_name = sheet_name)

    def write_new_data(self,
                       data,
                       sheet_name):

        """
        Write the new dataframe to an exisiting Excel file

        Parameters
        ----------

            data: DataFrame
                The dataframe containing data of the excel file

        """

        try: 
            with pd.ExcelWriter("test2.xlsx", mode='a') as writer:
                data.to_excel(writer, sheet_name = sheet_name)
        except FileNotFoundError:
            self.create_new_excel(data, sheet_name)
        except ValueError:
            print("This file already exists...")


    def start(self,
              filename):

        print("STARTING RESTRUCTURE ATTEMPT")
        headers, data = self.read_data(filename)

        for i in data:
            try:
                print(i)
                my_data = data[i].set_index('Category')
                entry_info = my_data.loc["Entry"]
                units = self.get_units(entry_info)
                new_df = self.make_new_df(my_data, units)
                self.write_new_data(new_df, i)
            except KeyError:
                print("skipping sheet...")

    def test(self,
             custom_string="mydefault"):
        
        print(f"I am in default with {custom_string}")