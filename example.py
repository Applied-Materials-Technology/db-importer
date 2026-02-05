
import dbimporter as dbi

#dbi.restructure.test()

#dbi.restructure.start(filename="src/dbimporter/data/find_unit_test.xlsx")

#dbi.write_units.start(filename="src/dbimporter/data/find_unit_test.xlsx")

#dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx", console_loglevel=40, file_type="baddata")

#dbi.check_structure.Check(filename="src/dbimporter/data/UKAEA Mini LCF Programe 0 point45 percent Strain Amp data_1.CSV", console_loglevel=40)

dbi.check_structure.Check(filename="src/dbimporter/data/find_unit_test.xlsx")
