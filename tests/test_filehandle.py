import pytest
import dbimporter as dbi
import pytest_mock

def test_find_module():

    """
    Check module can be found
    """

    modulefound = dbi.test()
    assert modulefound == True


class TestCheckAttrs:

    """
    Test correct attributes exist for Check object
    """

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
        assert hasattr(self.check, "expected_structure")

class TestCheckLogs:

    """
    Test the logger level settings
    """

    testdata = [(10, 10),
                (20, 20),]
    
    errordata = [(1, ValueError),
                 ("10", ValueError)]

    
    def test_default_consoleloglevel(self):
        check = dbi.structcheck.Check(filename="src/dbimporter/data/baddata.xlsx")
        assert check.console_loglevel == 0

    def test_default_fileloglevel(self):
        check = dbi.structcheck.Check(filename="src/dbimporter/data/baddata.xlsx")
        assert check.file_loglevel == 10

    @pytest.mark.parametrize("x ,expected", testdata)
    def test_change_consolelogpass(self, x, expected):
        check = dbi.structcheck.Check(filename="src/dbimporter/data/baddata.xlsx", console_loglevel = x)
        assert check.console_loglevel == expected

    @pytest.mark.xfail(strict=True)
    @pytest.mark.parametrize("x ,expected", errordata)
    def test_change_consolelogfail(self, x, expected):
        check = dbi.structcheck.Check(filename="src/dbimporter/data/baddata.xlsx", console_loglevel = x)


    @pytest.mark.parametrize("x ,expected", testdata)
    def test_change_filelogpass(self, x, expected):
        check = dbi.structcheck.Check(filename="src/dbimporter/data/baddata.xlsx", file_loglevel = x)
        assert check.file_loglevel == expected

    @pytest.mark.xfail(strict=True)
    @pytest.mark.parametrize("x ,expected", errordata)
    def test_change_filelogfail(self, x, expected):
        check = dbi.structcheck.Check(filename="src/dbimporter/data/baddata.xlsx", file_loglevel = x)





