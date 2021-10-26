from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from DB_functions import *

"""--------------------- Main functions ---------------------"""
def set_values_to_entries(selceted_dict_arg, values_dict = None):
    if type(values_dict) == type(dict()):
        for col in values_dict.keys():
            selceted_dict_arg[col].set(values_dict[col])
    else:
        for col in selceted_dict_arg.keys():
            selceted_dict_arg[col].set("")

def populate_entries_with_selected_row(table, select_row):
    ans = get_values_of_selected_row(table)
    set_values_to_entries(select_row, ans)

def create_gui_table(tab, columns):

    table = ttk.Treeview(tab, columns=columns)

    # Formate Our Columns + Create Headings
    table.column("#0", width=0, stretch=NO)
    table.heading("#0", text="", anchor=CENTER)
    for col in table['columns']:
        table.heading(col, text=col, anchor=CENTER)
        if "id" in col:
            table.column(col, anchor=CENTER,width = 50, stretch=NO)
        else:
            table.column(col, anchor=CENTER, width = 120, minwidth=10, stretch=YES)

    table.tag_configure('odd_row', background='lightblue')
    table.tag_configure('even_row', background='white')

    return table

def populate_table(table, data):
    for i, row in enumerate(data):
        tag = 'odd_row'
        if i % 2 == 0 :
            tag = 'even_row'
        table.insert(parent='', index='end', values=row, tags=(tag,))

def empty_table(table_name):
    for record in table_name.get_children():
        table_name.delete(record)

def renew_gui_table(table_name, data):
    empty_table(table_name)
    populate_table(table_name, data)

def get_data_and_renew_gui_table(DB_table, DB_columns, gui_table):
    data, columns = get_DB_table_data(DB_table, DB_columns)
    renew_gui_table(gui_table, data)

def get_data_and_renew_gui_table_and_clear_entires(DB_table, DB_columns, gui_table, values_dict):
    get_data_and_renew_gui_table(DB_table, DB_columns, gui_table)
    set_values_to_entries(values_dict)

def get_values_of_selected_row(table):
    selected_row = table.focus()
    values = table.item(selected_row, 'values')
    ans = {table['columns'][i]: val for i, val in enumerate(values)}
    return ans

def get_data_for_drop_down(DB_table, DB_column):
    data_dirty, column = get_DB_table_data(DB_table, [DB_column])
    return [_[0] for _ in data_dirty]
"""--------------------- Button Click functions ---------------------"""

def btn_click_clear(table, select_from_table_DB, DB_columns, selected_values_dict):
    get_data_and_renew_gui_table_and_clear_entires(DB_table=select_from_table_DB,
                                                   DB_columns=DB_columns,
                                                   gui_table=table,
                                                   values_dict=selected_values_dict)

def btn_click_update(table, values_dict, index_col, entity_name, db_update_function, select_from_table_DB, DB_columns ):
    if values_dict[index_col].get() == "":
        showwarning(title=f"{entity_name} Update", message=f"choose {entity_name}")
    else:
        status, details = db_update_function(values_dict)
        if status == "OK":
            get_data_and_renew_gui_table_and_clear_entires(DB_table=select_from_table_DB,
                                                           DB_columns=DB_columns,
                                                           gui_table=table,
                                                           values_dict=values_dict)
        else:
            showwarning(title=f"{entity_name} Update", message=details.msg)

def btn_click_remove(table_gui, remove_from_table_DB, select_from_table_DB, DB_columns, index_dict, entity_name, chosen_entity_to_nullify):
    if list(index_dict.values())[0] !="":
        status, details = remove_row_in_DB_table(remove_from_table_DB, index_dict)
        if status == "OK":
            get_data_and_renew_gui_table_and_clear_entires(DB_table=select_from_table_DB, DB_columns=DB_columns, gui_table=table_gui,
                                                           values_dict=chosen_entity_to_nullify)
        else:
            showwarning(title=f"{entity_name} Remove", message=details.msg)
    else:
        showwarning(title=f"{entity_name} Remove", message=f"Choose {entity_name}")

def btn_click_add_new(table, values_dict, index_col, entity_name, db_insert_function, select_from_table_DB, DB_columns):
    status, details = db_insert_function(values_dict)
    if status == "OK":
        get_data_and_renew_gui_table_and_clear_entires(DB_table = select_from_table_DB, DB_columns =DB_columns, gui_table = table, values_dict = values_dict)
    else:
        showwarning(title=f"{entity_name} Insert", message=details.msg)

"""--------------------- Payment functions ---------------------"""
def renew_payments_with_customer_filter(gui_table, customer_filter, selected_payment):
    set_values_to_entries(selected_payment)
    where_select = {"customer = %s ":customer_filter}
    payment_data, _ = get_DB_table_data("payment_for_gui_view", ['payment_id','customer', 'payment_date', 'payment_sum'], where_IS_dict = False, where_dict=where_select)
    renew_gui_table(gui_table, payment_data)

def btn_click_clear_payments(table, select_from_table_DB, DB_columns, selected_values_dict, chosen_customer):
    btn_click_clear(table, select_from_table_DB, DB_columns, selected_values_dict)
    chosen_customer.set("")

def btn_click_remove_payments(table_gui, remove_from_table_DB, select_from_table_DB, DB_columns, index_dict, entity_name,
                              chosen_entity_to_nullify, chosen_customer, order_gui_table):
    btn_click_remove(table_gui, remove_from_table_DB, select_from_table_DB, DB_columns, index_dict, entity_name, chosen_entity_to_nullify)
    chosen_customer.set("")
    payment_order_data, payment_order_columns = get_DB_table_data("order_for_payment_gui_view", ["*"])
    renew_gui_table(order_gui_table, payment_order_data)

def btn_click_update_payment(table, values_dict, index_col, entity_name, db_update_function,
                             select_from_table_DB, DB_columns, order_gui_table ):
    btn_click_update(table, values_dict, index_col, entity_name, db_update_function, select_from_table_DB, DB_columns)
    payment_order_data, payment_order_columns = get_DB_table_data("order_for_payment_gui_view", ["*"])
    renew_gui_table(order_gui_table, payment_order_data)

def btn_click_add_new_payment(table, values_dict, index_col, entity_name, db_insert_function, select_from_table_DB, DB_columns, chosen_customer):
    status, details = db_insert_function(values_dict, chosen_customer)
    if status == "OK":
        get_data_and_renew_gui_table_and_clear_entires(DB_table = select_from_table_DB, DB_columns = DB_columns, gui_table = table, values_dict = values_dict)
        chosen_customer.set('')
    else:
        showwarning(title=f"{entity_name} Insert", message=details.msg)

def bind_payment_to_orders(order_table, selected_payment):
    payment_id = selected_payment["payment_id"].get()
    selected_orders_ids = []
    for row in order_table.selection():
        selected_orders_ids.append((order_table.item(row)["values"][0]))

    if payment_id is None or len(selected_orders_ids) == 0:
        showwarning(title=f"Selection Error", message="No elements selected")
    else:
        status, details = update_orders_bind_to_payemnts_DB(payment_id, order_ids = selected_orders_ids)
        if status == "OK":
            payment_order_data, payment_order_columns = get_DB_table_data("order_for_payment_gui_view", ["*"])
            renew_gui_table(order_table, payment_order_data)
        else:
            showwarning(title=f"Bind Error", message=details.msg)

def unbind_payment_from_orders(order_table):
    selected_orders_ids = []
    for row in order_table.selection():
        selected_orders_ids.append((order_table.item(row)["values"][0]))
    if len(selected_orders_ids) == 0:
        showwarning(title=f"Selection Error", message="No elements selected")
    else:
        status, details = update_orders_UNbind_order_payment(order_ids=selected_orders_ids)
        if status == "OK":
            payment_order_data, payment_order_columns = get_DB_table_data("order_for_payment_gui_view", ["*"])
            renew_gui_table(order_table, payment_order_data)
        else:
            showwarning(title=f"Bind Error", message=details.msg)