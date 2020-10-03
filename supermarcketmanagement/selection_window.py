#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/09/10 10:18
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : selection_window.py
@Software: PyCharm
"""

import tkinter as tk
from supermarcketmanagement import opener
import main

FONT = main.FONT


class Admin:
    def __init__(self, master, username):
        reg_button = tk.Button(master,
                               width=15,
                               text=_("Registration"),
                               font=(FONT, 20),
                               command=lambda: self.__open_reg(master, username))

        stock_button = tk.Button(master,
                                 width=15,
                                 text=_("Inventory"),
                                 font=(FONT, 20),
                                 command=lambda: self.__open_stock(master, username))

        reg_button.pack()
        stock_button.pack()

    @staticmethod
    def __open_stock(master, username):
        master.destroy()
        opener.stock(username)

    @staticmethod
    def __open_reg(master, username):
        master.destroy()
        opener.reg(username)


class Employee:
    def __init__(self, master, username):
        purchase_button = tk.Button(master,
                                    width=15,
                                    text=_("Purchase"),
                                    font=(FONT, 20),
                                    command=lambda: self.__open_input(master, username))

        cashier_button = tk.Button(master,
                                   width=15,
                                   text=_("Cashier"),
                                   font=(FONT, 20),
                                   command=lambda: self.__open_sale(master, username))

        purchase_button.pack()
        cashier_button.pack()

    @staticmethod
    def __open_sale(master, username):
        master.destroy()
        opener.sale(username)

    @staticmethod
    def __open_input(master, username):
        master.destroy()
        opener.purchase(username)
