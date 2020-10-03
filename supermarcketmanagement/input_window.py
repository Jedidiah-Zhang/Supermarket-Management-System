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

CURSOR = main.CURSOR
CONNECTION = main.CONNECTION
CURSOR.execute("USE shop")

FONT = main.FONT


class Purchase(main.SetMenu, main.TreeView):
    def __init__(self, master, username):
        super().__init__(master, username)
        self.data = None
        name_label = tk.Label(master,
                              text=_("Principal: "),
                              font=(FONT, 16))
        name_label2 = tk.Label(master,
                               text=self.user[1] + " " + self.user[2],
                               font=(FONT, 16))
        purchase_button = tk.Button(master,
                                    width=25,
                                    text=_("Purchase Form File"),
                                    font=(FONT, 16),
                                    command=self.read_file)
        confirm_button = tk.Button(master,
                                   width=10,
                                   text=_("Confirm"),
                                   font=(FONT, 16),
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
        for col in heading:
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))
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
            CURSOR.execute("""
            SELECT MAX(`Product ID`)
            FROM shop.goods
            """)
            maximum = CURSOR.fetchall()[0][0]
            if maximum is None:
                maximum = 0
            for row in self.data:
                CURSOR.execute("""
                SELECT `Product ID`
                FROM shop.goods
                WHERE  `External ID` = {0} and Supplier = '{1}'
                """.format(row[0], row[2]))
                ID = CURSOR.fetchall()
                try:
                    if ID == ():
                        self.tree.insert("", "end",
                                         values=(row[1], maximum + 1, row[0], row[5], row[2], row[3]))
                        maximum += 1
                    else:
                        self.tree.insert("", "end",
                                         values=(row[1], ID[0][0], row[0], row[5], row[2], [row[3]]))
                except:
                    pass
                self.tree.update()

    def confirm(self):
        CURSOR.execute("""
                    SELECT MAX(`Product ID`)
                    FROM shop.purchase
                    """)
        maximum = CURSOR.fetchall()[0][0]
        if maximum is None:
            maximum = 0
        for row in self.data:
            CURSOR.execute("""
            SELECT `Product ID`
            FROM shop.goods
            WHERE `External ID` = {0} and Supplier = '{1}'
            """.format(row[0], row[2]))
            ID = CURSOR.fetchall()
            if ID == ():
                try:
                    maximum += 1
                    CURSOR.execute("""
                    INSERT INTO shop.purchase
                    (`Product Description`, `Product ID`, `External ID`, `Principal ID`, 
                    Supplier, Datetime, Amount, Price)
                    VALUE
                    ('{0}', {1}, {2}, {3}, '{4}', '{5}', {6}, {7})
                    """.format(row[1], maximum, row[0], self.user[0], row[2],
                               strftime("%Y-%m-%d %H:%M:%S", localtime()), row[5], row[3]))
                    CONNECTION.commit()
                    CURSOR.execute("""
                    INSERT INTO shop.goods
                    (`product id`, `product description`, Stock, `Buying Price`, 
                    `Selling Price`, `external id`, supplier)
                    VALUE
                    ({0}, '{1}', {2}, {3}, {4}, {5}, '{6}')
                    """.format(maximum, row[1], row[5], row[3], round(row[3] * 1.25, 2), row[0], row[2]))
                    CONNECTION.commit()
                except TclError:
                    CONNECTION.rollback()
            else:
                ID = ID[0][0]
                try:
                    CURSOR.execute("""
                    INSERT INTO shop.purchase
                    (`Product Description`, `Product ID`, `External ID`, `Principal ID`, 
                    Supplier, Datetime, Amount, Price)
                    VALUE
                    ('{0}', {1}, {2}, {3}, '{4}', '{5}', {6}, {7})
                    """.format(row[1], ID, row[0], self.user[0], row[2],
                               strftime("%Y-%m-%d %H:%M:%S", localtime()), row[5], row[3]))
                    CONNECTION.commit()
                    CURSOR.execute("""
                    SELECT Stock
                    FROM shop.goods
                    WHERE `Product ID` = {0}
                    """.format(ID))
                    stock = CURSOR.fetchall()[0][0]
                    CURSOR.execute("""
                    UPDATE shop.goods
                    SET Stock = {0}
                    WHERE `Product ID` = {1}
                    """.format(stock + row[5], ID))
                    CONNECTION.commit()
                except:
                    CONNECTION.rollback()

        tk.messagebox.showinfo(_("Info"), _("Done"))
