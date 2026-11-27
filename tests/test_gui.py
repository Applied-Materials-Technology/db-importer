from __future__ import annotations

import builtins
import sys
import types
import unittest.mock as mock

import pytest

import dbimporter as dbi
import gui as dbigui

# ---------------------------------------------------------------------------
# tkinter stubs (must be installed before importing gui)
# ---------------------------------------------------------------------------

class _BaseWidget:
    def __init__(self, *args, **kwargs):
        pass
    def pack(self, *args, **kwargs):
        return self
    def grid(self, *args, **kwargs):
        return self
    def configure(self, *args, **kwargs):
        return self
    config = configure
    def bind(self, *args, **kwargs):
        return self
    def tkraise(self, *args, **kwargs):
        return self
    def yview(self, *args, **kwargs):
        return self
    def geometry(self, *args, **kwargs):
        return self
    def mainloop(self, *args, **kwargs):
        return self


class Tk(_BaseWidget): pass
class Frame(_BaseWidget): pass
class Canvas(_BaseWidget): pass
class Text(_BaseWidget): pass
class Scrollbar(_BaseWidget):
    def set(self, *args, **kwargs):
        return self
class Label(_BaseWidget): pass
class Button(_BaseWidget): pass

NORMAL = "normal"
DISABLED = "disabled"
END = "end"
WORD = "word"
LEFT = "left"
RIGHT = "right"
BOTH = "both"
Y = "y"
X = "x"
NW = "nw"
NS = "ns"
NSEW = "nsew"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"

tk_mod = types.ModuleType("tkinter")
for _name in [
    "Tk", "Frame", "Canvas", "Text", "Scrollbar", "Label", "Button",
    "NORMAL", "DISABLED", "END", "WORD", "LEFT", "RIGHT", "BOTH",
    "Y", "X", "NW", "NS", "NSEW", "VERTICAL", "HORIZONTAL",
]:
    setattr(tk_mod, _name, eval(_name))

ttk_mod = types.ModuleType("tkinter.ttk")
ttk_mod.Scrollbar = Scrollbar
ttk_mod.Label = Label
ttk_mod.Button = Button

filedialog_mod = types.ModuleType("tkinter.filedialog")
filedialog_mod.askopenfilename = lambda *a, **k: None

messagebox_mod = types.ModuleType("tkinter.messagebox")
messagebox_mod.showerror = lambda *a, **k: None
messagebox_mod.showinfo = lambda *a, **k: None

simpledialog_mod = types.ModuleType("tkinter.simpledialog")
simpledialog_mod.askstring = lambda *a, **k: None

scrolledtext_mod = types.ModuleType("tkinter.scrolledtext")

sys.modules["tkinter"] = tk_mod
sys.modules["tkinter.ttk"] = ttk_mod
sys.modules["tkinter.filedialog"] = filedialog_mod
sys.modules["tkinter.messagebox"] = messagebox_mod
sys.modules["tkinter.simpledialog"] = simpledialog_mod
sys.modules["tkinter.scrolledtext"] = scrolledtext_mod
