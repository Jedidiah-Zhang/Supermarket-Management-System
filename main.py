#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/14 20:03
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : main.py
@Software: PyCharm
"""

import tkinter as tk
from tkinter import messagebox
import hashlib
import gettext
from os import popen
import configparser
import pymysql
from supermarcketmanagement import opener

# 链接数据库
connection = pymysql.connect(host="localhost",
                             port=3306,
                             user="root",
                             password="fdc45ba2",
                             db="shop")
cursor = connection.cursor()

cfg = "./docs/default.ini"
config = configparser.ConfigParser()
config.read(cfg)
defaults = dict(config.defaults())
gettext.translation("lang", "./lang", languages=[defaults["language"]]).install("lang")

languages = ["zh_CN", "en_GB"]
fonts = ["方正书宋简体", "Adobe Garamond Pro"]
cur_lang = config["DEFAULT"]["language"]
font = dict(zip(languages, fonts))[cur_lang]


class SetMenu:
    def __init__(self, master, name):
        cursor.execute("""
        SELECT * 
        FROM shop.members
        WHERE `Username` = '{0}'
        """.format(name))
        self.user = cursor.fetchall()[0]

        menubar = tk.Menu(master)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Settings"), menu=setting_menu)
        lang_menu = tk.Menu(setting_menu, tearoff=0)
        setting_menu.add_cascade(label=_("Language"), menu=lang_menu)
        for each in languages:
            lang_menu.add_command(label=each, command=lambda arg=each: self.set_lang(arg, master))
        setting_menu.add_command(label=_("Account"), command=lambda: self.account(self.user, master))
        setting_menu.add_command(label=_("Back"), command=lambda: self.back(master, self.user))
        setting_menu.add_command(label=_("Logout"), command=lambda: self.logout(master))
        master.config(menu=menubar)

    @staticmethod
    def set_lang(lang: str, master):
        config["DEFAULT"]["language"] = lang
        config["DEFAULT"]["font"] = dict(zip(languages, fonts))[lang]
        config.write(open(cfg, "w"))
        gettext.install("lang", "./lang")
        gettext.translation("lang", "./lang", languages=[lang]).install("lang")
        popen("python %s/main.py" % config["DEFAULT"]["path"])
        master.destroy()

    @staticmethod
    def logout(master):
        config["DEFAULT"]["remember"] = "False"
        config["ACCOUNTS"]["username"] = ""
        config["ACCOUNTS"]["password_sha"] = ""
        config.write(open(cfg, "w"))
        popen("python %s/main.py" % config["DEFAULT"]["path"])
        master.destroy()

    @staticmethod
    def account(info, master):
        root_window = tk.Tk()
        root_window.title(_("Account"))
        root_window.geometry("600x320")
        root_window.resizable(False, False)
        Account(root_window, info, master)
        root_window.mainloop()

    @staticmethod
    def back(master, info):
        master.destroy()
        if info[7] == 1:
            opener.admin(info[3])
        else:
            opener.employee(info[3])


class Account:
    def __init__(self, master, info, root):
        id_label1 = tk.Label(master,
                             text=_("ID: "),
                             font=(config["DEFAULT"]["font"], 16))
        id_label2 = tk.Label(master,
                             text=info[0],
                             font=(config["DEFAULT"]["font"], 16))
        name_label1 = tk.Label(master,
                               text=_("Name: "),
                               font=(config["DEFAULT"]["font"], 16))
        name_label2 = tk.Label(master,
                               text=info[1] + " " + info[2],
                               font=(config["DEFAULT"]["font"], 16))
        username_label = tk.Label(master,
                                  text=_("Username: "),
                                  font=(config["DEFAULT"]["font"], 16))
        self.username_entry = tk.Entry(master,
                                       width=40,
                                       font=(config["DEFAULT"]["font"], 16))
        self.username_entry.insert(0, info[3])
        email_label = tk.Label(master,
                               text=_("Email: "),
                               font=(config["DEFAULT"]["font"], 16))
        self.email_entry = tk.Entry(master,
                                    width=40,
                                    font=(config["DEFAULT"]["font"], 16))
        self.email_entry.insert(0, info[6])
        address_label = tk.Label(master,
                                 text=_("Address: "),
                                 font=(config["DEFAULT"]["font"], 16))
        self.address_text = tk.Text(master,
                                    width=40,
                                    height=3,
                                    font=(config["DEFAULT"]["font"], 16))
        self.address_text.insert("end", info[5])
        password_button = tk.Button(master,
                                    width=15,
                                    text=_("Change Password"),
                                    font=(config["DEFAULT"]["font"], 16),
                                    command=lambda: self.change_pass(info, master, root))
        confirm_button = tk.Button(master,
                                   width=15,
                                   text=_("Confirm Changes"),
                                   font=(config["DEFAULT"]["font"], 16),
                                   command=lambda: self._confirm(info, master, root))

        id_label1.grid(row=0, column=0, padx=10, pady=5, sticky="E")
        id_label2.grid(row=0, column=1)
        name_label1.grid(row=1, column=0, padx=10, sticky="E")
        name_label2.grid(row=1, column=1)
        username_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.username_entry.grid(row=2, column=1)
        email_label.grid(row=3, column=0, padx=10, sticky="E")
        self.email_entry.grid(row=3, column=1)
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky="NE")
        self.address_text.grid(row=4, column=1, pady=5)
        password_button.grid(row=5, column=0, padx=60, columnspan=2, pady=5, sticky="W")
        confirm_button.grid(row=5, column=1, padx=40, sticky="E")

    @staticmethod
    def change_pass(info, master, root):
        top = tk.Toplevel()
        top.title(_("Change Password"))
        top.geometry("370x130")
        top.resizable(False, False)
        original_label = tk.Label(top,
                                  text=_("Original Password: "),
                                  font=(config["DEFAULT"]["font"], 16))
        original_entry = tk.Entry(top,
                                  width=20,
                                  bd=2,
                                  font=(config["DEFAULT"]["font"], 12))
        new_label = tk.Label(top,
                             text=_("New Password: "),
                             font=(config["DEFAULT"]["font"], 16))
        new_entry = tk.Entry(top,
                             width=20,
                             bd=2,
                             font=(config["DEFAULT"]["font"], 12))
        confirm_label = tk.Label(top,
                                 text=_("Confirm Password: "),
                                 font=(config["DEFAULT"]["font"], 16))
        confirm_entry = tk.Entry(top,
                                 width=20,
                                 bd=2,
                                 font=(config["DEFAULT"]["font"], 12))

        original_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")
        original_entry.grid(row=0, column=1)
        new_label.grid(row=1, column=0, padx=10, sticky="E")
        new_entry.grid(row=1, column=1)
        confirm_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
        confirm_entry.grid(row=2, column=1)

        original_entry.bind("<Return>", lambda event: new_entry.focus())
        new_entry.bind("<Return>", lambda event: confirm_entry.focus())
        confirm_entry.bind("<Return>", lambda event: _save_change())

        original_entry.focus()

        def _save_change():
            original_sha = hashlib.sha256(original_entry.get().encode('utf-8')).hexdigest()
            if original_sha == info[4]:
                if new_entry.get() == confirm_entry.get():
                    new_sha = hashlib.sha256(new_entry.get().encode('utf-8')).hexdigest()
                    try:
                        cursor.execute("""
                        UPDATE shop.members
                        SET Password_SHA = '{0}'
                        WHERE `Employee ID` = {1}
                        """.format(new_sha, info[0]))
                        connection.commit()
                        popen("python %s/main.py" % config["DEFAULT"]["path"])
                        master.destroy()
                        root.destroy()
                    except:
                        connection.rollback()
                        tk.messagebox.showerror(_("Error"), _("Error occur, check the format of password."))
                else:
                    tk.messagebox.showwarning(_("Warning"), _("Check passwords entered."))
            else:
                tk.messagebox.showwarning(_("Warning"), _("Password incorrect."))

    def _confirm(self, info, master, root):
        try:
            cursor.execute("""
            UPDATE shop.members
            SET Username = '{0}' , Email = '{1}', Address = '{2}'
            WHERE `Employee ID` = {3}
            """.format(self.username_entry.get(), self.email_entry.get(), self.address_text.get("1.0", "end"), info[0]))
            connection.commit()
            if config.getboolean("DEFAULT", "REMEMBER"):
                config["ACCOUNTS"]["username"] = self.username_entry.get()
                config.write(open(cfg, "w"))
        except:
            connection.rollback()
        popen("python %s/main.py" % config["DEFAULT"]["path"])
        master.destroy()
        root.destroy()


if __name__ == "__main__":
    if not config.getboolean("DEFAULT", "REMEMBER"):
        opener.login()
    else:
        username = config["ACCOUNTS"]["username"]
        cursor.execute("""
        SELECT * 
        FROM shop.members
        WHERE `Username` = '{0}'
        """.format(username))
        user = cursor.fetchall()[0]
        if user[7]:
            opener.admin(username)
        else:
            opener.employee(username)
