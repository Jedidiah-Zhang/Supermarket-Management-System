#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/08/03 15:21
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : opener.py
@Software: PyCharm
"""

import tkinter as tk
from supermarcketmanagement import sale_window, login_window, \
    stock_window, selection_window, registration_window, input_window


class SelectionFactory:
    def __new__(cls, Authorization, username):
        if Authorization:
            root_window = tk.Tk()
            root_window.title(_("Select"))
            root_window.resizable(False, False)
            selection_window.Admin(root_window, username)
            root_window.mainloop()
        else:
            root_window = tk.Tk()
            root_window.title(_("Select"))
            root_window.resizable(False, False)
            selection_window.Employee(root_window, username)
            root_window.mainloop()


def login():
    root_window = tk.Tk()
    root_window.title(_("Login"))
    x = 380
    y = 190
    w = root_window.winfo_screenwidth() / 2 - x / 2
    h = root_window.winfo_screenheight() / 2 - y / 2
    root_window.geometry("%dx%d+%d+%d" % (x, y, w, h))
    root_window.resizable(False, False)
    login_window.LoginWindow(root_window)
    root_window.mainloop()


def sale(username):
    root_window = tk.Tk()
    root_window.title(_("Cashier Interface"))
    root_window.geometry("1280x720")
    sale_window.SalespersonBase(root_window, username)
    root_window.mainloop()


def stock(username):
    root_window = tk.Tk()
    root_window.title(_("Stock Management"))
    root_window.geometry("1143x620")
    root_window.resizable(False, False)
    stock_window.StockManagement(root_window, username)
    root_window.mainloop()


def reg(username):
    root_window = tk.Tk()
    root_window.title(_("Registration"))
    root_window.geometry("700x380")
    root_window.resizable(False, False)
    registration_window.Registration(root_window, username)
    root_window.mainloop()


def purchase(username):
    root_window = tk.Tk()
    root_window.title(_("Purchase"))
    root_window.geometry("840x600")
    root_window.resizable(False, False)
    input_window.Purchase(root_window, username)
    root_window.mainloop()
