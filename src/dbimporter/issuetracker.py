class Issues():

    def __init__(self,
                sheet_names: bool = None,
                sheet1_columns: bool = None,
                units: bool = None):
        
        self.sheet_names = sheet_names
        self.sheet1_columns = sheet1_columns
        self.units = units

    def sheet_name(self):
        print(self.sheet_names)

        