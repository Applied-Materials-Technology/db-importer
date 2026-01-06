import json

class MyClass2:
    def __init__(self, x):
        self.x = x
    @staticmethod
    def preset_a():
        return MyClass2(1)
    @staticmethod
    def preset_b():
        return MyClass2(2)
    @staticmethod
    def preset_c_with_extend(extend):
        return MyClass2(3+extend)

    def __str__(self):
        return f"The value of x is {self.x}"
    

class ExpectedStruct2:

    sheet_names: list = ["Sheet1", "Sheet2", "Sheet3"]
    Sheet1: list = ["Entry", "Material", "Heat", "Product", "Sub-product", "Test_Lab", "Specimen ID", "Internal ID"]
    Sheet2: list = ['Test Row', 'Curve description', 'Name', 'Units', 'cycle number']
    Sheet3: list = ["Entry", "Material", "Heat", "Product", "Sub-product", "Test_Lab", "Specimen ID", "Internal ID"]

class ExpectedStruct:

    def __init__(self, 
                 x,
                 sheet_names,
                 Sheet1,
                 Sheet2,
                 Sheet3):
        
        self.x = x
        self.sheet_names = sheet_names
        self.Sheet1 = Sheet1
        self.Sheet2 = Sheet2
        self.Sheet3 = Sheet3

    # @staticmethod
    # def preset_a():
    #     return ExpectedStruct(1)

    
    # @staticmethod
    # def preset_b():
    #     return ExpectedStruct(2)
    
    # @staticmethod
    # def preset_c_with_extend(extend):
    #     return ExpectedStruct(3+extend)

    def print_sheets(self):
        print(f"Sheet names are {self.sheet_names}")


    def __str__(self):
        return f"The value of x is {self.x}"
    

with open("baddatatest.json") as file:
    json_data = json.load(file)

my_obj = ExpectedStruct(1,**json_data)
print(my_obj.sheet_names)
print(my_obj.Sheet1)