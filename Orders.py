from Control_Functions import *

def set_order_tab(tab):
    selected_order = {"order_id": StringVar(),
                      "sadna": StringVar(),
                      "customer": StringVar(),
                      "start_time": StringVar(),
                      "order_date": StringVar(),
                      "location": StringVar(),
                      "price": StringVar(),
                      "taxi_cost": StringVar(),
                      "payment_date": StringVar()
                      }
    sadnaot_customer_data = {
        'sadna': get_data_for_drop_down(DB_table="sadnaot", DB_column ="name"),
        'customer': get_data_for_drop_down(DB_table="customers", DB_column ="name")
    }

    """----------------------1. Entry Frame ----------------------"""
    order_entry_frame = LabelFrame(tab, padx=10, pady=10)
    order_entry_frame.grid(column=0, row=0, padx=10, pady=10)

    for i, col in enumerate(selected_order.keys()):
        Label(order_entry_frame, text = col).grid(row=0, column=i)

        if col in ["order_id", 'location', "payment_date"] :
            Label(order_entry_frame, textvariable=selected_order[col]).grid(row=1, column= i)
        elif col in ['sadna', 'customer']:
            ttk.Combobox(order_entry_frame,
                         value=sadnaot_customer_data[col],
                         textvariable=selected_order[col],
                         justify=CENTER,
                         state="readonly").grid(row=1, column=i)
        else:
            Entry(order_entry_frame,
                  textvariable=selected_order[col],
                  justify=CENTER).grid(row=1, column=i)


    """----------------------2. Table Frame ----------------------"""
    order_table_frame = LabelFrame(tab, padx=10, pady=10)
    order_table_frame.grid(column=0, row=1, padx=10, pady=10)

    order_columns = ["order_id", "sadna", "customer", "start_time", "order_date", "location", "price", "taxi_cost", "payment_date"]

    order_table = create_gui_table(order_table_frame, order_columns)
    order_table.pack()
    get_data_and_renew_gui_table(DB_table="orders_for_gui_view", DB_columns=order_columns, gui_table=order_table)

    order_table.bind("<<TreeviewSelect>>", lambda event,: populate_entries_with_selected_row(order_table, selected_order))

    """----------------------3. Buttons Frame ----------------------"""
    order_btn_frame = LabelFrame(tab, padx=10, pady=10)
    order_btn_frame.grid(column=0, row=2, padx=10, pady=10)
    Button(order_btn_frame, text="Clear", command = lambda: btn_click_clear(table=order_table,
                                                                            select_from_table_DB="orders_for_gui_view",
                                                                            DB_columns=order_columns,
                                                                            selected_values_dict=selected_order)).grid(column=0, row=0, padx=5)
    Button(order_btn_frame, text="Remove",command = lambda: btn_click_remove(
               table_gui=order_table,
               remove_from_table_DB="orders",
               select_from_table_DB="orders_for_gui_view",
               DB_columns = ["*"],
               index_dict= {"order_id": selected_order["order_id"].get()},
               entity_name="Order",
               chosen_entity_to_nullify = selected_order)).grid(column=2, row=0, padx=5)

    Button(order_btn_frame, text="Update", command = lambda:btn_click_update(
                                                            table = order_table,
                                                            values_dict = selected_order,
                                                            index_col = 'order_id',
                                                            entity_name = 'Order',
                                                            db_update_function = update_order_in_DB,
                                                            select_from_table_DB = "orders_for_gui_view",
                                                            DB_columns = ["*"])).grid(column=1, row=0, padx=5)

    Button(order_btn_frame, text="Add New", command = lambda: btn_click_add_new(
                                                            table = order_table,
                                                            values_dict = selected_order,
                                                            index_col = 'order_id',
                                                            entity_name = 'Order',
                                                            db_insert_function = add_new_order_to_DB,
                                                            select_from_table_DB = "orders_for_gui_view",
                                                            DB_columns = ["*"])).grid(column=3, row=0, padx=5)


