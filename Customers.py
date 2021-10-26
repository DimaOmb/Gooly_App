from Control_Functions import *

def set_customer_tab(tab):

    selected_customer = {
                    "cust_id": StringVar(),
                    "name": StringVar(),
                    "contact_name": StringVar(),
                    "phone_number": StringVar(),
                    "city": StringVar(),
                   "address_street": StringVar(),
                   "address_house": StringVar(),
                   "address_appartment" : StringVar(),
                   "address_entrence": StringVar()
    }

    """----------------------1. Entry Frame ----------------------"""
    entry_frame = LabelFrame(tab, padx=10, pady=10)
    entry_frame.grid(column=0, row=0, padx=10, pady=10)

    for i, col in enumerate(selected_customer.keys()):
        Label(entry_frame, text = col).grid(row=0, column=i)

        if col == "cust_id":
            Label(entry_frame, textvariable=selected_customer["cust_id"]).grid(row=1, column=i)
        elif col == "city":
            city_data = get_data_for_drop_down(DB_table='city', DB_column='name')
            ttk.Combobox(entry_frame, value=city_data, justify = CENTER, textvariable=selected_customer[col],state="readonly").grid(row=1, column=i)
        else:
            Entry(entry_frame, textvariable = selected_customer[col], justify = CENTER).grid(row=1, column = i)


    """----------------------2. Table Frame ----------------------"""
    table_frame = LabelFrame(tab, padx=10, pady=10)
    table_frame.grid(column=0, row=1, padx=10, pady=10)
    columns = ["cust_id", "name", "contact_name", "phone_number", "city", "address_street", "address_house", "address_appartment",
     "address_entrence"]
    cust_table = create_gui_table(table_frame, columns)
    cust_table.pack()
    get_data_and_renew_gui_table(DB_table="customers", DB_columns=columns, gui_table=cust_table)

    cust_table.bind("<<TreeviewSelect>>",
                    lambda event, tbl=cust_table: populate_entries_with_selected_row(tbl, selected_customer))

    """----------------------3. buttons Frame ----------------------"""
    button_frame = LabelFrame(tab, padx=10, pady=10)
    button_frame.grid(column=0, row=2, padx=10, pady=10)
    Button(button_frame, text = "Clear", command = lambda : btn_click_clear(table=cust_table,
                                                                            select_from_table_DB="customers",
                                                                            DB_columns=columns,
                                                                            selected_values_dict=selected_customer)).grid(column=0, row=0, padx=5)

    Button(button_frame, text = "Update", command = lambda: btn_click_update(cust_table,
                                                                             selected_customer,
                                                                             db_update_function=update_customer_in_DB,
                                                                             index_col="cust_id",
                                                                             select_from_table_DB = "customers",
                                                                             DB_columns = "*",
                                                                             entity_name = "customer")).grid(column=1, row=0, padx=5)

    Button(button_frame, text = "Remove", command = lambda: btn_click_remove(table_gui=cust_table,
                                            remove_from_table_DB="customers",
                                            select_from_table_DB="customers",
                                            DB_columns=columns,
                                            index_dict={"cust_id": selected_customer["cust_id"].get()},
                                            entity_name="Customer",
                                            chosen_entity_to_nullify = selected_customer
                                            )).grid(column=2, row=0, padx=5)

    Button(button_frame, text = "Add New", command = lambda: btn_click_add_new(table=cust_table,
                                                                               values_dict = selected_customer,
                                                                               index_col= 'cust_id',
                                                                               entity_name = 'Customer',
                                                                               db_insert_function = add_new_customer_to_DB,
                                                                               select_from_table_DB = "customers",
                                                                               DB_columns = columns)).grid(column=3, row=0, padx=5)

