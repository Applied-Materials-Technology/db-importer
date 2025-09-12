class Issues():

    def __init__(self,
                sheet_names: bool = None,
                sheet1_columns: bool = None):
        
        self.sheet_names = sheet_names
        self.sheet1_columns = sheet1_columns

    def sheet_name(self):
        print(self.sheet_names)

        