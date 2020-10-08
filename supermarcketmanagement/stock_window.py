#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/08/09 10:25
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : stock_window.py
@Software: PyCharm
"""

from tkinter import ttk
from main import *


class StockManagement(SetMenu, TreeView):
    def __init__(self, master, username):
        super().__init__(master, username)

        id_label = tk.Label(master,
                            text=t("Good ID: "),
                            font=(FONT, 16))
        self.id_entry = tk.Entry(master,
                                 width=40,
                                 font=(FONT, 12))
        desc_label = tk.Label(master,
                              text=t("Good Name: "),
                              font=(FONT, 16))
        self.desc_entry = tk.Entry(master,
                                   width=40,
                                   font=(FONT, 12))
        ex_id_label = tk.Label(master,
                               text=t("External ID: "),
                               font=(FONT, 16))
        self.ex_id_entry = tk.Entry(master,
                                    width=25,
                                    font=(FONT, 12))
        supplier_label = tk.Label(master,
                                  text=t("Supplier: "),
                                  font=(FONT, 16))
        self.supplier_entry = tk.Entry(master,
                                       width=25,
                                       font=(FONT, 12))
        alter_button = tk.Button(master,
                                 width=12,
                                 text=t("Alter"),
                                 font=(FONT, 16),
                                 command=lambda: self.__alter_row(self.tree.selection()))
        analyze_button = tk.Button(master,
                                   width=12,
                                   text=t("Analyze"),
                                   font=(FONT, 16),
                                   command=self.__analyze)
        heading = [t("ID"), t("Description"), t("Stock"), t("Buying Price"),
                   t("Selling Price"), t("External ID"), t("Supplier")]
        width = [200, 300, 90, 90, 90, 173, 200]
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

        id_label.grid(row=0, column=0, sticky="W", padx=5, pady=10)
        self.id_entry.grid(row=0, column=1, sticky="W")
        desc_label.grid(row=1, column=0, sticky="W", padx=5)
        self.desc_entry.grid(row=1, column=1, sticky="W")
        ex_id_label.grid(row=0, column=2, sticky="W", padx=5)
        self.ex_id_entry.grid(row=0, column=3, sticky="W")
        supplier_label.grid(row=1, column=2, sticky="W", padx=5)
        self.supplier_entry.grid(row=1, column=3, sticky="W")
        alter_button.grid(row=0, column=4, rowspan=2, padx=20)
        analyze_button.grid(row=0, column=5, rowspan=2, padx=10)
        self.tree.grid(row=2, column=0, columnspan=6, sticky="NEWS", pady=5)
        self.VScroll.place(relx=0.98, rely=0.15, relwidth=0.02, relheight=0.828)
        self.tree.configure(yscrollcommand=self.VScroll.set)

        self.id_entry.bind("<KeyRelease>", lambda event: self.search())
        self.desc_entry.bind("<KeyRelease>", lambda event: self.search())
        self.ex_id_entry.bind("<KeyRelease>", lambda event: self.search())
        self.supplier_entry.bind("<KeyRelease>", lambda event: self.search())
        master.bind("<FocusIn>", lambda event: self.search())

        self.search()
        self.A_window = None

    def search(self):
        children = self.tree.get_children()
        for item in children:
            self.tree.delete(item)
        quests = [self.id_entry.get(), self.desc_entry.get(), self.ex_id_entry.get(), self.supplier_entry.get()]
        CURSOR.execute("""
        SELECT `Product ID`, `Product Description`, Stock, 
        `Buying Price`, `Selling Price`, `External ID`, Supplier
        FROM shop.goods
        WHERE `Product ID` LIKE '{0}'
        AND `Product Description` LIKE '{1}'
        AND `External ID` LIKE '{2}'
        AND Supplier LIKE '{3}'
        """.format("%" + quests[0] + "%" if quests[0] is not None else "%",
                   "%" + quests[1] + "%" if quests[1] is not None else "%",
                   "%" + quests[2] + "%" if quests[2] is not None else "%",
                   "%" + quests[3] + "%" if quests[3] is not None else "%"))
        output = CURSOR.fetchall()
        for each in output:
            self.tree.insert("", "end", values=each)
        self.tree.update()

    def __alter_row(self, row):
        if self.A_window is None and row != ():
            self.__create_toplevel(row)
        elif row == ():
            pass
        else:
            try:
                if "normal" == self.A_window.state():
                    self.A_window.set_values(self.tree.item(row[0], "values"))
                    self.A_window.focus_set()
            except tk.TclError:
                self.A_window = None
                self.__create_toplevel(row)

    def __create_toplevel(self, row):
        self.A_window = Alter(self.tree.item(row[0], "values"))

    def __analyze(self):
        pass


class Alter(tk.Toplevel):
    def __init__(self, values, **kw):
        super().__init__(**kw)
        self.title(t("Alter"))
        self.geometry("620x250")
        self.values = values

        desc_label = tk.Label(self,
                              text=t("Product Description: "),
                              font=(FONT, 16))
        stock_label = tk.Label(self,
                               text=t("Stock: "),
                               font=(FONT, 16))
        sell_label = tk.Label(self,
                              text=t("Selling Price: "),
                              font=(FONT, 16))
        self.desc_entry = tk.Entry(self,
                                   width=40,
                                   font=(FONT, 13))
        self.desc_entry.insert(0, values[1])
        self.stock_entry = tk.Entry(self,
                                    width=40,
                                    font=(FONT, 13))
        self.stock_entry.insert(0, values[2])
        self.sell_entry = tk.Entry(self,
                                   width=40,
                                   font=(FONT, 13))
        self.sell_entry.insert(0, values[4])
        delete_button = tk.Button(self,
                                  width=15,
                                  text=t("Delete Row"),
                                  font=(FONT, 16),
                                  command=self.__delete)
        confirm_button = tk.Button(self,
                                   width=15,
                                   text=t("Confirm Changes"),
                                   font=(FONT, 16),
                                   command=self.__confirm)
        desc_label.grid(row=0, column=0, padx=20, pady=20, sticky="E")
        stock_label.grid(row=1, column=0, padx=20, sticky="E")
        sell_label.grid(row=2, column=0, padx=20, pady=20, sticky="E")
        self.desc_entry.grid(row=0, column=1)
        self.stock_entry.grid(row=1, column=1)
        self.sell_entry.grid(row=2, column=1)
        delete_button.grid(row=3, column=0, columnspan=2, padx=80, sticky="W")
        confirm_button.grid(row=3, column=1, padx=40, sticky="E")

        self.desc_entry.bind("<Button-3>", self.__entry_clear)
        self.stock_entry.bind("<Button-3>", self.__entry_clear)
        self.stock_entry.bind("<KeyRelease>", self.__num_only)
        self.sell_entry.bind("<Button-3>", self.__entry_clear)
        self.sell_entry.bind("<KeyRelease>", self.__num_only)

    def set_values(self, values: tuple):
        self.values = values
        self.desc_entry.delete(0, "end")
        self.desc_entry.insert(0, values[1])
        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, values[2])
        self.sell_entry.delete(0, "end")
        self.sell_entry.insert(0, values[4])

    @staticmethod
    def __num_only(event):
        try:
            float(event.widget.get())
        except ValueError:
            event.widget.delete(event.widget.index(tk.INSERT) - 1)

    @staticmethod
    def __entry_clear(event):
        event.widget.delete(0, "end")
        event.widget.focus()

    def __delete(self):
        try:
            CURSOR.execute("""
            DELETE FROM shop.goods
            WHERE `Product ID` = {0}
            """.format(self.values[0]))
            CONNECTION.commit()
            self.desc_entry.delete(0, "end")
            self.stock_entry.delete(0, "end")
            self.sell_entry.delete(0, "end")
        except:
            CONNECTION.rollback()

    def __confirm(self):
        try:
            CURSOR.execute("""
            UPDATE shop.goods
            SET `Product Description` = '{0}', Stock = {1}, `Selling Price` = {2}
            WHERE `Product ID` = {3}
            """.format(self.desc_entry.get(), self.stock_entry.get(), self.sell_entry.get(), self.values[0]))
            CONNECTION.commit()
            self.desc_entry.delete(0, "end")
            self.stock_entry.delete(0, "end")
            self.sell_entry.delete(0, "end")
        except:
            CONNECTION.rollback()


class Analysis(tk.Toplevel):
    def __init__(self, **kw):
        super().__init__(**kw)
