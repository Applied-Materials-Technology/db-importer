class Issues():

    def __init__(self,
                sheet_names: bool = None,
                sheet1_columns: bool = None,
                units: bool = None):
        
        self.sheet_names = sheet_names
        self.sheet1_columns = sheet1_columns
        self.units = units

    def sheet_name(self):
        print("I'm in sheet name")
        if self.sheet_names == True:
            self.printing()
            return None
        else:
            return None

    def sheet1_column(self):
        print("I'm in sheet1 column")
        if self.sheet1_columns == True:
            self.printing()
            return None
        else:
            return None
        
    def unit(self):
        print("I'm in unit")
        if self.units == True:
            self.printing()
            return None
        else:
            return None
        
    def printing(self):
        print("I'm fixing something")

    def check_self(self):
        self.sheet_name()
        self.sheet1_column()
        self.unit()
        print("hello")
        