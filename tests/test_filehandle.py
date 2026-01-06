import pytest
import dbimporter as dbi

def test_find_module():

    """
    Check module can be found
    """

    modulefound = dbi.find_me()
    #assert modulefound == True
    assert modulefound


def test_filename_exists(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert hasattr(check, "filename")

def test_console_loglevel_exists(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert hasattr(check, "console_loglevel")

def test_file_loglevel_exists(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert hasattr(check, "file_loglevel")

def test_issues_exists(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert hasattr(check, "issues")

def test_expected_structure_exists(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert hasattr(check, "expected_structure")

#########################################################################################   

testdata = [(10, 10),
            (20, 20),]

errordata = [(1, ValueError),
                ("10", ValueError)]


def test_default_consoleloglevel(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert check.console_loglevel == 0

def test_default_fileloglevel(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert check.file_loglevel == 10

@pytest.mark.parametrize("x ,expected", testdata)
def test_change_consolelogpass(monkeypatch, x, expected):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx", console_loglevel = x)
    assert check.console_loglevel == expected

@pytest.mark.xfail(strict=True)
@pytest.mark.parametrize("x ,expected", errordata)
def test_change_consolelogfail(monkeypatch, x, expected):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx", console_loglevel = x)
    assert check.console_loglevel == expected


@pytest.mark.parametrize("x ,expected", testdata)
def test_change_filelogpass(monkeypatch, x, expected):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx", file_loglevel = x)
    assert check.file_loglevel == expected

@pytest.mark.xfail(strict=True)
@pytest.mark.parametrize("x ,expected", errordata)
def test_change_filelogfail(monkeypatch, x, expected):
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx", file_loglevel = x)
    assert check.file_log_level == expected