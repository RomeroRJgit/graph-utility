from tkinter import *

from tkinter import ttk


def on_quit(root):
    pass


pages = {}


def open_page(root, page):
    for p in pages.values():
        p.pack_forget()

    page.pack()

    # root.columnconfigure(0, weight=1)
    # root.rowconfigure(0, weight=1)

class Page(ttk.Frame):
    def __init__(self, master=None, theme=None, **kw):
        super().__init__(master, **kw)
        self.root = master
        self.theme = theme

    def initialize(self):
        open_page(page=pages['menu'])
        self.root.protocol('WM_DELETE_WINDOW', lambda: on_quit(self.root))
        self.root.mainloop()

    def create(self):
        pass
