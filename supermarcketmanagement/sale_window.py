#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/15 22:07
@Author  : Jedidiah
@Contact : yanzhe_zhang@qq.com
@File    : sale_window.py
@Software: PyCharm
"""

from tkinter import ttk
from tkinter import messagebox
from time import localtime, strftime
from threading import Thread
from main import *


class SalespersonBase(SetMenu):
    def __init__(self, master, username):
        super().__init__(master, username)
        total = tk.StringVar()

        frame_top = tk.Frame(master)
        frame_info = tk.Frame(frame_top)
        frame_list = tk.Frame(master)
        frame_sale = tk.LabelFrame(master)
        frame_entry = tk.LabelFrame(master, text="", font=(FONT, 14))
        frame_goods = tk.Frame(master)

        self.INFO = Info(frame_info, self.user)
        self.LST = List(frame_list, total)
        self.SALE = Sale(frame_sale, total, self.LST, self.INFO)
        self.GOOD = Goods(frame_goods, self.LST)
        self.ENTRY = Entry(frame_entry, self.GOOD)

        frame_list.pack(side="right", fill="both", expand=True)
        frame_top.pack(expand=True, fill="both")
        frame_info.pack(side="right", fill="both", expand=True)
        frame_sale.pack(side="bottom", fill="both", expand=True)
        frame_entry.pack(side="bottom", fill="both", expand=True)
        frame_goods.pack(side="bottom", fill="both", expand=True)


class Info:
    def __init__(self, master, user):
        self.date = tk.StringVar()
        self.order_number = tk.StringVar()
        self.name = tk.StringVar()
        self.staff_code = tk.StringVar()

        label_ordernum = tk.Label(master,
                                  text=t("Order Number: "),
                                  font=(FONT, 13))
        label_salesperson = tk.Label(master,
                                     text=t("Salesperson: "),
                                     font=(FONT, 13))
        label_staffcode = tk.Label(master,
                                   text=t("Staff Code: "),
                                   font=(FONT, 13))
        label_note = tk.Label(master,
                              text=t("Note: "),
                              font=(FONT, 13))
        label_date = tk.Label(master,
                              text=t("Date: "),
                              font=(FONT, 13))
        self.date.set(strftime("%d-%m-%Y", localtime()))
        label_date1 = tk.Label(master,
                               textvariable=self.date,
                               font=(FONT, 13))
        CURSOR.execute("""
        SELECT MAX(`Bill ID`) as `Bill ID`
        FROM shop.bills
        """)
        num = CURSOR.fetchall()[0][0]
        if num is None:
            self.order_number.set("1")
        else:
            self.order_number.set(str(num + 1))
        label_ordernum2 = tk.Label(master,
                                   textvariable=self.order_number,
                                   font=(FONT, 12))
        self.name.set(user[1] + " " + user[2])
        label_salesperson2 = tk.Label(master,
                                      textvariable=self.name,
                                      font=(FONT, 12))
        self.staff_code.set(user[0])
        label_staffcode2 = tk.Label(master,
                                    textvariable=self.staff_code,
                                    font=(FONT, 12))
        entry_note = tk.Entry(master,
                              width=60,
                              font=(FONT, 12))

        label_ordernum.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        label_salesperson.grid(row=1, column=0, padx=10, pady=5, sticky="W")
        label_staffcode.grid(row=2, column=0, padx=10, pady=5, sticky="W")
        label_ordernum2.grid(row=0, column=1, padx=20, sticky="W")
        label_salesperson2.grid(row=1, column=1, padx=20, sticky="W")
        label_staffcode2.grid(row=2, column=1, padx=20, sticky="W")
        label_note.grid(row=3, column=0, padx=10, pady=5, sticky="W")
        entry_note.grid(row=3, column=0, columnspan=5, padx=80, sticky="E")
        label_date.grid(row=0, column=2, padx=10, pady=10, sticky="E")
        label_date1.grid(row=0, column=3)


class List(TreeView):
    def __init__(self, master, total):
        super().__init__()
        self.total = total
        heading = (t("Product Description"), t("Product ID"), t("Price"), t("Discount"), t("Quantity"), t("Subtotal"))
        col_width = (200, 100, 80, 50, 50, 80)
        self.table = ttk.Treeview(master,
                                  height=40,
                                  show="headings",
                                  columns=heading)
        for i, each in enumerate(heading):
            self.table.column(each, width=col_width[i], anchor="center")
            self.table.heading(each, text=each)
        for col in heading:
            self.table.heading(col, text=col,
                               command=lambda _col=col: self.treeview_sort_column(self.table, _col, False))
        self.products = {
            "description": [],
            "id": [],
            "price": [],
            "discount": [],
            "quantity": []
        }

        self.VScroll = tk.Scrollbar(master, orient="vertical", command=self.table.yview)

        self.table.bind("<Double-1>", lambda event: self.__set_quantity(master, event))
        self.table.pack(side="top", fill="both", expand=True)
        self.VScroll.place(relx=0.978, rely=0.025, relwidth=0.02, relheight=0.958)
        self.table.configure(yscrollcommand=self.VScroll.set)

    def __set_quantity(self, master, event):
        def __save_edit():
            new_q = int(entry.get())  # 更改的数量
            self.table.set(row, column=4, value=new_q)
            self.table.set(row, column=5, value=each * new_q)
            self.products["quantity"][rn - 1] = new_q
            total = int(self.total.get())
            total -= quantity * each
            total += int(entry.get()) * each
            self.total.set(total)
            set_window.destroy()

        def __num_only(e):
            try:
                int(e.widget.get())
            except ValueError:
                e.widget.delete(e.widget.index(tk.INSERT) - 1)

        row = self.table.identify_row(event.y)
        if row != "":
            set_window = tk.Toplevel(master)
            set_window.title(t("Set Quantity"))
            set_window.geometry("340x50")
            set_window.resizable(False, False)
            set_window.attributes("-topmost", 1)
            set_window.grab_set()
            label = tk.Label(set_window, text=t("Quantity: "))
            entry = tk.Entry(set_window, width=20)
            rn = int(str(row).replace('I', ''))  # 序号
            quantity = self.products["quantity"][rn - 1]  # 原数量
            each = int(self.products["price"][rn - 1] * (1 - self.products["discount"][rn - 1] / 100))  # 原单价
            button = tk.Button(set_window, text="OK", width=10, command=lambda: __save_edit())
            label.pack(side="left", padx=10)
            entry.insert(0, quantity)
            entry.selection_range(0, "end")
            entry.pack(side="left")
            button.pack(side="left", padx=10)
            entry.bind("<Return>", lambda e: __save_edit())
            entry.bind("<KeyRelease>", __num_only)
            entry.focus()


class Sale:
    def __init__(self, master, total, LST, INFO):
        label_total = tk.Label(master,
                               text=t("Total: "),
                               font=(FONT, 20))

        total.set("0")
        label_number = tk.Label(master,
                                textvariable=total,
                                font=(FONT, 20))
        label_pay = tk.Label(master,
                             text=t("Payment: "),
                             font=(FONT, 20))
        entry_pay = tk.Entry(master,
                             width=10,
                             font=(FONT, 20))
        label_change = tk.Label(master,
                                text=t("Change: "),
                                font=(FONT, 20))
        change = tk.StringVar()
        change.set("0")
        label_change_num = tk.Label(master,
                                    textvariable=change,
                                    font=(FONT, 20))
        button_confirm = tk.Button(master,
                                   text=t("Confirm"),
                                   font=(FONT, 17),
                                   width=13,
                                   command=lambda: self.__confirm(entry_pay, total, change, LST, INFO))

        label_total.grid(row=0, column=0, padx=20, pady=10, sticky="W")
        label_number.grid(row=0, column=1, sticky="W")
        label_pay.grid(row=1, column=0, padx=20, sticky="W")
        entry_pay.grid(row=1, column=1, sticky="W")
        label_change.grid(row=0, column=2, padx=10, sticky="W")
        label_change_num.grid(row=0, column=3, padx=10, sticky="W")
        button_confirm.grid(row=1, column=3, padx=30, pady=15, sticky="W")

        entry_pay.bind("<KeyRelease>", lambda event: self.__calc_change(event, entry_pay, total, change))
        entry_pay.bind("<Return>", lambda event: self.__confirm(entry_pay, total, change, LST, INFO))

    @staticmethod
    def __calc_change(event, entry_pay, total, change):
        try:
            int(event.widget.get())
        except ValueError:
            event.widget.delete(event.widget.index(tk.INSERT) - 1)
        if entry_pay.get() != "":
            try:
                change.set(str(int(entry_pay.get()) - int(total.get())))
            except ValueError:
                pass
        else:
            change.set("")

    @staticmethod
    def __confirm(entry_pay, total, change, LST, INFO):
        if entry_pay.get() == "":
            entry_pay.insert(0, 0)
        if int(total.get()) - int(entry_pay.get()) > 0:
            tk.messagebox.showwarning(title=t("Warning"), message=t("Payment Failure"))
        else:
            children = LST.table.get_children()
            try:
                query_bill = """
                INSERT INTO shop.bills
                (`Cashier ID`, Total, Datetime) 
                VALUE
                ({0}, {1}, '{2}')
                """.format(INFO.staff_code.get(), total.get(),
                           strftime("%Y-%m-%d %H:%M:%S", localtime()))
                CURSOR.execute(query_bill)
                CONNECTION.commit()
                for item in children:
                    row = LST.table.item(item)["values"]
                    query_items = """
                    INSERT INTO shop.items
                    (`Bill ID`, `Product ID`, Quantity, `Selling Price`)
                    VALUES
                    ({0}, {1}, {2}, {3})
                    """.format(INFO.order_number.get(), row[1], row[4], row[2])
                    CURSOR.execute("""
                    SELECT Stock
                    FROM shop.goods
                    WHERE `Product ID` = {0}
                    """.format(row[1]))
                    stock = CURSOR.fetchall()[0][0]
                    CURSOR.execute("""
                    UPDATE shop.goods
                    SET Stock = {0}
                    WHERE `Product ID` = {1}
                    """.format(stock - row[4], row[1]))
                    CURSOR.execute(query_items[:-2])
                    CONNECTION.commit()
                INFO.order_number.set(str(int(INFO.order_number.get()) + 1))
                tk.messagebox.showinfo(t("Info"), t("Success"))
            except:
                CONNECTION.rollback()
                tk.messagebox.showerror(t("Error"), t("Error occur"))

            entry_pay.delete(0, "end")
            total.set(0)
            change.set("0")
            LST.table.delete(*LST.table.get_children())
            LST.products = {
                "description": [],
                "id": [],
                "price": [],
                "discount": [],
                "quantity": []
            }


class Entry:
    def __init__(self, master, Good):
        frame_top = tk.Frame(master)

        label_search = tk.Label(frame_top, text=t("Search："), font=(FONT, 20))
        self.entry_search = tk.Entry(frame_top, font=(FONT, 20))
        self.check = [tk.BooleanVar(), tk.BooleanVar()]
        self.check[0].set(1)
        checkbutton_id = tk.Checkbutton(master,
                                        var=self.check[0],
                                        text=t("ID"), font=(FONT, 12))
        checkbutton_name = tk.Checkbutton(master,
                                          var=self.check[1],
                                          text=t("Name"), font=(FONT, 12))

        frame_top.pack(side="top", fill="both", expand=True)
        label_search.pack(side="left", padx=20)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=10)
        checkbutton_id.pack(side="left", padx=200, pady=10)
        checkbutton_name.pack(side="left", padx=20, pady=10)

        self.entry_search.bind("<KeyRelease>", lambda event: self.__save_search(Good))

    def __save_search(self, GOOD):
        GOOD.clear_list()
        quest = '.*{}.*'.format(self.entry_search.get())
        if self.check[0].get() and self.check[1].get() is False:
            CURSOR.execute("""
            SELECT * 
            FROM shop.goods
            WHERE `Product ID` RLIKE '{0}'
            """.format(quest))
        elif self.check[0].get() is False and self.check[1].get():
            CURSOR.execute("""
            SELECT *
            FROM shop.goods
            WHERE `Product Description` RLIKE '{0}'
            """.format(quest))
        elif self.check[0].get() and self.check[1].get():
            CURSOR.execute("""
            SELECT *
            FROM shop.goods
            WHERE `Product ID` RLIKE '{0}' OR `Product Description` RLIKE '{1}'
            """.format(quest, quest))
        output = CURSOR.fetchall()
        for each in output[:20]:
            GOOD.add_row(each[1], each[0], each[4], each[8])


class Goods(TreeView):
    def __init__(self, master, LST):
        super().__init__()
        heading = (t("Product Description"), t("Product ID"), t("Price"), t("Discount"))
        self.alternative_table = tk.ttk.Treeview(master,
                                                 height=40,
                                                 show="headings",
                                                 columns=heading)
        width = (200, 100, 80, 50)
        for i, each in enumerate(heading):
            self.alternative_table.column(each, width=width[i], anchor="center")
            self.alternative_table.heading(each, text=each)
        for col in heading:
            self.alternative_table.heading(col, text=col,
                                           command=lambda _col=col: self.treeview_sort_column(self.alternative_table,
                                                                                              _col, False))
        self.alternative_table.pack(fill="both")
        self.description = []
        self.good_id = []
        self.price = []
        self.discount = []

        self.VScroll = tk.Scrollbar(master, orient="vertical", command=self.alternative_table.yview)
        self.VScroll.place(relx=0.978, rely=0.025, relwidth=0.02, relheight=0.958)
        self.alternative_table.configure(yscrollcommand=self.VScroll.set)

        self.alternative_table.bind("<Double-1>", lambda event: self.__get_row(LST))

    def __get_row(self, LST):  # 双击行
        for item in self.alternative_table.selection():
            row = self.alternative_table.item(item, "values")
            self.add_to_list(LST, row[0], int(row[1]), float(row[2]), int(row[3]), 1)

    @staticmethod
    def add_to_list(LST, description, product_id, price, discount, quantity):
        if product_id not in LST.products["id"]:
            LST.products["description"].append(description)
            LST.products["id"].append(product_id)
            LST.products["price"].append(price)
            LST.products["discount"].append(discount)
            LST.products["quantity"].append(quantity)
            subtotal = int(price * (1 - (discount / 100)) * quantity)
            LST.table.insert('', len(LST.products["description"]) - 1,
                             values=(description, product_id, price,
                                     discount, quantity, subtotal))
            LST.table.update()
            LST.total.set(str(int(LST.total.get()) + subtotal))

    def add_row(self, desc, good_id, price, discount):
        self.description.append(desc)
        self.good_id.append(good_id)
        self.price.append(price)
        self.discount.append(discount)
        try:
            self.alternative_table.insert("", len(self.description) - 1,
                                          values=(self.description[-1],
                                                  self.good_id[-1],
                                                  self.price[-1],
                                                  self.discount[-1]))
            self.alternative_table.update()
        except:
            pass

    def clear_list(self):
        self.description = []
        self.good_id = []
        self.price = []
        self.discount = []
        children = self.alternative_table.get_children()
        for item in children:
            self.alternative_table.delete(item)
