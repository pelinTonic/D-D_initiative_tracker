import tkinter as tk
from tkinter import ttk
from functions import *


main_screen = tk.Tk()
main_screen.title("D&D initiative tracker")

main_label_frame = tk.LabelFrame(main_screen)
main_label_frame.pack(expand=True, anchor=tk.CENTER)

main_treeview = create_treeview(main_label_frame, ("#", "Name","Initiative","AC","Condition", "HP"))

main_treeview.bind("<<TreeviewSelect>>", lambda event, main_treeview = main_treeview: show_selection(event, main_treeview))


lower_label_frame = tk.LabelFrame(main_screen)
lower_label_frame.pack(padx=5, pady=5)

name_label = tk.Label(lower_label_frame, text="Ime: ")
name_label.grid(row=0, column=0, padx=5, pady=5)
initiative_label = tk.Label(lower_label_frame, text="Inicijativa: ")
initiative_label.grid(row=1, column=0, padx=5, pady=5)
ac_label = tk.Label(lower_label_frame, text="AC: ")
ac_label.grid(row=2, column=0, padx=5, pady=5)
condition_label = tk.Label(lower_label_frame, text="Status: ")
condition_label.grid(row=3, column=0, padx=5, pady=5)
hp_label = tk.Label(lower_label_frame, text="HP: ")
hp_label.grid(row=4, column=0, padx=5, pady=5)

name_entry = tk.Entry(lower_label_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)
initiative_entry = tk.Entry(lower_label_frame)
initiative_entry.grid(row=1, column=1, padx=5, pady=5)
ac_entry = tk.Entry(lower_label_frame)
ac_entry.grid(row=2, column=1, padx=5, pady=5)

options = ["None","Blinded","Charmed","Deafened","Frightened","Grappled","Incapacitated","Invisible","Paralyzed","Petrified","Poisoned","Prone","Restrained","Stunned","Unconscious"]
selected_option = tk.StringVar()
condition_dropdown = tk.OptionMenu(lower_label_frame, selected_option, *options)
condition_dropdown.grid(row=3, column=1)
condition_dictionary = open_json_file("conditions.json")
info_button = tk.Button(lower_label_frame, text = "Info", command=lambda: show_info(selected_option.get(), condition_dictionary))
info_button.grid(row=3, column=2, padx=5, pady=5)
hp_entry = tk.Entry(lower_label_frame)
hp_entry.grid(row=4, column=1, padx=5, pady=5)

button_label_frame = tk.LabelFrame(main_screen)
button_label_frame.pack(padx=5, pady=5)

selection_label_frame = tk.LabelFrame(main_screen)
selection_label_frame.pack(padx=5, pady=5)

selection_entry = tk.Entry(selection_label_frame)
selection_entry.pack(padx=5, pady=5)

populate_treeview(main_treeview)
main_treeview.bind("<<TreeviewSelect>>", lambda event, main_treeview = main_treeview: show_selection(main_treeview,name_entry, initiative_entry, ac_entry, selection_entry, hp_entry))

save_button = tk.Button(button_label_frame, text="Spremi", command=lambda: save(name_entry.get(), initiative_entry.get(), ac_entry.get(), selected_option.get(), hp_entry.get(), main_treeview))
save_button.grid(row=0, column=0, padx=5, pady=5)
delete_button = tk.Button(button_label_frame, text="Ukloni", command= lambda : (delete_from_database(selection_entry.get(), "initiative_tracker.db", "initiative"), populate_treeview(main_treeview)))
delete_button.grid(row=0, column=1, padx=5, pady=5)
refresh_button = tk.Button(button_label_frame, text = "Osvježi", command=lambda: populate_treeview(main_treeview))
refresh_button.grid(row= 0, column=2, padx=5, pady=5 )
update_button = tk.Button(button_label_frame, text="Update", command=lambda: update(name_entry.get(), "initiative_tracker.db", "initiative", hp_entry.get(), main_treeview, selected_option.get()))
update_button.grid(row=0, column=3, padx=5, pady=5)



main_screen.mainloop()



