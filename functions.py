import tkinter as tk
from tkinter import ttk
from database_manager import * 
from tkinter import END
from error_handling import *

def show_selection(main_treeview: ttk.Treeview, name_entry:tk.Entry, initiative_entry: tk.Entry, ac_entry: tk.Entry, selection_entry: tk.Entry, hp_entry: tk.Entry):
    """Update entry widgets with the selected values from a Treeview

    Args:
        main_treeview (ttk.Treeview): The main Treeview widget containing the data
        name_entry (tk.Entry): Entry widget for displaying/editing the selected name
        initiative_entry (tk.Entry): Entry widget for displaying/editing the selected initiative.
        ac_entry (tk.Entry): Entry widget for displaying/editing the selected armor class (ac).
        selection_entry (tk.Entry): Entry widget for displaying the selected item's identifier.
        hp_entry (tk.Entry): Entry widget for displaying/editing the selected hit points (hp).

    If the selected item cannot be retrieved or an error occurs, the function gracefully handles the exception and does nothing.
    """

    try:
        curItem = main_treeview.focus()
        dict = (main_treeview.item(curItem))
        values = dict["values"]

        id = values[0]
        name = values[1]
        initiative = values[2]
        ac = values[3]
        hp = values[5]

        name_entry.delete(0,END)
        name_entry.insert(0, f"{name}")

        initiative_entry.delete(0,END)
        initiative_entry.insert(0, f"{initiative}")

        ac_entry.delete(0,END)
        ac_entry.insert(0, f"{ac}")

        hp_entry.delete(0,END)
        hp_entry.insert(0, f"{hp}")

        selection_entry.delete(0,END)
        selection_entry.insert(0, f"{id}")

    except:
        pass



def select_from_treeview(event: tk.Event, treeview: ttk.Treeview) -> list:

    """ handles an event triggered when an item is selected

    Args:
        event (tk.Event): a tkinter event
        treeview (ttk.Treeview):  widget in which the item was selected.

    Returns:
        list: data displayed in the columns of the selected row
    """
    selected_item = treeview.selection()
    item_data = treeview.item(selected_item)
    values = item_data["values"]
    
    return values

def populate_treeview(treeview: ttk.Treeview):
    """
    Populates a ttk.Treeview widget with data from an SQLite database

    Args:
        treeview (ttk.Treeview): treeview object
    """

    for row in treeview.get_children():
        treeview.delete(row)

    data = select_data_from_database("initiative_tracker.db", "initiative")
    sorted_data = sorted(data, key=lambda x: x[2], reverse=True)
    
    for row in sorted_data:
        treeview.insert("","end", values = row)


def create_treeview(screen: tk.LabelFrame, column_names: tuple)-> ttk.Treeview:
    """Function argument are screen that treeview will be placed, and name of the
       colums that are shown in treeview

    Args:
        screen (tk.LabelFrame): Label frame that will show treeview
        column_names (tuple): Tuple that contains names of colums in treeview

    Returns:
        ttk.Treeview: Returns treeview object 
    """

    treeview = ttk.Treeview(screen)
    treeview["columns"] = column_names
    treeview.column("#0", width = 0, stretch="NO")

    for column in column_names:
        treeview.column(f"{column}", anchor="center")
        treeview.heading(f"{column}",  text=f"{column}", anchor="center")
    
    treeview.pack(padx=5, pady=5)

    return treeview

def get_entry_data(name: str, initiative: int, AC: int, condition: str, hp: int) -> tuple:
    """Constructing a data tuple for the purpose of inserting a new entry into an SQLite database table

    Args:
        name (str): The name of the character or entity to be added to the database.
        initiative (int): The initiative value, which represents the character's turn order in a game or initiative order.
        AC (int): The Armor Class, which indicates the character's defense or difficulty to hit.
        condition (str): A textual description of the character's condition, such as "Healthy," "Injured," etc.
        hp (int):The character's current hit points, representing their health.

    Returns:
        tuple: inserting a new entry into an SQLite database table
    """

    try:
        connection = create_connection("initiative_tracker.db")
        number = get_largest_ID(connection, "initiative")
    
        if number == None:
            number = 1
            initiative = int(initiative)
            AC = int(AC)
            hp = int(hp)
        else:
            number = number+1
            initiative = int(initiative)
            AC = int(AC)
            hp = int(hp)
        data = (number, name, initiative, AC, condition, hp)

        return data
    except:
        data_entry_error("Nisu uneseni valjani podatci")

    
def save(name: str, initiative: int, AC: int, condition: str, hp: int, main_treeview: ttk.Treeview):
    """Saving a data tuple as new entry into an SQLite database table

    Args:
        name (str): The name of the character or entity to be added to the database.
        initiative (int): The initiative value, which represents the character's turn order in a game or initiative order.
        AC (int): The Armor Class, which indicates the character's defense or difficulty to hit.
        condition (str): A textual description of the character's condition, such as "Healthy," "Injured," etc.
        hp (int):The character's current hit points, representing their health.
        main_treeview(ttk.Treeview): treeview that will be updated

    """
    connection = create_connection("initiative_tracker.db")
    create_table_sql = """CREATE TABLE IF NOT EXISTS initiative (
    number INTEGER PRIMARY KEY,
    name TEXT,
    initiative INTEGER,
    armor_class INTEGER,
    condition TEXT,
    hp INTEGER
    )"""

   
    create_table(connection, create_table_sql)

    data = get_entry_data(name, initiative, AC, condition, hp)

    insert_into_table(connection, "INSERT INTO initiative (number, name, initiative, armor_class, condition, hp) VALUES (?, ?, ?, ?, ?,?)", data)
    populate_treeview(main_treeview)

def update(name: str, database: str, table_name: str, hp:str, treeview: ttk.Treeview, condition: str):
    update_database(name, database, table_name, hp, condition)
    populate_treeview(treeview)
