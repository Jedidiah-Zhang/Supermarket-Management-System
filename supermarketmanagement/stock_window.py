#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 20/08/09 10:25
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : stock_window.py
@Software: PyCharm
"""
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from main import *


class StockManagement(SetMenu, TreeView):
    def __init__(self, master, username):
        super().__init__(master, username, "Inventory")
        self.master = master

        self.popup = tk.Menu(self.master, tearoff=0)
        self.popup.add_command(label=t("Alter"), command=self.__alter_row, state="disabled")
        self.popup.add_command(label=t("Delete"), command=self.__delete, state="disabled")

        id_label = tk.Label(self.master, text=t("Good ID: "), font=(FONT, 16))
        self.id_entry = tk.Entry(self.master, width=40, font=(FONT, 12))
        desc_label = tk.Label(self.master, text=t("Good Name: "), font=(FONT, 16))
        self.desc_entry = tk.Entry(self.master, width=40, font=(FONT, 12))
        ex_id_label = tk.Label(self.master, text=t("External ID: "), font=(FONT, 16))
        self.ex_id_entry = tk.Entry(self.master, width=25, font=(FONT, 12))
        supplier_label = tk.Label(self.master, text=t("Supplier: "), font=(FONT, 16))
        self.supplier_entry = tk.Entry(self.master, width=25, font=(FONT, 12))
        alter_button = tk.Button(self.master, width=12, text=t("Alter"), font=(FONT, 16), command=self.__alter_row)
        analyze_button = tk.Button(self.master, width=12, text=t("Analyze"), font=(FONT, 16), command=self.__analyze)

        heading = [t("ID"), t("Description"), t("Stock"), t("Buying Price"),
                   t("Selling Price"), t("External ID"), t("Supplier")]
        width = [200, 300, 90, 90, 90, 173, 200]
        self.table = ttk.Treeview(self.master, height=100, columns=heading, show='headings')

        for i in range(len(heading)):
            self.table.column(heading[i], width=width[i], anchor="center")
            self.table.heading(heading[i], text=heading[i])
        for col in heading:
            self.table.heading(col, text=col,
                               command=lambda _col=col: self.sort_column(self.table, _col, False))
        self.VScroll = tk.Scrollbar(self.master, orient="vertical", command=self.table.yview)

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
        self.table.grid(row=2, column=0, columnspan=6, sticky="NEWS", pady=5)
        self.VScroll.place(relx=0.98, rely=0.15, relwidth=0.02, relheight=0.828)
        self.table.configure(yscrollcommand=self.VScroll.set)

        def __pop_up(event):
            self.table.selection_set(self.table.identify_row(event.y))
            if self.table.selection() != ():
                self.popup.entryconfig(t("Alter"), state='normal')
                self.popup.entryconfig(t("Delete"), state='normal')
            self.popup.post(event.x_root, event.y_root)
            self.popup.grab_release()

        self.table.bind("<Button-3>", __pop_up)
        self.id_entry.bind("<KeyRelease>", lambda event: self.search())
        self.desc_entry.bind("<KeyRelease>", lambda event: self.search())
        self.ex_id_entry.bind("<KeyRelease>", lambda event: self.search())
        self.supplier_entry.bind("<KeyRelease>", lambda event: self.search())
        self.master.bind("<FocusIn>", lambda event: self.search())

        self.search()
        self.AlterWindow = None
        self.AnalysisWindow = None

    def search(self):
        children = self.table.get_children()
        for item in children:
            self.table.delete(item)
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
            self.table.insert("", "end", values=each)
        self.table.update()

    def __alter_row(self):
        row = self.table.selection()
        if self.AlterWindow is None and row != ():
            self.AlterWindow = Alter(self.table.item(row, "values"))
        elif row == ():
            pass
        else:
            try:
                if self.AlterWindow.state() == "normal":
                    self.AlterWindow.set_values(self.table.item(row[0], "values"))
                    self.AlterWindow.focus_set()
            except tk.TclError:
                self.AlterWindow = None
                self.AlterWindow = Alter(self.table.item(row, "values"))

    def __delete(self):
        item = self.table.selection()
        row = self.table.item(item, "values")
        confirm = tk.messagebox.askokcancel(t("Warning"),
                                            t("The row will be deleted, there's no way for undo this action!"))
        if confirm:
            try:
                CURSOR.execute("""
                DELETE FROM shop.goods
                WHERE `Product ID` = {0}
                """.format(row[0]))
                CONNECTION.commit()
            except:
                CONNECTION.rollback()
            self.table.delete(item)
            self.table.update()

    def __analyze(self):
        try:
            if self.AnalysisWindow.state() == 'normal':
                self.AnalysisWindow.focus()
        except:
            self.AnalysisWindow = Analysis()


class Alter(tk.Toplevel):
    def __init__(self, values, **kw):
        super().__init__(**kw)
        self.title(t("Alter"))
        self.geometry("620x250")
        self.resizable(False, False)
        self.values = values

        desc_label = tk.Label(self, text=t("Product Description: "), font=(FONT, 16))
        stock_label = tk.Label(self, text=t("Stock: "), font=(FONT, 16))
        sell_label = tk.Label(self, text=t("Selling Price: "), font=(FONT, 16))
        self.desc_entry = tk.Entry(self, width=40, font=(FONT, 13))
        self.desc_entry.insert(0, values[1])
        self.stock_entry = tk.Entry(self, width=40, font=(FONT, 13))
        self.stock_entry.insert(0, values[2])
        self.sell_entry = tk.Entry(self, width=40, font=(FONT, 13))
        self.sell_entry.insert(0, values[4])
        delete_button = tk.Button(self, width=15, text=t("Delete Row"), font=(FONT, 16), command=self.__delete)
        confirm_button = tk.Button(self, width=15, text=t("Confirm Changes"), font=(FONT, 16), command=self.__confirm)

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
        self.title(t("Analysis"))
        self.geometry("650x500")
        self.resizable(False, False)
        locale = {"Chinese": "zh_CN", "English": "en_GB"}

        from_label = tk.Label(self, text=t("From: "), font=(FONT, 16))
        self.from_date = DateEntry(self, width=20, font=(FONT, 16),
                                   date_pattern="y-mm-dd", locale=locale[CUR_LANG], borderwidth=2)
        to_label = tk.Label(self, text=t("To: "), font=(FONT, 16))
        self.to_date = DateEntry(self, width=20, font=(FONT, 16),
                                 date_pattern="y-mm-dd", locale=locale[CUR_LANG], borderwidth=2)
        supplier_label = tk.Label(self, text=t("Supplier"), font=(FONT, 16))
        self.supplier_list = tk.Listbox(self, selectmode="extended", exportselection=0,
                                        font=("Adobe Garamond Pro", 16), width=25)
        supplier_scroll = tk.Scrollbar(self.supplier_list, orient="vertical", command=self.supplier_list.yview)
        self.supplier_list.configure(yscrollcommand=supplier_scroll.set)
        supplier_scroll.place(relx=0.98, rely=-0.05, relwidth=0.02, relheight=1.1)
        CURSOR.execute("""
        SELECT DISTINCT supplier
        FROM shop.goods
        """)
        supplier = CURSOR.fetchall()
        for item in supplier:
            self.supplier_list.insert("end", item[0])

        cashier_label = tk.Label(self, text=t("Cashier"), font=(FONT, 16))
        self.cashier_list = tk.Listbox(self, selectmode="extended", exportselection=0,
                                       font=("Adobe Garamond Pro", 16), width=25)
        cashier_scroll = tk.Scrollbar(self.cashier_list, orient="vertical", command=self.cashier_list.yview)
        self.cashier_list.configure(yscrollcommand=cashier_scroll.set)
        cashier_scroll.place(relx=0.98, rely=-0.05, relwidth=0.02, relheight=1.1)
        CURSOR.execute("""
                SELECT DISTINCT `Cashier ID`
                FROM shop.bills
                """)
        cashier = CURSOR.fetchall()
        for item in cashier:
            CURSOR.execute("""
            SELECT `First Name`, `Last Name`
            FROM shop.members
            WHERE `Employee ID` = {}
            """.format(item[0]))
            name = CURSOR.fetchone()
            self.cashier_list.insert("end", "%s %s" % name)

        file_button = tk.Button(self, text=t("Output to File"), font=(FONT, 16), width=20, command=self.__create_file)

        from_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")
        self.from_date.grid(row=0, column=1)
        to_label.grid(row=0, column=2, padx=10)
        self.to_date.grid(row=0, column=3)
        supplier_label.grid(row=1, column=0, columnspan=2)
        self.supplier_list.grid(row=2, column=0, columnspan=2)
        cashier_label.grid(row=1, column=2, columnspan=2)
        self.cashier_list.grid(row=2, column=2, columnspan=2)
        file_button.grid(row=3, column=0, columnspan=2, pady=30)

    def __create_file(self):
        start_date = self.from_date.get()
        end_date = self.to_date.get()
        supplier = (self.supplier_list.get(i) for i in self.supplier_list.curselection())
        cashier = (self.cashier_list.get(i) for i in self.supplier_list.curselection())
        CURSOR.execute("""
        SELECT b.`Bill ID`, b.`Cashier ID`, i.`Product ID`, i.Quantity, i.`Selling Price`
        FROM shop.bills b
        LEFT JOIN shop.items i
        ON b.`Bill ID` = i.`Bill ID`
        WHERE b.Datetime BETWEEN '{0}' AND '{1}'
        """.format(start_date, end_date))
        print(CURSOR.fetchall())
        CURSOR.execute("""
        CREATE OR REPLACE VIEW all_items AS
        SELECT b.`Bill ID`, b.`Cashier ID`, b.Datetime, i.`Product ID`, i.Quantity, i.`Selling Price`
        FROM shop.bills b
        LEFT JOIN shop.items i
        ON b.`Bill ID` = i.`Bill ID`
        """)

        file_name = tk.filedialog.asksaveasfilename(filetypes=[("Excel", ".xlsx")])
        print(file_name)
