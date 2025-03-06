#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/09/10 10:18
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : selection_window.py
@Software: PyCharm
"""


from main import *


class Admin:
    def __init__(self, master, username):
        self.master = master
        self.username = username

        reg_button = tk.Button(self.master, width=15, text=t("Registration"), font=(FONT, 20),
                               command=self.__open_reg)
        stock_button = tk.Button(self.master, width=15, text=t("Inventory"), font=(FONT, 20),
                                 command=self.__open_stock)

        reg_button.pack()
        stock_button.pack()

    def __open_stock(self):
        self.master.destroy()
        opener.WindowFactory("Inventory", self.username)

    def __open_reg(self):
        self.master.destroy()
        opener.WindowFactory("Registration", self.username)


class Employee:
    def __init__(self, master, username):
        self.master = master
        self.username = username

        purchase_button = tk.Button(self.master, width=15, text=t("Purchase"), font=(FONT, 20),
                                    command=self.__open_input)
        cashier_button = tk.Button(self.master, width=15, text=t("Cashier"), font=(FONT, 20),
                                   command=self.__open_sale)

        purchase_button.pack()
        cashier_button.pack()

    def __open_sale(self):
        self.master.destroy()
        opener.WindowFactory("Cashier", self.username)

    def __open_input(self):
        self.master.destroy()
        opener.WindowFactory("Purchase", self.username)
