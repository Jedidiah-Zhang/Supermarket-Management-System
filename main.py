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
from os import popen
import configparser
import pymysql
from supermarketmanagement import opener

# 链接数据库
CONNECTION = pymysql.connect(host="localhost",
                             port=3306,
                             user="root",
                             password="fdc45ba2",
                             db="shop")
CURSOR = CONNECTION.cursor()

CFG = "./docs/default.ini"
CONFIG = configparser.ConfigParser()
CONFIG.read(CFG)

LANGUAGES = ["Chinese", "English"]
FONTS = ["方正书宋简体", "Adobe Garamond Pro"]
CUR_LANG = CONFIG["DEFAULT"]["language"]
FONT = dict(zip(LANGUAGES, FONTS))[CUR_LANG]


def t(msgid: str) -> str:
    trans = {}
    with open('./lang/{}.lang'.format(CUR_LANG), 'r', encoding='utf-8') as f:
        for each in f.readlines()[:-1]:
            lines = each[:-1].split('=')
            trans[lines[0]] = lines[1]
    if msgid in trans:
        return trans[msgid]
    else:
        return msgid


class SetMenu:
    def __init__(self, master, name):
        CURSOR.execute("""
        SELECT * 
        FROM shop.members
        WHERE `Username` = '{0}'
        """.format(name))
        self.user = CURSOR.fetchall()[0]

        menubar = tk.Menu(master)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t("Settings"), menu=setting_menu)
        lang_menu = tk.Menu(setting_menu, tearoff=0)
        setting_menu.add_cascade(label=t("Language"), menu=lang_menu)
        for each in LANGUAGES:
            lang_menu.add_command(label=each, command=lambda arg=each: self._set_lang(arg, master))
        setting_menu.add_command(label=t("Account"), command=lambda: self._account(self.user, master))
        setting_menu.add_command(label=t("Back"), command=lambda: self._back(master, self.user))
        setting_menu.add_command(label=t("Logout"), command=lambda: self._logout(master))
        master.config(menu=menubar)

    @staticmethod
    def _set_lang(lang: str, master):
        CONFIG["DEFAULT"]["language"] = lang
        CONFIG["DEFAULT"]["font"] = dict(zip(LANGUAGES, FONTS))[lang]
        CONFIG.write(open(CFG, "w"))
        popen("python %s/main.py" % CONFIG["DEFAULT"]["path"])
        master.destroy()

    @staticmethod
    def _logout(master):
        CONFIG["DEFAULT"]["remember"] = "False"
        CONFIG["ACCOUNTS"]["username"] = ""
        CONFIG.write(open(CFG, "w"))
        popen("python %s/main.py" % CONFIG["DEFAULT"]["path"])
        master.destroy()

    @staticmethod
    def _account(info, master):
        root_window = tk.Tk()
        root_window.title(t("Account"))
        root_window.geometry("600x320")
        root_window.resizable(False, False)
        Account(root_window, info, master)
        root_window.mainloop()

    @staticmethod
    def _back(master, info):
        master.destroy()
        opener.SelectionFactory(info[7], info[3])


class Account:
    def __init__(self, master, info, root):
        id_label1 = tk.Label(master,
                             text=t("ID: "),
                             font=(CONFIG["DEFAULT"]["font"], 16))
        id_label2 = tk.Label(master,
                             text=info[0],
                             font=(CONFIG["DEFAULT"]["font"], 16))
        name_label1 = tk.Label(master,
                               text=t("Name: "),
                               font=(CONFIG["DEFAULT"]["font"], 16))
        name_label2 = tk.Label(master,
                               text=info[1] + " " + info[2],
                               font=(CONFIG["DEFAULT"]["font"], 16))
        username_label = tk.Label(master,
                                  text=t("Username: "),
                                  font=(CONFIG["DEFAULT"]["font"], 16))
        self.username_entry = tk.Entry(master,
                                       width=40,
                                       font=(CONFIG["DEFAULT"]["font"], 16))
        self.username_entry.insert(0, info[3])
        email_label = tk.Label(master,
                               text=t("Email: "),
                               font=(CONFIG["DEFAULT"]["font"], 16))
        self.email_entry = tk.Entry(master,
                                    width=40,
                                    font=(CONFIG["DEFAULT"]["font"], 16))
        self.email_entry.insert(0, info[6])
        address_label = tk.Label(master,
                                 text=t("Address: "),
                                 font=(CONFIG["DEFAULT"]["font"], 16))
        self.address_text = tk.Text(master,
                                    width=40,
                                    height=3,
                                    font=(CONFIG["DEFAULT"]["font"], 16))
        self.address_text.insert("end", info[5])
        password_button = tk.Button(master,
                                    width=15,
                                    text=t("Change Password"),
                                    font=(CONFIG["DEFAULT"]["font"], 16),
                                    command=lambda: self.__change_pass(info, master, root))
        confirm_button = tk.Button(master,
                                   width=15,
                                   text=t("Confirm Changes"),
                                   font=(CONFIG["DEFAULT"]["font"], 16),
                                   command=lambda: self.__confirm(info, master, root))

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
    def __change_pass(info, master, root):
        top = tk.Toplevel()
        top.title(t("Change Password"))
        top.geometry("370x130")
        top.resizable(False, False)
        original_label = tk.Label(top,
                                  text=t("Original Password: "),
                                  font=(CONFIG["DEFAULT"]["font"], 16))
        original_entry = tk.Entry(top,
                                  width=20,
                                  bd=2,
                                  font=(CONFIG["DEFAULT"]["font"], 12))
        new_label = tk.Label(top,
                             text=t("New Password: "),
                             font=(CONFIG["DEFAULT"]["font"], 16))
        new_entry = tk.Entry(top,
                             width=20,
                             bd=2,
                             font=(CONFIG["DEFAULT"]["font"], 12))
        confirm_label = tk.Label(top,
                                 text=t("Confirm Password: "),
                                 font=(CONFIG["DEFAULT"]["font"], 16))
        confirm_entry = tk.Entry(top,
                                 width=20,
                                 bd=2,
                                 font=(CONFIG["DEFAULT"]["font"], 12))

        original_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")
        original_entry.grid(row=0, column=1)
        new_label.grid(row=1, column=0, padx=10, sticky="E")
        new_entry.grid(row=1, column=1)
        confirm_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
        confirm_entry.grid(row=2, column=1)

        original_entry.bind("<Return>", lambda event: new_entry.focus())
        new_entry.bind("<Return>", lambda event: confirm_entry.focus())
        confirm_entry.bind("<Return>", lambda event: __save_change())

        original_entry.focus()

        def __save_change():
            original_sha = hashlib.sha256(original_entry.get().encode('utf-8')).hexdigest()
            if original_sha == info[4]:
                if new_entry.get() == confirm_entry.get():
                    new_sha = hashlib.sha256(new_entry.get().encode('utf-8')).hexdigest()
                    try:
                        CURSOR.execute("""
                        UPDATE shop.members
                        SET Password_SHA = '{0}'
                        WHERE `Employee ID` = {1}
                        """.format(new_sha, info[0]))
                        CONNECTION.commit()
                        popen("python %s/main.py" % CONFIG["DEFAULT"]["path"])
                        master.destroy()
                        root.destroy()
                    except:
                        CONNECTION.rollback()
                        tk.messagebox.showerror(t("Error"), t("Error occur, check the format of password."))
                else:
                    tk.messagebox.showwarning(t("Warning"), t("Check passwords entered."))
            else:
                tk.messagebox.showwarning(t("Warning"), t("Password incorrect."))

    def __confirm(self, info, master, root):
        try:
            CURSOR.execute("""
            UPDATE shop.members
            SET Username = '{0}' , Email = '{1}', Address = '{2}'
            WHERE `Employee ID` = {3}
            """.format(self.username_entry.get(), self.email_entry.get(), self.address_text.get("1.0", "end"), info[0]))
            CONNECTION.commit()
            if CONFIG.getboolean("DEFAULT", "REMEMBER"):
                CONFIG["ACCOUNTS"]["username"] = self.username_entry.get()
                CONFIG.write(open(CFG, "w"))
        except:
            CONNECTION.rollback()
        popen("python %s/main.py" % CONFIG["DEFAULT"]["path"])
        master.destroy()
        root.destroy()


class TreeView:
    def __init__(self):
        pass

    def treeview_sort_column(self, tv, col, reverse):
        L = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            L.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            L.sort(reverse=reverse)
        for index, (val, k) in enumerate(L):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))


if __name__ == "__main__":
    if not CONFIG.getboolean("DEFAULT", "REMEMBER"):
        opener.login()
    else:
        Username = CONFIG["ACCOUNTS"]["username"]
        CURSOR.execute("""
        SELECT * 
        FROM shop.members
        WHERE `Username` = '{0}'
        """.format(Username))
        User = CURSOR.fetchall()[0]
        opener.SelectionFactory(User[7], Username)
