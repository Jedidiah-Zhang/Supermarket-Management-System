#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/08/09 10:26
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : input_window.py
@Software: PyCharm
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from time import strftime, localtime
import main

cursor = main.cursor
connection = main.connection
cursor.execute("USE shop")

cfg = main.cfg
config = main.config


class Purchase(main.SetMenu):
    def __init__(self, master, username):
        super().__init__(master, username)
        self.data = None
        name_label = tk.Label(master,
                              text=_("Principal: "),
                              font=(config["DEFAULT"]["font"], 16))
        name_label2 = tk.Label(master,
                               text=self.user[1] + " " + self.user[2],
                               font=(config["DEFAULT"]["font"], 16))
        purchase_button = tk.Button(master,
                                    width=25,
                                    text=_("Purchase Form File"),
                                    font=(config["DEFAULT"]["font"], 16),
                                    command=self.read_file)
        confirm_button = tk.Button(master,
                                   width=10,
                                   text=_("Confirm"),
                                   font=(config["DEFAULT"]["font"], 16),
                                   command=self.confirm)
        heading = ["Product Description", "Product ID", "External ID", "Amount", "Supplier", "Price"]
        width = [240, 140, 140, 80, 140, 100]
        self.tree = ttk.Treeview(master,
                                 height=100,
                                 columns=heading,
                                 show='headings')
        for i in range(len(heading)):
            self.tree.column(heading[i], width=width[i], anchor="center")
            self.tree.heading(heading[i], text=heading[i])

        self.VScroll = tk.Scrollbar(master, orient="vertical", command=self.tree.yview)

        name_label.grid(row=0, column=0, padx=10, sticky="E")
        name_label2.grid(row=0, column=1)
        purchase_button.grid(row=0, column=2, padx=20, pady=5)
        confirm_button.grid(row=0, column=3)
        self.tree.grid(row=1, column=0, columnspan=4, sticky="NEWS")
        self.VScroll.place(relx=0.98, rely=0.145, relwidth=0.02, relheight=0.828)
        self.tree.configure(yscrollcommand=self.VScroll.set)

    def read_file(self):
        filename = tk.filedialog.askopenfilename()
        if filename != "":
            self.data = pd.read_excel(filename).values
            cursor.execute("""
            SELECT MAX(`Product ID`)
            FROM shop.purchase
            """)
            maximum = cursor.fetchall()[0][0]
            if maximum is None:
                maximum = 0
            for row in self.data:
                try:
                    self.tree.insert("", "end",
                                     values=(row[1], maximum+1, row[0], row[5], row[2], row[3]))
                    maximum += 1
                    self.tree.update()
                except:
                    pass

    def confirm(self):
        cursor.execute("""
                    SELECT MAX(`Product ID`)
                    FROM shop.purchase
                    """)
        maximum = cursor.fetchall()[0][0]
        if maximum is None:
            maximum = 0
        for row in self.data:
            cursor.execute("""
            SELECT `Product ID`
            FROM shop.goods
            WHERE `External ID` = {0}
            """.format(row[0]))
            ID = cursor.fetchall()
            if ID == ():
                try:
                    maximum += 1
                    cursor.execute("""
                    INSERT INTO shop.purchase
                    (`Product Description`, `Product ID`, `External ID`, `Principal ID`, 
                    Supplier, Datetime, Amount, Price)
                    VALUE
                    ('{0}', {1}, {2}, {3}, '{4}', '{5}', {6}, {7})
                    """.format(row[1], maximum, row[0], self.user[0], row[2],
                               strftime("%Y-%m-%d %H:%M:%S", localtime()), row[5], row[3]))
                    connection.commit()
                    cursor.execute("""
                    INSERT INTO shop.goods
                    (`product id`, `product description`, Stock, `Buying Price`, 
                    `Selling Price`, `external id`, supplier)
                    VALUE
                    ({0}, '{1}', {2}, {3}, {4}, {5}, '{6}')
                    """.format(maximum, row[1], row[5], row[3], round(row[3]*1.25, 2), row[0], row[2]))
                    connection.commit()
                except:
                    connection.rollback()
            else:
                ID = ID[0][0]
                try:
                    cursor.execute("""
                    INSERT INTO shop.purchase
                    (`Product Description`, `Product ID`, `External ID`, `Principal ID`, 
                    Supplier, Datetime, Amount, Price)
                    VALUE
                    ('{0}', {1}, {2}, {3}, '{4}', '{5}', {6}, {7})
                    """.format(row[1], ID, row[0], self.user[0], row[2],
                               strftime("%Y-%m-%d %H:%M:%S", localtime()), row[5], row[3]))
                    connection.commit()
                    cursor.execute("""
                    SELECT Stock
                    FROM shop.goods
                    WHERE `Product ID` = {0}
                    """.format(ID))
                    stock = cursor.fetchall()[0][0]
                    cursor.execute("""
                    UPDATE shop.goods
                    SET Stock = {0}
                    WHERE `Product ID` = {1}
                    """.format(stock+row[5], ID))
                    connection.commit()
                except:
                    connection.rollback()

        tk.messagebox.showinfo(_("Info"), _("Done"))

