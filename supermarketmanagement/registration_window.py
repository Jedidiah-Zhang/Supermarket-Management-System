#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/08/09 10:27
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : registration_window.py
@Software: PyCharm
"""

from tkinter import messagebox
from main import *

DEFAULT = CONFIG["DEFAULT"]["default_pass"]


class Registration(SetMenu):
    def __init__(self, master, username):
        super().__init__(master, username, "Registration")
        self.master = master

        welcome_label = tk.Label(self.master, text=t("Registration"), font=(FONT, 20))
        first_name_label = tk.Label(self.master, text=t("First Name: "), font=(FONT, 14))
        last_name_label = tk.Label(self.master, text=t("Last Name: "), font=(FONT, 14))
        username_label = tk.Label(self.master,text=t("Username: "),font=(FONT, 14))
        address_label = tk.Label(self.master, text=t("Address: "), font=(FONT, 14))
        email_label = tk.Label(self.master, text=t("Email: "), font=(FONT, 14))

        self.first_name_entry = tk.Entry(self.master, width=50, bd=1, font=(FONT, 14))
        self.last_name_entry = tk.Entry(self.master, width=50, bd=1, font=(FONT, 14))
        self.username_entry = tk.Entry(self.master, width=50, bd=1, font=(FONT, 14))
        self.address_entry = tk.Entry(self.master, width=50, bd=1, font=(FONT, 14))
        self.email_entry = tk.Entry(self.master, width=50, bd=1, font=(FONT, 14))
        self.admin = tk.BooleanVar()
        self.admin.set(0)
        employee_radiobutton = tk.Radiobutton(self.master, text=t("Employee"), variable=self.admin, value=0)
        admin_radiobutton = tk.Radiobutton(self.master, text=t("Administration"), variable=self.admin, value=1)
        password_label = tk.Label(self.master, text=t("*Password will be set as default: ") + DEFAULT, font=(FONT, 12))
        confirm_button = tk.Button(self.master, text=t("Confirm"), width=15, font=(FONT, 14), command=self.__confirm)

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
            tk.messagebox.showinfo(t("Info"), t("Account Created"))
        except:
            CONNECTION.rollback()
            tk.messagebox.showwarning(t("Warning"), t("Error: Check details entered."))
