import pytest
import dbimporter as dbi
import pytest_mock

def test_find_module(mocker):
    modulefound = dbi.test()
    assert modulefound == True

"""
class TestClass:
    check = dbi.structcheck.Check(filename="src/dbimporter/data/baddata.xlsx")

    def test_filename_exists(self):
        assert hasattr(self.check, "filename")

    def test_console_loglevel_exists(self):
        assert hasattr(self.check, "console_loglevel")

    def test_file_loglevel_exists(self):
        assert hasattr(self.check, "file_loglevel")

    def test_issues_exists(self):
        assert hasattr(self.check, "issues")

    def test_expected_structure_exists(self):
        assert hasattr(self.check, "expected_structure")"""

