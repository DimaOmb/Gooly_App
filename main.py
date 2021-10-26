from tkinter import *
from tkinter import ttk
from DB_functions import *
from Sadnaot import set_sadnaot_tab
from Customers import set_customer_tab
from Orders import set_order_tab
from Payments import set_payments_tab

def resize_window_and_refresh_data():
    """
        get the selected tab, refresh the content and resize the window accordingly

    :return: None
    """
    # Enter event loop until all idle callbacks have been called.
    # This will update the display of windows but not process events caused by the user.
    notebook.update_idletasks()

    # get selected tab
    selected_tab = notebook.nametowidget(notebook.select())
    tab_name = selected_tab._name

    # for tab update
    tab_functions = {'sadnaot_tab': set_sadnaot_tab,
                     'customers_tab': set_customer_tab,
                     'payment_tab': set_payments_tab,
                     'orders_tab': set_order_tab
                     }

    # remove all widgets from the selected tab
    for widget_obj in selected_tab.winfo_children():
        widget_obj.destroy()

    # re-create all widgets in the selected tab
    tab_functions[tab_name](selected_tab)

    # change window size accordingly
    notebook.configure(height=selected_tab.winfo_reqheight(), width = int(1.05 * selected_tab.winfo_reqwidth()))

root = Tk()
root.title('Gooly')
root.geometry("+10+10")


# change password to the password in of your connection
activate_DB_con()

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=TRUE)

sadnaot_tab = Frame(notebook, name ="sadnaot_tab")
customers_tab = Frame(notebook, name ="customers_tab")
orders_tab = Frame(notebook, name ='orders_tab')
payment_tab = Frame(notebook, name ='payment_tab')

notebook.bind("<<NotebookTabChanged>>", lambda event: resize_window_and_refresh_data())
notebook.add(sadnaot_tab, text="סדנאות")
notebook.add(customers_tab, text="לקוחות")
notebook.add(orders_tab, text="הזמנות")
notebook.add(payment_tab, text="תשלומים")

set_sadnaot_tab(sadnaot_tab)
set_customer_tab(customers_tab)
set_order_tab(orders_tab)
set_payments_tab(payment_tab)

# tabControl.select(payment_tab)


root.mainloop()

