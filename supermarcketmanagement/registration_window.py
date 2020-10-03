#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/08/09 10:27
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : registration_window.py
@Software: PyCharm
"""

import tkinter as tk
from tkinter import messagebox
import main

CONFIG = main.CONFIG
DEFAULT = "Default"
CONNECTION = main.CONNECTION
CURSOR = main.CURSOR
CURSOR.execute("USE shop")


class Registration(main.SetMenu):
    def __init__(self, master, username):
        super().__init__(master, username)

        welcome_label = tk.Label(master,
                                 text=_("Registration"),
                                 font=(CONFIG["DEFAULT"]["font"], 20))
        first_name_label = tk.Label(master,
                                    text=_("First Name: "),
                                    font=(CONFIG["DEFAULT"]["font"], 14))
        last_name_label = tk.Label(master,
                                   text=_("Last Name: "),
                                   font=(CONFIG["DEFAULT"]["font"], 14))
        username_label = tk.Label(master,
                                  text=_("Username: "),
                                  font=(CONFIG["DEFAULT"]["font"], 14))
        address_label = tk.Label(master,
                                 text=_("Address: "),
                                 font=(CONFIG["DEFAULT"]["font"], 14))
        email_label = tk.Label(master,
                               text=_("Email: "),
                               font=(CONFIG["DEFAULT"]["font"], 14))

        self.first_name_entry = tk.Entry(master,
                                         width=50,
                                         bd=1,
                                         font=(CONFIG["DEFAULT"]["font"], 14))
        self.last_name_entry = tk.Entry(master,
                                        width=50,
                                        bd=1,
                                        font=(CONFIG["DEFAULT"]["font"], 14))
        self.username_entry = tk.Entry(master,
                                       width=50,
                                       bd=1,
                                       font=(CONFIG["DEFAULT"]["font"], 14))
        self.address_entry = tk.Entry(master,
                                      width=50,
                                      bd=1,
                                      font=(CONFIG["DEFAULT"]["font"], 14))
        self.email_entry = tk.Entry(master,
                                    width=50,
                                    bd=1,
                                    font=(CONFIG["DEFAULT"]["font"], 14))
        self.admin = tk.BooleanVar()
        self.admin.set(0)
        employee_radiobutton = tk.Radiobutton(master,
                                              text=_("Employee"),
                                              variable=self.admin,
                                              value=0)
        admin_radiobutton = tk.Radiobutton(master,
                                           text=_("Administration"),
                                           variable=self.admin,
                                           value=1)
        password_label = tk.Label(master,
                                  text=_("*Password will be set as default: ") + DEFAULT,
                                  font=(CONFIG["DEFAULT"]["font"], 12))
        confirm_button = tk.Button(master,
                                   text=_("Confirm"),
                                   width=15,
                                   font=(CONFIG["DEFAULT"]["font"], 14),
                                   command=self.__confirm)

        welcome_label.grid(row=0, column=0, padx=10, pady=10)
        first_name_label.grid(row=1, column=0, padx=20, pady=10, sticky="E")
        last_name_label.grid(row=2, column=0, padx=20, sticky="E")
        username_label.grid(row=3, column=0, padx=20, pady=10, sticky="E")
        address_label.grid(row=4, column=0, padx=20, sticky="E")
        email_label.grid(row=5, column=0, padx=20, pady=10, sticky="E")
        self.first_name_entry.grid(row=1, column=1, padx=5)
        self.last_name_entry.grid(row=2, column=1, padx=5)
        self.username_entry.grid(row=3, column=1, padx=5)
        self.address_entry.grid(row=4, column=1, padx=5)
        self.email_entry.grid(row=5, column=1, padx=5)
        employee_radiobutton.grid(row=6, column=0, columnspan=2, padx=120, sticky="W")
        admin_radiobutton.grid(row=6, column=1, sticky="E", padx=100)
        password_label.grid(row=7, column=0, columnspan=2, padx=40, sticky="W")
        confirm_button.grid(row=7, column=1, padx=40, pady=20, sticky="E")

    def __confirm(self):
        try:
            CURSOR.execute("""
            INSERT INTO shop.members
            (`First Name`, `Last Name`, Username, Address, Email, Admin)
            VALUE 
            ('{0}', '{1}', '{2}', '{3}', '{4}', {5})
            """.format(self.first_name_entry.get(), self.last_name_entry.get(),
                       self.username_entry.get(), self.address_entry.get(), self.email_entry.get(), self.admin.get()))
            CONNECTION.commit()
            self.first_name_entry.delete(0, "end")
            self.last_name_entry.delete(0, "end")
            self.username_entry.delete(0, "end")
            self.address_entry.delete(0, "end")
            self.email_entry.delete(0, "end")
            tk.messagebox.showinfo(_("Info"), _("Account Created"))
        except:
            CONNECTION.rollback()
            tk.messagebox.showwarning(_("Warning"), _("Error: Check details entered."))
