#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/08/09 10:25
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : stock_window.py
@Software: PyCharm
"""

import tkinter as tk
from tkinter import ttk
import main

CURSOR = main.CURSOR
CONNECTION = main.CONNECTION
CURSOR.execute("USE shop")

FONT = main.FONT


class StockManagement(main.SetMenu, main.TreeView):
    def __init__(self, master, username):
        super().__init__(master, username)

        id_label = tk.Label(master,
                            text=_("Good ID: "),
                            font=(FONT, 16))
        self.id_entry = tk.Entry(master,
                                 width=40,
                                 font=(FONT, 12))
        desc_label = tk.Label(master,
                              text=_("Good Name: "),
                              font=(FONT, 16))
        self.desc_entry = tk.Entry(master,
                                   width=40,
                                   font=(FONT, 12))
        ex_id_label = tk.Label(master,
                               text=_("External ID: "),
                               font=(FONT, 16))
        self.ex_id_entry = tk.Entry(master,
                                    width=25,
                                    font=(FONT, 12))
        supplier_label = tk.Label(master,
                                  text=_("Supplier: "),
                                  font=(FONT, 16))
        self.supplier_entry = tk.Entry(master,
                                       width=25,
                                       font=(FONT, 12))
        alter_button = tk.Button(master,
                                 width=12,
                                 text=_("Alter"),
                                 font=(FONT, 16),
                                 command=lambda: self._alter_row(self.tree.selection()))
        analyze_button = tk.Button(master,
                                   width=12,
                                   text=_("Analyze"),
                                   font=(FONT, 16),
                                   command=self._analyze)
        heading = [_("ID"), _("Description"), _("Stock"), _("Buying Price"),
                   _("Selling Price"), _("External ID"), _("Supplier")]
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

        self.id_entry.bind("<KeyRelease>", lambda event: self._search())
        self.desc_entry.bind("<KeyRelease>", lambda event: self._search())
        self.ex_id_entry.bind("<KeyRelease>", lambda event: self._search())
        self.supplier_entry.bind("<KeyRelease>", lambda event: self._search())

        self._search()
        self.top = None

    def _search(self):
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

    def _alter_row(self, row):
        if self.top is None and row != ():
            self._create_toplevel(row)
        elif row == ():
            pass
        else:
            try:
                if "normal" == self.top.state():
                    self.A_window.values(self.tree.item(row[0], "values"))
                    self.top.focus_set()
            except tk.TclError:
                self.top = None
                self._create_toplevel(row)
                pass

    def _create_toplevel(self, row):
        self.top = tk.Toplevel()
        self.top.geometry("620x250")
        self.top.title(_("Alter"))
        self.A_window = Alter(self.top, self.tree.item(row[0], "values"))

    def _analyze(self):
        pass


class Alter:
    def __init__(self, master, values):
        self.values = values
        desc_label = tk.Label(master,
                              text=_("Product Description: "),
                              font=(FONT, 16))
        stock_label = tk.Label(master,
                               text=_("Stock: "),
                               font=(FONT, 16))
        sell_label = tk.Label(master,
                              text=_("Selling Price: "),
                              font=(FONT, 16))
        self.desc_entry = tk.Entry(master,
                                   width=40,
                                   font=(FONT, 13))
        self.desc_entry.insert(0, values[1])
        self.stock_entry = tk.Entry(master,
                                    width=40,
                                    font=(FONT, 13))
        self.stock_entry.insert(0, values[2])
        self.sell_entry = tk.Entry(master,
                                   width=40,
                                   font=(FONT, 13))
        self.sell_entry.insert(0, values[4])
        delete_button = tk.Button(master,
                                  width=15,
                                  text=_("Delete Row"),
                                  font=(FONT, 16),
                                  command=lambda: self._delete(master))
        confirm_button = tk.Button(master,
                                   width=15,
                                   text=_("Confirm Change"),
                                   font=(FONT, 16),
                                   command=lambda: self._confirm(master))
        desc_label.grid(row=0, column=0, padx=20, pady=20, sticky="E")
        stock_label.grid(row=1, column=0, padx=20, sticky="E")
        sell_label.grid(row=2, column=0, padx=20, pady=20, sticky="E")
        self.desc_entry.grid(row=0, column=1)
        self.stock_entry.grid(row=1, column=1)
        self.sell_entry.grid(row=2, column=1)
        delete_button.grid(row=3, column=0, columnspan=2, padx=80, sticky="W")
        confirm_button.grid(row=3, column=1, padx=40, sticky="E")

        self.desc_entry.bind("<Button-3>", self._entry_clear)
        self.stock_entry.bind("<Button-3>", self._entry_clear)
        self.stock_entry.bind("<KeyRelease>", self._num_only)
        self.sell_entry.bind("<Button-3>", self._entry_clear)
        self.sell_entry.bind("<KeyRelease>", self._num_only)

    def values(self, values):
        self.values = values
        self.desc_entry.delete(0, "end")
        self.desc_entry.insert(0, values[1])
        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, values[2])
        self.stock_entry.delete(0, "end")
        self.sell_entry.insert(0, values[4])

    @staticmethod
    def _num_only(event):
        try:
            float(event.widget.get())
        except ValueError:
            event.widget.delete(event.widget.index(tk.INSERT) - 1)

    @staticmethod
    def _entry_clear(event):
        event.widget.delete(0, "end")
        event.widget.focus()

    def _delete(self, master):
        try:
            CURSOR.execute("""
            DELETE FROM shop.goods
            WHERE `Product ID` = {0}
            """.format(self.values[0]))
            CONNECTION.commit()
            master.destroy()
        except:
            CONNECTION.rollback()

    def _confirm(self, master):
        try:
            CURSOR.execute("""
            UPDATE shop.goods
            SET `Product Description` = '{0}', Stock = {1}, `Selling Price` = {2}
            WHERE `Product ID` = {3}
            """.format(self.desc_entry.get(), self.stock_entry.get(), self.sell_entry.get(), self.values[0]))
            CONNECTION.commit()
            master.destroy()
        except:
            CONNECTION.rollback()
