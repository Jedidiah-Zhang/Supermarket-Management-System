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
from os import system, environ
import configparser
import pymysql
import webbrowser
from supermarketmanagement import opener
import pyglet as pl

CFG = "./docs/default.ini"
CONFIG = configparser.ConfigParser()
CONFIG.read(CFG, encoding="utf-8")

for each in CONFIG["LANGUAGE"]["fonts path"].split(", "):
    pl.font.add_file(each)
LANGUAGES = CONFIG["LANGUAGE"]["languages"].split(", ")
FONTS = CONFIG["LANGUAGE"]["fonts"].split(", ")
CUR_LANG = CONFIG["DEFAULT"]["language"]
FONT = dict(zip(LANGUAGES, FONTS))[CUR_LANG]


def init_language():
    trans = {}
    with open('./lang/{}.lang'.format(CUR_LANG), 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines[:-1].split('=')
            trans[line[0]] = line[1]
    return trans


def t(msgid: str) -> str:
    if msgid in TRANSLATION:
        return TRANSLATION[msgid]
    else:
        return msgid


TRANSLATION = init_language()

db_name = CONFIG["DATABASE"]["user"]
db_pass = CONFIG["DATABASE"]["password"]
try:
    CONNECTION = pymysql.connect(host=CONFIG["DATABASE"]["host"],
                                 port=int(CONFIG["DATABASE"]["port"]),
                                 user=db_name,
                                 password=db_pass)
    CURSOR = CONNECTION.cursor()
except pymysql.err.OperationalError:
    CURSOR = None
    tk.messagebox.showerror(t("Error"), t("Cannot find database, check database information in the config file."))
    quit()
try:
    CURSOR.execute("USE shop")
except pymysql.err.OperationalError:
    path = environ["path"].split(';')
    if CONFIG["DATABASE"]["mysql path"] not in path:
        environ["path"] = environ["path"] + ';' + CONFIG["DATABASE"]["mysql path"]
    system("mysql -u" + db_name + " -p" + db_pass + " < .\\sql.sql")


class SetMenu:
    def __init__(self, master, name, window):
        self.master = master
        CURSOR.execute("""
        SELECT * 
        FROM shop.members
        WHERE `Username` = '{0}'
        """.format(name))
        self.user = CURSOR.fetchall()[0]

        self.menubar = tk.Menu(self.master)
        self.action_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t("Action"), menu=self.action_menu)
        lang_menu = tk.Menu(self.action_menu, tearoff=0)
        self.action_menu.add_cascade(label=t("Language"), menu=lang_menu)
        for each in LANGUAGES:
            lang_menu.add_command(label=each, command=lambda arg=each: self._set_lang(arg, window))
        self.action_menu.add_command(label=t("Back"), command=self._back)

        self.account_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t("Account"), menu=self.account_menu)
        self.account_menu.add_command(label=t("Details"), command=self._account)
        self.account_menu.add_command(label=t("Logout"), command=self._logout)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t("Help"), menu=self.help_menu)
        self.help_menu.add_command(label=t("Open Help File"), command=self._open_file)
        self.help_menu.add_command(label=t("Open GitHub Page"), command=self._open_url)

        self.master.config(menu=self.menubar)

    def _set_lang(self, lang: str, window):
        global CUR_LANG, FONT, TRANSLATION
        CONFIG["DEFAULT"]["language"] = lang
        CONFIG["DEFAULT"]["font"] = dict(zip(LANGUAGES, FONTS))[lang]
        CONFIG.write(open(CFG, "w", encoding="utf-8"))
        CUR_LANG = lang
        FONT = dict(zip(LANGUAGES, FONTS))[CUR_LANG]
        TRANSLATION = init_language()
        self.master.destroy()
        opener.WindowFactory(window, self.user[3])

    def _logout(self):
        CONFIG["DEFAULT"]["remember"] = "False"
        CONFIG["ACCOUNTS"]["username"] = ""
        CONFIG.write(open(CFG, "w", encoding="utf-8"))
        self.master.destroy()
        opener.WindowFactory("Login")

    def _account(self):
        root_window = tk.Tk()
        root_window.title(t("Account"))
        root_window.geometry("600x320")
        root_window.resizable(False, False)
        Account(root_window, self.user, self.master)
        root_window.mainloop()

    def _back(self):
        self.master.destroy()
        if self.user[7] == 1:
            opener.WindowFactory("Admin", username=self.user[3])
        else:
            opener.WindowFactory("Employee", username=self.user[3])

    @staticmethod
    def _open_file():
        webbrowser.open_new_tab("https://github.com/Jedidiah-Zhang/Supermarket-Management-System/blob/master/README.md")

    @staticmethod
    def _open_url():
        webbrowser.open_new_tab("https://github.com/Jedidiah-Zhang/Supermarket-Management-System")


class Account:
    def __init__(self, master, info, root):
        self.master = master
        self.info = info
        self.root = root
        id_label1 = tk.Label(self.master, text=t("ID: "), font=(FONT, 16))
        id_label2 = tk.Label(self.master, text=info[0], font=(FONT, 16))
        name_label1 = tk.Label(self.master, text=t("Name: "), font=(FONT, 16))
        name_label2 = tk.Label(self.master, text="%s %s" % (info[1], info[2]), font=(FONT, 16))
        username_label = tk.Label(self.master, text=t("Username: "), font=(FONT, 16))
        self.username_entry = tk.Entry(self.master, width=40, font=(FONT, 16))
        self.username_entry.insert(0, info[3])
        email_label = tk.Label(self.master, text=t("Email: "), font=(FONT, 16))
        self.email_entry = tk.Entry(self.master, width=40, font=(FONT, 16))
        self.email_entry.insert(0, info[6])
        address_label = tk.Label(self.master, text=t("Address: "), font=(FONT, 16))
        self.address_text = tk.Text(self.master, width=40, height=3, font=(FONT, 16))
        self.address_text.insert("end", info[5])
        password_button = tk.Button(self.master, width=15, text=t("Change Password"), font=(FONT, 16),
                                    command=self.__change_pass)
        confirm_button = tk.Button(self.master, width=15, text=t("Confirm Changes"), font=(FONT, 16),
                                   command=self.__confirm)

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

    def __change_pass(self):
        top = tk.Toplevel()
        top.title(t("Change Password"))
        top.geometry("370x130")
        top.resizable(False, False)
        original_label = tk.Label(top, text=t("Original Password: "), font=(FONT, 16))
        original_entry = tk.Entry(top, width=20, bd=2, font=(FONT, 12))
        new_label = tk.Label(top, text=t("New Password: "), font=(FONT, 16))
        new_entry = tk.Entry(top, width=20, bd=2, font=(FONT, 12))
        confirm_label = tk.Label(top, text=t("Confirm Password: "), font=(FONT, 16))
        confirm_entry = tk.Entry(top, width=20, bd=2, font=(FONT, 12))

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
            if original_sha == self.info[4]:
                if new_entry.get() == confirm_entry.get():
                    new_sha = hashlib.sha256(new_entry.get().encode('utf-8')).hexdigest()
                    try:
                        CURSOR.execute("""
                        UPDATE shop.members
                        SET Password_SHA = '{0}'
                        WHERE `Employee ID` = {1}
                        """.format(new_sha, self.info[0]))
                        CONNECTION.commit()
                        tk.messagebox.showwarning(t("Warning"),
                                                  t("Account details have been changed, please login again."))
                        self.master.destroy()
                        self.root.destroy()
                        opener.WindowFactory("Login")
                    except:
                        CONNECTION.rollback()
                        tk.messagebox.showerror(t("Error"), t("Error occur, check the format of password."))
                else:
                    tk.messagebox.showwarning(t("Warning"), t("Check passwords entered."))
            else:
                tk.messagebox.showwarning(t("Warning"), t("Password incorrect."))

    def __confirm(self):
        try:
            CURSOR.execute("""
            UPDATE shop.members
            SET Username = '{0}' , Email = '{1}', Address = '{2}'
            WHERE `Employee ID` = {3}
            """.format(self.username_entry.get(), self.email_entry.get(),
                       self.address_text.get("1.0", "end"), self.info[0]))
            CONNECTION.commit()
            if CONFIG.getboolean("DEFAULT", "REMEMBER"):
                CONFIG["ACCOUNTS"]["username"] = self.username_entry.get()
                CONFIG.write(open(CFG, "w", encoding="utf-8"))
            tk.messagebox.showwarning(t("Warning"), t("Account details have been changed, please login again."))
            self.master.destroy()
            self.root.destroy()
            opener.WindowFactory("Login")
        except:
            CONNECTION.rollback()
            tk.messagebox.showwarning(t("Error"), t("Error occur"))


class TreeView:
    def __init__(self):
        pass

    def sort_column(self, tv, col, reverse):
        L = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            L.sort(key=lambda x: int(x[0]), reverse=reverse)
        except ValueError:
            L.sort(reverse=reverse)
        for index, (val, k) in enumerate(L):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.sort_column(tv, col, not reverse))


if __name__ == "__main__":
    if not CONFIG.getboolean("DEFAULT", "REMEMBER"):
        opener.WindowFactory("Login")
    else:
        Username = CONFIG["ACCOUNTS"]["username"]
        CURSOR.execute("""
        SELECT * 
        FROM shop.members
        WHERE `Username` = '{0}'
        """.format(Username))
        try:
            User = CURSOR.fetchall()[0]
            if User[7] == 1:
                opener.WindowFactory("Admin", Username)
            else:
                opener.WindowFactory("Employee", Username)
        except IndexError:
            CONFIG["DEFAULT"]["remember"] = "False"
            CONFIG["ACCOUNTS"]["username"] = ""
            CONFIG.write(open(CFG, "w", encoding="utf-8"))
            opener.WindowFactory("Login")
