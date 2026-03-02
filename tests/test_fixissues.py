import pytest
import dbimporter as dbi

testdata = [(10, 10),
            (20, 20),]

errordata = [(1, ValueError),
                ("10", ValueError)]


def test_default_consoleloglevel(monkeypatch):

    monkeypatch.setattr('builtins.input', lambda _: "N")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert check.console_loglevel == 0

def test_make_newfile(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "N")
    check = dbi.check_structure.Check(filename="src/dbimporter/data/baddata.xlsx")
    assert check.console_loglevel == 0

