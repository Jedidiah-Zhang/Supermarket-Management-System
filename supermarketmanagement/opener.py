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
from supermarketmanagement import sale_window, login_window, \
    stock_window, selection_window, registration_window, input_window
from main import t


class SelectionFactory:
    def __new__(cls, Authorization, username):
        if Authorization:
            root_window = tk.Tk()
            root_window.title(t("Select"))
            root_window.resizable(False, False)
            selection_window.Admin(root_window, username)
            root_window.mainloop()
        else:
            root_window = tk.Tk()
            root_window.title(t("Select"))
            root_window.resizable(False, False)
            selection_window.Employee(root_window, username)
            root_window.mainloop()


class WindowFactory:
    def __new__(cls, window, username=None):
        if window == "Purchase":
            root_window = tk.Tk()
            root_window.title(t("Purchase"))
            root_window.geometry("840x600")
            root_window.resizable(False, False)
            input_window.Purchase(root_window, username)
            root_window.mainloop()
        elif window == "Inventory":
            root_window = tk.Tk()
            root_window.title(t("Stock Management"))
            root_window.geometry("1143x620")
            root_window.resizable(False, False)
            stock_window.StockManagement(root_window, username)
            root_window.mainloop()
        elif window == "Registration":
            root_window = tk.Tk()
            root_window.title(t("Registration"))
            root_window.geometry("700x380")
            root_window.resizable(False, False)
            registration_window.Registration(root_window, username)
            root_window.mainloop()
        elif window == "Cashier":
            root_window = tk.Tk()
            root_window.title(t("Cashier Interface"))
            root_window.geometry("1280x720")
            sale_window.SalespersonBase(root_window, username)
            root_window.mainloop()
        elif window == "Login":
            root_window = tk.Tk()
            root_window.title(t("Login"))
            x = 380
            y = 190
            w = root_window.winfo_screenwidth() / 2 - x / 2
            h = root_window.winfo_screenheight() / 2 - y / 2
            root_window.geometry("%dx%d+%d+%d" % (x, y, w, h))
            root_window.resizable(False, False)
            login_window.LoginWindow(root_window)
            root_window.mainloop()
