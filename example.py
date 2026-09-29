import dbimporter as dbi
import gui as dbigui


dbi.check_structure.Check(filename="src/dbimporter/data/find_unit_test.xlsx", 
                          file_type = "default",
                          automatic_start=True)

# dbigui.start_gui()
