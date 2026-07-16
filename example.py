import dbimporter as dbi
import gui as dbigui


dbi.check_structure.Check(filename="src/dbimporter/data/find_unit_test.xlsx", 
                          file_type = "default",
                          automatic_start=True)

#dbi.check_structure.Check(filename="src/dbimporter/data/Rod #8- 3.4.2-10%-test data at cryo -75C.xlsx", file_type = "cryotensile")

# sheetnames, sheets = dbi.graph_extract.read_data(filename="src/dbimporter/data/Rod #8- 3.4.2-10%-test data at cryo -75C.xlsx")
# sheetdata = sheets[sheetnames[0]]

# print(sheetdata.head(3))

