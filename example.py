import dbimporter as dbi
from pathlib import Path


dbi.check_structure.Check(filename="src/dbimporter/data/find_unit_test.xlsx")
#dbi.issuescheck.fix_file(filename="src/dbimporter/data/find_unit_test.xlsx", issuesfile="output.json")


