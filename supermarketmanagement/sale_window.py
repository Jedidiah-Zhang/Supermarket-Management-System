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
from main import *


class SalespersonBase(SetMenu):
    def __init__(self, master, username):
        super().__init__(master, username, "Cashier")
        self.master = master
        self.total = tk.StringVar()

        frame_top = tk.Frame(self.master)
        frame_info = tk.Frame(frame_top)
        frame_list = tk.Frame(self.master)
        frame_sale = tk.LabelFrame(self.master)
        frame_entry = tk.LabelFrame(self.master, text="", font=(FONT, 14))
        frame_goods = tk.Frame(self.master)

        self.INFO = Info(frame_info, self.user)
        self.LST = List(frame_list, self.total)
        self.SALE = Sale(frame_sale, self.total, self.LST, self.INFO)
        self.GOOD = Goods(frame_goods, self.LST)
        self.ENTRY = Entry(frame_entry, self.GOOD)

        frame_list.pack(side="right", fill="both", expand=True)
        frame_top.pack(fill="both", expand=True)
        frame_info.pack(side="right", fill="both", expand=True)
        frame_sale.pack(side="bottom", fill="both", expand=True)
        frame_entry.pack(side="bottom", fill="both", expand=True)
        frame_goods.pack(side="bottom", fill="both", expand=True)


class Info:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        self.date = tk.StringVar()
        self.order_number = tk.StringVar()
        self.name = tk.StringVar()
        self.staff_code = tk.StringVar()

        label_ordernum = tk.Label(self.master, text=t("Order Number: "), font=(FONT, 13))
        label_salesperson = tk.Label(self.master, text=t("Salesperson: "), font=(FONT, 13))
        label_staffcode = tk.Label(self.master, text=t("Staff Code: "), font=(FONT, 13))
        label_note = tk.Label(self.master, text=t("Note: "), font=(FONT, 13))
        label_date = tk.Label(self.master, text=t("Date: "), font=(FONT, 13))
        self.date.set(strftime("%d-%m-%Y", localtime()))
        label_date1 = tk.Label(self.master, textvariable=self.date, font=(FONT, 13))
        CURSOR.execute("""
        SELECT MAX(`Bill ID`) as `Bill ID`
        FROM shop.bills
        """)
        num = CURSOR.fetchall()[0][0]
        if num is None:
            self.order_number.set("1")
        else:
            self.order_number.set(str(num + 1))
        label_ordernum2 = tk.Label(self.master, textvariable=self.order_number, font=(FONT, 12))
        self.name.set("%s %s" % (self.user[1], self.user[2]))
        label_salesperson2 = tk.Label(self.master, textvariable=self.name, font=(FONT, 12))
        self.staff_code.set(self.user[0])
        label_staffcode2 = tk.Label(self.master, textvariable=self.staff_code, font=(FONT, 12))
        entry_note = tk.Entry(self.master, width=60, font=(FONT, 12))

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
        self.master = master
        self.total = total

        self.popup = tk.Menu(self.master, tearoff=0)
        self.popup.add_command(label=t("Set Quantity"), command=self.__set_quantity, state="disabled")

        heading = (t("Product Description"), t("Product ID"), t("Price"), t("Discount"), t("Quantity"), t("Subtotal"))
        col_width = (200, 100, 80, 50, 50, 80)
        self.table = ttk.Treeview(self.master, height=40, show="headings", columns=heading)
        for i, each in enumerate(heading):
            self.table.column(each, width=col_width[i], anchor="center")
            self.table.heading(each, text=each)
        for col in heading:
            self.table.heading(col, text=col, command=lambda _col=col: self.sort_column(self.table, _col, False))
        self.products = {
            "description": [],
            "id": [],
            "price": [],
            "discount": [],
            "quantity": []
        }

        self.VScroll = tk.Scrollbar(master, orient="vertical", command=self.table.yview)

        def __pop_up(event):
            self.popup.selection = self.table.identify_row(event.y)
            if self.popup.selection != "":
                self.popup.entryconfig(t("Set Quantity"), state='normal')
            self.popup.post(event.x_root, event.y_root)
            self.popup.grab_release()

        self.table.bind("<Double-1>", self.__set_quantity)
        self.table.bind("<Button-3>",  __pop_up)
        self.table.pack(side="top", fill="both", expand=True)
        self.VScroll.place(relx=0.978, rely=0.025, relwidth=0.02, relheight=0.958)
        self.table.configure(yscrollcommand=self.VScroll.set)

    def __set_quantity(self, event=None):
        def __save_edit():
            new_q = int(entry.get())  # 更改的数量
            self.table.set(row, column=4, value=new_q)
            self.table.set(row, column=5, value=each * new_q)
            self.products["quantity"][rn - 1] = new_q
            total = float(self.total.get())
            total -= float(quantity * each)
            total += float(int(entry.get()) * each)
            self.total.set("%.2f" % total)
            set_window.destroy()

        def __num_only(e):
            try:
                int(e.widget.get())
            except ValueError:
                e.widget.delete(e.widget.index(tk.INSERT) - 1)
        if event is None:
            row = self.popup.selection
        else:
            row = self.table.identify_row(event.y)
        if row != "":
            set_window = tk.Toplevel(self.master)
            set_window.title(t("Set Quantity"))
            set_window.geometry("340x50")
            set_window.resizable(False, False)
            set_window.attributes("-topmost", 1)
            set_window.grab_set()
            label = tk.Label(set_window, text=t("Quantity: "))
            entry = tk.Entry(set_window, width=20)
            rn = int(str(row).replace('I', ''))  # 序号
            quantity = self.products["quantity"][rn - 1]  # 原数量
            each = self.products["price"][rn - 1] * (1 - self.products["discount"][rn - 1] / 100)  # 原单价
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
        self.master = master
        self.LST = LST
        self.INFO = INFO
        self.total = total
        self.change = tk.StringVar()

        label_total = tk.Label(self.master, text=t("Total: "), font=(FONT, 20))
        self.total.set("0.00")
        label_number = tk.Label(self.master, textvariable=total, font=(FONT, 20))
        label_pay = tk.Label(self.master, text=t("Payment: "), font=(FONT, 20))
        self.entry_pay = tk.Entry(self.master, width=10, font=(FONT, 20))
        label_change = tk.Label(master, text=t("Change: "), font=(FONT, 20))
        self.change.set("0.00")
        label_change_num = tk.Label(self.master, textvariable=self.change, font=(FONT, 20))
        button_confirm = tk.Button(self.master, text=t("Confirm"), font=(FONT, 17), width=13, command=self.__confirm)

        label_total.grid(row=0, column=0, padx=20, pady=10, sticky="W")
        label_number.grid(row=0, column=1, sticky="W")
        label_pay.grid(row=1, column=0, padx=20, sticky="W")
        self.entry_pay.grid(row=1, column=1, sticky="W")
        label_change.grid(row=0, column=2, padx=10, sticky="W")
        label_change_num.grid(row=0, column=3, padx=10, sticky="W")
        button_confirm.grid(row=1, column=3, padx=30, pady=15, sticky="W")

        self.entry_pay.bind("<KeyRelease>", lambda event: self.__calc_change(event))
        self.entry_pay.bind("<Return>", lambda event: self.__confirm())

    def __calc_change(self, event):
        try:
            int(event.widget.get())
        except ValueError:
            event.widget.delete(event.widget.index(tk.INSERT) - 1)
        if self.entry_pay.get() != "":
            try:
                self.change.set("%.2f" % (float(self.entry_pay.get()) - float(self.total.get())))
            except ValueError:
                pass
        else:
            self.change.set("0.00")

    def __confirm(self):
        if self.entry_pay.get() == "":
            self.entry_pay.insert(0, 0)
        if float(self.total.get()) - float(self.entry_pay.get()) > 0:
            tk.messagebox.showwarning(title=t("Warning"), message=t("Payment Failure"))
        else:
            children = self.LST.table.get_children()
            try:
                query_bill = """
                INSERT INTO shop.bills
                (`Cashier ID`, Total, Datetime) 
                VALUE
                ({0}, {1}, '{2}')
                """.format(self.INFO.staff_code.get(), self.total.get(),
                           strftime("%Y-%m-%d %H:%M:%S", localtime()))
                CURSOR.execute(query_bill)
                CONNECTION.commit()
                for item in children:
                    row = self.LST.table.item(item)["values"]
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

                    CURSOR.execute("""
                    INSERT INTO shop.items
                    (`Bill ID`, `Product ID`, Quantity, `Selling Price`)
                    VALUES
                    ({0}, {1}, {2}, {3})
                    """.format(self.INFO.order_number.get(), row[1], row[4], row[2]))
                    CONNECTION.commit()
                self.INFO.order_number.set(str(int(self.INFO.order_number.get()) + 1))
                tk.messagebox.showinfo(t("Info"), t("Success"))
            except:
                CONNECTION.rollback()
                tk.messagebox.showerror(t("Error"), t("Error occur"))

            self.entry_pay.delete(0, "end")
            self.total.set("0.00")
            self.change.set("0.00")
            self.LST.table.delete(*self.LST.table.get_children())
            self.LST.products = {
                "description": [],
                "id": [],
                "price": [],
                "discount": [],
                "quantity": []
            }


class Entry:
    def __init__(self, master, Good):
        self.master = master
        self.GOOD = Good

        frame_top = tk.Frame(self.master)
        label_search = tk.Label(frame_top, text=t("Search："), font=(FONT, 20))
        self.entry_search = tk.Entry(frame_top, font=(FONT, 20))
        self.check = [tk.BooleanVar(), tk.BooleanVar()]
        self.check[0].set(1)
        checkbutton_id = tk.Checkbutton(self.master, var=self.check[0], text=t("ID"), font=(FONT, 12))
        checkbutton_name = tk.Checkbutton(self.master, var=self.check[1], text=t("Name"), font=(FONT, 12))

        frame_top.pack(side="top", fill="both", expand=True)
        label_search.pack(side="left", padx=20)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=10)
        checkbutton_id.pack(side="left", padx=200, pady=10)
        checkbutton_name.pack(side="left", padx=20, pady=10)

        self.entry_search.bind("<KeyRelease>", lambda event: self.__save_search())

    def __save_search(self):
        self.GOOD.clear_list()
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
        for each in output:
            self.GOOD.add_row(each[1], each[0], each[4], each[8])
        self.GOOD.get_table().update()


class Goods(TreeView):
    def __init__(self, master, LST):
        super().__init__()
        self.master = master
        self.LST = LST

        heading = (t("Product Description"), t("Product ID"), t("Price"), t("Discount"))
        self.alternative_table = tk.ttk.Treeview(self.master, height=40, show="headings", columns=heading)
        width = (200, 100, 80, 50)
        for i, each in enumerate(heading):
            self.alternative_table.column(each, width=width[i], anchor="center")
            self.alternative_table.heading(each, text=each)
        for col in heading:
            self.alternative_table.heading(col, text=col,
                                           command=lambda _col=col: self.sort_column(self.alternative_table,
                                                                                     _col, False))
        self.alternative_table.pack(fill="both")
        self.description = []
        self.good_id = []
        self.price = []
        self.discount = []

        self.VScroll = tk.Scrollbar(self.master, orient="vertical", command=self.alternative_table.yview)
        self.VScroll.place(relx=0.978, rely=0.025, relwidth=0.02, relheight=0.958)
        self.alternative_table.configure(yscrollcommand=self.VScroll.set)

        self.alternative_table.bind("<Double-1>", lambda event: self.__get_row())

    def __get_row(self):
        for item in self.alternative_table.selection():
            row = self.alternative_table.item(item, "values")
            self.add_to_list(row[0], int(row[1]), float(row[2]), int(row[3]), 1)

    def get_table(self):
        return self.alternative_table

    def add_to_list(self, description, product_id, price, discount, quantity):
        if product_id not in self.LST.products["id"]:
            self.LST.products["description"].append(description)
            self.LST.products["id"].append(product_id)
            self.LST.products["price"].append(price)
            self.LST.products["discount"].append(discount)
            self.LST.products["quantity"].append(quantity)
            subtotal = float(price * (1 - (discount / 100)) * quantity)
            self.LST.table.insert('', len(self.LST.products["description"]) - 1,
                                  values=(description, product_id, price,
                                          discount, quantity, subtotal))
            self.LST.table.update()
            self.LST.total.set("%.2f" % (float(self.LST.total.get()) + subtotal))

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
