import os

import pytest

from dbimporter.fix_structure.default import Default
from dbimporter.fix_structure.tensile import Tensile


class TestDefaultSetUpFile:
    """Tests for Default.set_up_file filename handling when output exists.

    Covers the behaviour where the user can type a new filename or leave it
    blank (to overwrite) without having to confirm with "yes" first.
    """

    def test_no_prompt_when_file_does_not_exist(self, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", lambda _: False)

        prompt_called = []

        def fake_prompt(msg):
            prompt_called.append(msg)
            return "ignored.xlsx"

        fixer = Default(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert prompt_called == []
        assert fixer.new_filename == "output_fixed.xlsx"

    def test_new_filename_used_when_provided(self, monkeypatch):
        call_count = [0]

        def fake_isfile(path):
            call_count[0] += 1
            # First call: output exists -> prompt for a new name.
            # Second call (recursion): the new name does not exist -> stop.
            return call_count[0] == 1

        monkeypatch.setattr(os.path, "isfile", fake_isfile)

        def fake_prompt(msg):
            return "custom_name"

        fixer = Default(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "custom_name.xlsx"

    def test_new_filename_keeps_xlsx_extension(self, monkeypatch):
        call_count = [0]

        def fake_isfile(path):
            call_count[0] += 1
            return call_count[0] == 1

        monkeypatch.setattr(os.path, "isfile", fake_isfile)

        def fake_prompt(msg):
            return "custom_name.xlsx"

        fixer = Default(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "custom_name.xlsx"

    def test_blank_keeps_current_filename(self, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", lambda _: True)

        def fake_prompt(msg):
            return ""

        fixer = Default(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "output_fixed.xlsx"

    def test_cancel_none_keeps_current_filename(self, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", lambda _: True)

        def fake_prompt(msg):
            return None

        fixer = Default(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "output_fixed.xlsx"

    def test_whitespace_keeps_current_filename(self, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", lambda _: True)

        def fake_prompt(msg):
            return "   "

        fixer = Default(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "output_fixed.xlsx"


class TestTensileSetUpFile:
    """Tests for Tensile.set_up_file filename handling (mirrors Default)."""

    def test_no_prompt_when_file_does_not_exist(self, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", lambda _: False)

        prompt_called = []

        def fake_prompt(msg):
            prompt_called.append(msg)
            return "ignored.xlsx"

        fixer = Tensile(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert prompt_called == []
        assert fixer.new_filename == "output_fixed.xlsx"

    def test_new_filename_used_when_provided(self, monkeypatch):
        call_count = [0]

        def fake_isfile(path):
            call_count[0] += 1
            return call_count[0] == 1

        monkeypatch.setattr(os.path, "isfile", fake_isfile)

        def fake_prompt(msg):
            return "custom_name"

        fixer = Tensile(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "custom_name.xlsx"

    def test_blank_keeps_current_filename(self, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", lambda _: True)

        def fake_prompt(msg):
            return ""

        fixer = Tensile(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "output_fixed.xlsx"

    def test_cancel_none_keeps_current_filename(self, monkeypatch):
        monkeypatch.setattr(os.path, "isfile", lambda _: True)

        def fake_prompt(msg):
            return None

        fixer = Tensile(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
        fixer.set_up_file(prompt_func=fake_prompt)

        assert fixer.new_filename == "output_fixed.xlsx"


@pytest.mark.parametrize("fixer_cls", [Default, Tensile])
def test_prompt_message_mentions_overwrite(fixer_cls, monkeypatch):
    """The prompt should tell the user blank means overwrite, not require 'yes'."""
    monkeypatch.setattr(os.path, "isfile", lambda _: True)

    captured = {}

    def fake_prompt(msg):
        captured["message"] = msg
        return ""

    fixer = fixer_cls(filename="somefile.xlsx", new_filename="output_fixed.xlsx")
    fixer.set_up_file(prompt_func=fake_prompt)

    assert "overwrite" in captured["message"].lower()
    assert "blank" in captured["message"].lower()
    assert "yes" not in captured["message"].lower()
