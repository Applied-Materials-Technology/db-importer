
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
        #if self.sheet_names == True:
        if self.sheet_names is True:
            self.printing()
            return None
        else:
            return None

    def sheet1_column(self):
        print("I'm in sheet1 column")
        if self.sheet1_columns is True:
            self.printing()
            return None
        else:
            return None
        
    def unit(self):
        print("I'm in unit")
        if self.units is True:
            self.printing()
            #return None
        else:
            #return None
            pass
        
    def printing(self):
        print("I'm fixing something")

    def check_self_beta(self, headers, data):
        self.sheet_name()
        self.sheet1_column()
        self.unit()
        print("hello")

    def check_self(self, headers, data):
        return None
        
    """
    def fix_units(self, headers, data):
        print("func started")
        units = dbi.restructure.get_units(headers)
        print("ran line 1")
        new_df = dbi.restructure.write_units(headers, data, units)
        print("ran line 2")
        dbi.restructure.write_new_data(new_df)
        print("ran line 3")

    def check_self(self, headers, data):
        self.fix_units(headers, data)"""
        