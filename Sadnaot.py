from Control_Functions import *


def set_sadnaot_tab(tab):
    selected_sadna = {"sadna_id": StringVar(),
                      "name": StringVar(),
                      "description": StringVar(),
                      "duration": StringVar(),
                      "base_cost": StringVar(),
                      "base_price": StringVar()}

    """----------------------1. Entry Frame ----------------------"""
    sadna_entry_frame = LabelFrame(tab, padx=10, pady=10)
    sadna_entry_frame.grid(column=0, row=0, padx=10, pady=10)

    for i, col in enumerate(selected_sadna.keys()):
        Label(sadna_entry_frame, text = col).grid(row=0, column=i)
        if col == "sadna_id":
            Label(sadna_entry_frame, textvariable=selected_sadna[col]).grid(row=1, column=i)
        else:
            Entry(sadna_entry_frame, textvariable=selected_sadna[col], justify=CENTER).grid(row=1, column=i)

    """----------------------2. Table Frame ----------------------"""
    sadna_table_frame = LabelFrame(tab, padx=10, pady=10)
    sadna_table_frame.grid(column=0, row=1, padx=10, pady=10)

    columns = ["sadna_id", "name", "description", "duration", "base_cost", "base_price"]
    sadna_table = create_gui_table(sadna_table_frame, columns)
    get_data_and_renew_gui_table(DB_table="sadnaot", DB_columns=columns, gui_table=sadna_table)

    sadna_table.pack()
    sadna_table.bind("<<TreeviewSelect>>", lambda event: populate_entries_with_selected_row(sadna_table, selected_sadna))

    """----------------------3. buttons Frame ----------------------"""
    button_frame = LabelFrame(tab, padx=10, pady=10)
    button_frame.grid(column=0, row=2, padx=10, pady=10)
    Button(button_frame, text="Clear", command=lambda: btn_click_clear(table=sadna_table,
                                                                       select_from_table_DB = "sadnaot",
                                                                       DB_columns = columns,
                                                                       selected_values_dict=selected_sadna)).grid(column=0, row=0, padx=5)

    Button(button_frame, text="Update", command=lambda: btn_click_update(sadna_table,
                                                                             selected_sadna,
                                                                             db_update_function=update_sadna_in_DB,
                                                                             index_col="sadna_id",
                                                                             select_from_table_DB = "sadnaot",
                                                                             DB_columns = columns,
                                                                             entity_name = "Sadna")

           ).grid(column=1, row=0, padx=5)
    Button(button_frame, text="Remove", command=lambda: btn_click_remove(
                                                                            table_gui = sadna_table,
                                                                            remove_from_table_DB = "sadnaot",
                                                                            select_from_table_DB = "sadnaot",
                                                                            DB_columns = columns,
                                                                            index_dict = {"sadna_id": selected_sadna["sadna_id"].get()},
                                                                            entity_name = "Sadna",
                                                                            chosen_entity_to_nullify= selected_sadna)
           ).grid(column=2, row=0, padx=5)


    Button(button_frame, text="Add New", command=lambda: btn_click_add_new(table=sadna_table,
                                                                               values_dict = selected_sadna,
                                                                               index_col= 'sadna_id',
                                                                               entity_name = 'Sadna',
                                                                               db_insert_function = add_new_sadna_to_DB,
                                                                               select_from_table_DB = "sadnaot",
                                                                               DB_columns = columns)).grid(column=3, row=0, padx=5)

