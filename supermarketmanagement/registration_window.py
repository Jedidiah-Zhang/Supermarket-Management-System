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
import re
from main import *

DEFAULT = CONFIG["DEFAULT"]["default password"]


class Registration(SetMenu):
    def __init__(self, master, username):
        super().__init__(master, username, "Registration")
        FONT = get_font()
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
        self.address_text = tk.Text(self.master, width=50, bd=1, height=3, font=(FONT, 14))
        self.email_entry = tk.Entry(self.master, width=50, bd=1, font=(FONT, 14))
        self.admin = tk.BooleanVar()
        self.admin.set(0)
        employee_radiobutton = tk.Radiobutton(self.master, text=t("Employee"), variable=self.admin, value=0)
        admin_radiobutton = tk.Radiobutton(self.master, text=t("Administrator"), variable=self.admin, value=1)
        password_label = tk.Label(self.master, text=t("*Password will be set as default: ") + DEFAULT, font=(FONT, 12))
        confirm_button = tk.Button(self.master, text=t("Confirm"), width=15, font=(FONT, 14), command=self.__confirm)

        self.first_name = tk.StringVar()
        self.first_name.set("*")
        self.label1 = tk.Label(self.master, fg="red", textvariable=self.first_name)
        self.last_name = tk.StringVar()
        self.last_name.set("*")
        self.label2 = tk.Label(self.master, fg="red", textvariable=self.last_name)
        self.username = tk.StringVar()
        self.username.set("*")
        self.label3 = tk.Label(self.master, fg="red", textvariable=self.username)
        self.email = tk.StringVar()
        self.email.set("*")
        self.label4 = tk.Label(self.master, fg="red", textvariable=self.email)

        welcome_label.grid(row=0, column=0, padx=10, pady=10)
        first_name_label.grid(row=1, column=0, padx=20, pady=10, sticky="E")
        last_name_label.grid(row=2, column=0, padx=20, sticky="E")
        username_label.grid(row=3, column=0, padx=20, pady=10, sticky="E")
        address_label.grid(row=4, column=0, padx=20, sticky="EN")
        email_label.grid(row=5, column=0, padx=20, pady=10, sticky="E")
        self.first_name_entry.grid(row=1, column=1, padx=5)
        self.last_name_entry.grid(row=2, column=1, padx=5)
        self.username_entry.grid(row=3, column=1, padx=5)
        self.address_text.grid(row=4, column=1, padx=5)
        self.email_entry.grid(row=5, column=1, padx=5)
        employee_radiobutton.grid(row=6, column=0, columnspan=2, padx=120, sticky="W")
        admin_radiobutton.grid(row=6, column=1, sticky="E", padx=100)
        password_label.grid(row=7, column=0, columnspan=2, padx=40, sticky="W")
        confirm_button.grid(row=7, column=1, padx=40, pady=20, sticky="E")
        self.label1.grid(row=1, column=2)
        self.label2.grid(row=2, column=2)
        self.label3.grid(row=3, column=2)
        self.label4.grid(row=5, column=2)

        self.first_name_entry.bind("<KeyRelease>", lambda event: self.__first_name_check())
        self.last_name_entry.bind("<KeyRelease>", lambda event: self.__last_name_check())
        self.username_entry.bind("<KeyRelease>", lambda event: self.__username_check())
        self.email_entry.bind("<KeyRelease>", lambda event: self.__email_check())

    def __first_name_check(self):
        if self.first_name_entry.get() != "":
            self.first_name.set("√")
            self.label1.config(fg="green")
            return True
        else:
            self.first_name.set("*")
            self.label1.config(fg="red")
            return False

    def __last_name_check(self):
        if self.last_name_entry.get() != "":
            self.last_name.set("√")
            self.label2.config(fg="green")
        else:
            self.last_name.set("*")
            self.label2.config(fg="red")

    def __username_check(self):
        if self.username_entry.get() != "":
            CURSOR.execute("""
            SELECT Username
            FROM shop.members
            WHERE Username = '{}'
            """.format(self.username_entry.get()))
            if CURSOR.fetchone() is None:
                self.username.set("√")
                self.label3.config(fg="green")
            else:
                self.username.set("*")
                self.label3.config(fg="red")
        else:
            self.username.set("*")
            self.label3.config(fg="red")

    def __email_check(self):
        if re.search(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", self.email_entry.get()) is not None:
            CURSOR.execute("""
            SELECT Email
            FROM shop.members
            WHERE Email = '{}'
            """.format(self.email_entry.get()))
            if CURSOR.fetchone() is None:
                self.email.set("√")
                self.label4.config(fg="green")
            else:
                self.email.set("*")
                self.label4.config(fg="red")
        else:
            self.email.set("*")
            self.label4.config(fg="red")

    def __confirm(self):
        password_sha = hashlib.sha256(DEFAULT.encode('utf-8')).hexdigest()
        try:
            if re.search(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", self.email_entry.get()) is None:
                raise ValueError
            CURSOR.execute("""
            INSERT INTO shop.members
            (`First Name`, `Last Name`, Username, Password_SHA, Address, Email, Admin)
            VALUE 
            ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6})
            """.format(self.first_name_entry.get(), self.last_name_entry.get(), self.username_entry.get(),
                       password_sha, self.address_text.get("1.0", "end"), self.email_entry.get(), self.admin.get()))
            CONNECTION.commit()
            self.first_name_entry.delete(0, "end")
            self.last_name_entry.delete(0, "end")
            self.username_entry.delete(0, "end")
            self.address_text.delete("1.0", "end")
            self.email_entry.delete(0, "end")
            self.first_name.set("*")
            self.label1.config(fg="red")
            self.last_name.set("*")
            self.label2.config(fg="red")
            self.username.set("*")
            self.label3.config(fg="red")
            self.email.set("*")
            self.label4.config(fg="red")
            tk.messagebox.showinfo(t("Info"), t("Account Created"))
        except:
            CONNECTION.rollback()
            tk.messagebox.showwarning(t("Warning"), t("Error: Check details entered."))
