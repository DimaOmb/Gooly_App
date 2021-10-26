import mysql.connector
import sys

highlight = 20 * "-"

def activate_DB_con():
    try:
        global conn_gooly
        global CURSOR
        conn_gooly = mysql.connector.connect(host="localhost", user="root", password="1234", database="Gooly")
        conn_gooly.autocommit = True
        CURSOR = conn_gooly.cursor()
    except  mysql.connector.DatabaseError:
        print(f"{highlight} DB connection ERROR {highlight}")
        print(sys.exc_info())

def clean_val(val):
    if val in ["None", ""]:
        return None
    return val

def correct_values_for_DB(val_dict, keys_to_remove: list = []):
    return {col: clean_val(var.get()) for col, var in val_dict.items() if col not in keys_to_remove}

"""--------------------- main SQL functions ---------------------"""
def get_DB_table_data(db_table_name, columns, where_IS_dict = True, where_dict = {}):
    """

    :param db_table_name:
    :param columns:
    :param where_dict: col:value to filer by
    :return:
    """
    try:
        sql_where = ""
        if not where_IS_dict: # where_dict is string
            sql_where = "where " + " and ".join(list(where_dict.keys()))
            where_values = list(where_dict.values())
            CURSOR.execute(f'SELECT {", ".join(columns)} FROM {db_table_name} {sql_where};', where_values)

        elif bool(where_dict): # not empty
            sql_where = " where " + " and ".join([f"{col} = %s" for col in where_dict.keys()])
            where_values = list(where_dict.values())
            CURSOR.execute(f'SELECT {", ".join(columns)} FROM {db_table_name}{sql_where};', where_values)

        else:
            CURSOR.execute(f'SELECT {", ".join(columns)} FROM {db_table_name};')
        ans = CURSOR.fetchall()
        return ans, CURSOR.column_names
    except mysql.connector.Error as err:
        print(f"{highlight} QUERY ERROR {highlight}")
        print(err)  # full text error
        print(CURSOR.statement)
        print(sys.exc_info())

        print( 3 * highlight)

def update_record_in_DB_table(db_table_name, rec_index_dict, value_dict):
    """

    :param db_table_name:
    :param rec_index_dict: {index_col: value}
    :param value_dict: {col_name: value}
    :return:
    """
    sql_set = ", ".join([f"{col} = %s" for col in value_dict.keys()])
    sql_where =  " and ".join([f"{col} = %s" for col in rec_index_dict.keys()])
    values = list(value_dict.values()) + list(rec_index_dict.values())
    sql = f"update {db_table_name} set {sql_set} where {sql_where};"
    try:
        CURSOR.execute(sql, values)
        return "OK", CURSOR.lastrowid

    except mysql.connector.Error as err:
        print(f"{highlight} Update Error {highlight}")
        print(err)
        print(CURSOR.statement)
        return "ERROR", err

def remove_row_in_DB_table(db_table_name, rec_index_dict):
    sql_where =  " and ".join([f"{col} = %s" for col in rec_index_dict.keys()])
    sql = f"DELETE FROM {db_table_name} where {sql_where};"
    try:
        CURSOR.execute(sql, list(rec_index_dict.values()))
        return "OK", CURSOR.lastrowid

    except mysql.connector.Error as err:
        print(f"{highlight} Delete Error {highlight}")
        print(err)
        print(CURSOR.statement)

        return "ERROR", err

def add_new_row_to_DB_table(db_table_name, value_dict):
    columns = ", ".join(value_dict.keys())
    sql = f'insert into {db_table_name} ({columns}) values ({",".join(["%s"] * len(value_dict.keys()))})'
    values = list(value_dict.values())
    try:
        CURSOR.execute(sql, values)
        return "OK", CURSOR.lastrowid
    except mysql.connector.Error as err:
        print(f"{highlight} Insert Error {highlight}")
        print(err)
        print(CURSOR.statement)
        return "ERROR", err

"""--------------------- Sadnaot SQL functions ---------------------"""
def update_sadna_in_DB(sadna_dict):
    index = {"sadna_id": sadna_dict["sadna_id"].get()}
    values = correct_values_for_DB(sadna_dict, keys_to_remove=['sadna_id'])
    return update_record_in_DB_table("sadnaot", index, values)

def add_new_sadna_to_DB(sadna_dict):
    values = correct_values_for_DB(sadna_dict, keys_to_remove=['sadna_id'])
    return add_new_row_to_DB_table("sadnaot", values)

"""--------------------- Customer SQL functions ---------------------"""
def add_new_customer_to_DB(customer_dict):
    values = correct_values_for_DB(customer_dict, keys_to_remove = ['cust_id'])
    return add_new_row_to_DB_table("customers", values)

def update_customer_in_DB(customer_dict):
    index = {"cust_id": customer_dict["cust_id"].get()}
    values = correct_values_for_DB(customer_dict, keys_to_remove=['cust_id'])
    return update_record_in_DB_table("customers", index, values)


"""----------------------- Orders SQL functions ----------------------------------------------"""

def add_new_order_to_DB(order_dict):
    values = correct_values_for_DB(order_dict, keys_to_remove=["order_id", 'payment_date', 'location'])
    values['payment_id'] = None
    values_for_sql = order_values_for_sql(values)

    sql_insert_query = f"insert into orders ({', '.join(values_for_sql.keys())}) values ({', '.join(values_for_sql.values())})"
    try:
        CURSOR.execute(sql_insert_query, [val for col, val in values.items()])
        return "OK", CURSOR.lastrowid
    except mysql.connector.Error as err:
        print(f"{highlight} Insert Error {highlight}")
        print(err)
        print(CURSOR.statement)
        return "ERROR", err

def update_order_in_DB(order_dict):
    values = correct_values_for_DB(order_dict, keys_to_remove=["order_id", 'payment_date', 'location'])
    values_for_sql = order_values_for_sql(values)

    sql_update_query = f"update orders set {', '.join([f'{col} = {val}' for col, val in values_for_sql.items()])} where order_id = %s"
    try:
        CURSOR.execute(sql_update_query, [*values.values(), order_dict["order_id"].get()])
        return "OK", CURSOR.lastrowid
    except mysql.connector.Error as err:
        print(f"{highlight} Update Error {highlight}")
        print(err)
        print(CURSOR.statement)
        return "ERROR", err

def order_values_for_sql(values_dict):
    values_for_sql = {}
    for col, val in values_dict.items():
        if col == "customer":
            values_for_sql['cust_id'] = "(select cust_id from customers where name = %s)"
        elif col == "sadna":
            values_for_sql['sadna_id'] = "(select sadna_id from sadnaot where name = %s)"
        else:
            values_for_sql[col] = "%s"
    return values_for_sql
"""----------------------- Payments SQL functions ----------------------------------------------"""

def update_payemnt_in_DB(payment_dict):
    index = {"payment_id": payment_dict["payment_id"].get()}
    values = correct_values_for_DB(payment_dict, keys_to_remove=["payment_id"])
    values.pop('customer')
    return update_record_in_DB_table("payments", index, values)

def add_new_payment_to_DB(payment_dict, chosen_customer):
    DB_values = correct_values_for_DB(payment_dict, keys_to_remove=["payment_id", 'customer'])
    values_for_sql = {col: "%s" for col in DB_values.keys() }
    values_for_sql['cust_id'] = "(select cust_id from customers where name = %s)"

    sql_insert_query = f"insert into payments ({', '.join(values_for_sql.keys())}) values ({', '.join(values_for_sql.values())})"
    try:
        values_for_execute = list(DB_values.values())
        customer_name = chosen_customer.get()
        if customer_name == "":
            customer_name = None
        values_for_execute.append(customer_name)
        CURSOR.execute(sql_insert_query, values_for_execute)
        return "OK", CURSOR.lastrowid
    except mysql.connector.Error as err:
        print(f"{highlight} Insert Error {highlight}")
        print(err)
        print(CURSOR.statement)
        return "ERROR", err

def update_orders_bind_to_payemnts_DB(payment_id, order_ids):
    try:
        sql_query = f"update orders set payment_id = %s where order_id in ({', '.join(['%s'] * len(order_ids))});"
        CURSOR.execute(sql_query, [payment_id, *order_ids])
        return "OK", CURSOR.lastrowid
    except mysql.connector.Error as err:
        print(f"{highlight} Update Error {highlight}")
        print(err)
        print(CURSOR.statement)
        return "ERROR", err

def update_orders_UNbind_order_payment(order_ids):
    try:
        sql_query = f"update orders set payment_id = null where order_id in ({', '.join(['%s'] * len(order_ids))});"
        CURSOR.execute(sql_query, order_ids)
        return "OK", CURSOR.lastrowid
    except mysql.connector.Error as err:
        print(f"{highlight} Update Error {highlight}")
        print(err)
        print(CURSOR.statement)
        return "ERROR", err

