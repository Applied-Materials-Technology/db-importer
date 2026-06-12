import dbimporter as dbi


#dbi.check_structure.Check(filename="src/dbimporter/data/find_unit_test.xlsx", automatic_start=True)

dbi.check_structure.Check(filename="src/dbimporter/data/Rod #8- 3.4.2-10%-test data at cryo -75C.xlsx", file_type = "cryotensile")
