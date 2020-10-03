#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/15 20:07
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : login_window.py
@Software: PyCharm
"""

import tkinter as tk
from tkinter import messagebox
import hashlib
from supermarcketmanagement import opener
import main

CURSOR = main.CURSOR
CURSOR.execute("USE shop")

CFG = main.CFG
CONFIG = main.CONFIG


class LoginWindow:
    def __init__(self, master):
        label_welcome = tk.Label(master,
                                 text=_("Login"),
                                 font=(CONFIG["DEFAULT"]["font"], 16))
        label_username = tk.Label(master,
                                  text=_("Username: "))
        label_password = tk.Label(master,
                                  text=_("Password: "))
        self.entry_username = tk.Entry(master,
                                       width=35)
        self.entry_password = tk.Entry(master,
                                       width=35,
                                       show="*")
        button_confirm = tk.Button(master,
                                   width=10,
                                   text=_("LOGIN"),
                                   command=lambda: self.__login(master))

        self.rem = tk.IntVar()
        checkbutton_remember = tk.Checkbutton(master,
                                              text=_("Remember Me"),
                                              variable=self.rem,
                                              onvalue=1,
                                              offvalue=0)

        label_welcome.grid(row=0, column=0, padx=10, pady=10)
        label_username.grid(row=1, column=0, padx=10, pady=10)
        label_password.grid(row=2, column=0, padx=10)
        self.entry_username.grid(row=1, column=1, columnspan=2)
        self.entry_password.grid(row=2, column=1, columnspan=2)
        button_confirm.grid(row=3, column=2, sticky="SE", pady=20)
        checkbutton_remember.grid(row=3, column=1, sticky="WN")

        self.entry_username.bind("<Return>", lambda event: self.__next())
        self.entry_password.bind("<Return>", lambda event: self.__login(master))

        self.entry_username.focus()

    def __next(self):
        self.entry_password.focus()

    def __login(self, master):
        username = self.entry_username.get()
        password_sha = hashlib.sha256(self.entry_password.get().encode('utf-8')).hexdigest()
        CURSOR.execute("""
        SELECT * 
        FROM shop.members
        WHERE `Username` = '{0}'
        """.format(username))
        user = CURSOR.fetchall()
        if user:
            user = user[0]
            if user[4] == password_sha:
                CONFIG["ACCOUNTS"]["USERNAME"] = username
                if self.rem.get() == 1:
                    CONFIG["DEFAULT"]["REMEMBER"] = "True"
                    CONFIG.write(open(CFG, "w"))
                master.destroy()
                if user[7] == 0:
                    opener.employee(username)
                else:
                    opener.admin(username)
            else:
                tk.messagebox.showwarning(_("Warning"), _("Password does not match."))
        else:
            tk.messagebox.showwarning(_("Warning"), _("Username does not exist."))
