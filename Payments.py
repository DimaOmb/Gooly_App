from Control_Functions import *


def set_payments_tab(tab):
    customers = get_data_for_drop_down(DB_table='customers', DB_column='name')

    selected_payment = {
            'payment_id': StringVar(), 'customer': StringVar(), 'payment_date': StringVar(), 'payment_sum': StringVar()
            }
    chosen_customer = StringVar()

    left_side = LabelFrame(tab, padx=1, pady=1)
    left_side.grid(row=0, column=0)

    """----------------------1. Entry Frame ----------------------"""
    payment_entry_frame = LabelFrame(left_side, padx=5, pady=5)
    payment_entry_frame.grid(column=0, row=0, padx=5, pady=5)

    # ------ row 0 ------
    Label(payment_entry_frame, text="Select Customer").grid(row=0, column=0)
    customer_select = ttk.Combobox(payment_entry_frame, value=customers, textvariable=chosen_customer, justify=CENTER,
                                   state="readonly")
    customer_select.grid(row=0, column=1)

    # ------ row 1 ------
    Label(payment_entry_frame, text="ID").grid(row=1, column=0)
    Label(payment_entry_frame, text="Customer").grid(row=1, column=1)
    Label(payment_entry_frame, text="payment_date").grid(row=1, column=2)
    Label(payment_entry_frame, text="payment_sum").grid(row=1, column=3)

    # ------ row 2 ------
    Label(payment_entry_frame, textvariable=selected_payment["payment_id"]).grid(row=2, column=0)
    Label(payment_entry_frame, textvariable=selected_payment["customer"], justify=CENTER).grid(row=2, column=1)
    Entry(payment_entry_frame, textvariable=selected_payment['payment_date'], justify=CENTER).grid(row=2, column=2)
    Entry(payment_entry_frame, textvariable=selected_payment['payment_sum'], justify=CENTER).grid(row=2, column=3)

    """----------------------2. Payment Table Frame ----------------------"""
    payment_table_frame = LabelFrame(left_side, padx=10, pady=10, text="Payments")
    payment_table_frame.grid(column=0, row=1, pady=5)
    payments_columns = ['payment_id', 'customer', 'payment_date', 'payment_sum']
    # payments_data, payments_columns = get_DB_table_data("order_for_payment_gui_view", payments_columns)



    payment_table = create_gui_table(payment_table_frame, payments_columns)
    payment_table.pack()
    payment_order_columns = ["order_id", "customer", "sadna", "order_date", "total_price", "payment_sum",
                             "payment_date"]
    get_data_and_renew_gui_table(DB_table="order_for_payment_gui_view",
                                 DB_columns=payment_order_columns,
                                 gui_table=payment_table)

    # populate_table(payment_table, payments_data)
    payment_table.bind("<<TreeviewSelect>>",
                       lambda event, tbl=payment_table: populate_entries_with_selected_row(tbl, selected_payment))

    customer_select.bind("<<ComboboxSelected>>",
                         lambda event: renew_payments_with_customer_filter(payment_table, customer_select.get(),
                                                                           selected_payment))

    """----------------------3. Orders Table Frame ----------------------"""
    payment_orders_frame = LabelFrame(tab, padx=10, pady=10, text='Orders')
    payment_orders_frame.grid(column=1, row=0, padx=10, pady=10, sticky=N)


    order_table = create_gui_table(payment_orders_frame, payment_order_columns)
    order_table.grid(column=0, row=1)
    get_data_and_renew_gui_table(DB_table="order_for_payment_gui_view", DB_columns=payment_order_columns,
                                 gui_table=order_table)

    """----------------------4. Payments Button Frame ----------------------"""
    payment_btn_frame = LabelFrame(left_side)
    payment_btn_frame.grid(column=0, row=2, padx=5, pady=5)

    Button(payment_btn_frame, text="Clear", command=lambda: btn_click_clear_payments(table=payment_table,
                                                                                     select_from_table_DB="order_for_payment_gui_view",
                                                                                     DB_columns=payment_order_columns,
                                                                                     selected_values_dict=selected_payment,
                                                                                     chosen_customer=chosen_customer)).grid(
            column=0, row=0, padx=5, pady=10)
    Button(payment_btn_frame, text="Remove",
           command=lambda: btn_click_remove_payments(table_gui=payment_table, remove_from_table_DB="payments",
                                                     select_from_table_DB="order_for_payment_gui_view",
                                                     DB_columns=payment_order_columns,
                                                     index_dict={"payment_id": selected_payment["payment_id"].get()},
                                                     entity_name="Payment", chosen_entity_to_nullify=selected_payment,
                                                     chosen_customer=chosen_customer,
                                                     order_gui_table=order_table)).grid(column=1, row=0, padx=5,
                                                                                        pady=10)

    Button(payment_btn_frame, text="Add Payment",
           command=lambda: btn_click_add_new_payment(table=payment_table, values_dict=selected_payment,
                                                     index_col='payment_id', entity_name='Payment',
                                                     db_insert_function=add_new_payment_to_DB,
                                                     select_from_table_DB="order_for_payment_gui_view",
                                                     DB_columns=payment_order_columns,
                                                     chosen_customer=chosen_customer)).grid(column=2, row=0, padx=5,
                                                                                            pady=10)

    Button(payment_btn_frame, text="Update", command=lambda: btn_click_update_payment(payment_table, selected_payment,
                                                                                      db_update_function=update_payemnt_in_DB,
                                                                                      index_col="payment_id",
                                                                                      select_from_table_DB="order_for_payment_gui_view",
                                                                                      DB_columns=payment_order_columns,
                                                                                      entity_name="Payment",
                                                                                      order_gui_table=order_table)).grid(
            column=3, row=0, padx=5, pady=10)

    """----------------------5. Orders Button Frame ----------------------"""
    payment_order_btn_frame = LabelFrame(payment_orders_frame, borderwidth=0)
    payment_order_btn_frame.grid(column=0, row=2, padx=10, pady=10)
    Button(payment_order_btn_frame, text="Bind",
           command=lambda: bind_payment_to_orders(order_table, selected_payment)).grid(column=0, row=0, padx=5, pady=10)
    Button(payment_order_btn_frame, text="UN - Bind ", command=lambda: unbind_payment_from_orders(order_table)).grid(
            column=1, row=0, padx=5, pady=10)