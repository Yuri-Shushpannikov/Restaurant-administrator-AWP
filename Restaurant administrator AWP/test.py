import tkinter as tk
import json
import pathlib, os
from pathlib import Path
from tkinter import ttk, messagebox, simpledialog 
from tkinter import *

root = tk.Tk()

# Getting the current working directory
current_directory = os.getcwd()

# Specify the subfolder where your images are stored
image_folder = "Images"

# Construct the full path to the image folder
image_path = os.path.join(current_directory, image_folder)

menubutton_img = PhotoImage(file=os.path.join(image_path, 'Menu.png'))
menubutton_label = Label(image = menubutton_img)

reservationbutton_img = PhotoImage(file=os.path.join(image_path, 'Zal.png'))
reservationbutton_label = Label(image = reservationbutton_img)

class AddReservationDialog(tk.Toplevel):
    def __init__(self, parent, table):
        super().__init__(parent)
        self.title("Добавить бронирование")       
        self.geometry("400x300") 

        self.name_label = tk.Label(self, text="Имя гостя:")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self, width = 35)
        self.name_entry.grid(row=0, column=1)

        self.time_label = tk.Label(self, text="Время бронирования:")
        self.time_label.grid(row=1, column=0, sticky="w")
        self.time_entry = tk.Entry(self, width = 35)
        self.time_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self, text="Добавить бронирование", command=self.add_reservation)
        self.add_button.grid(row=2, column=0, padx=10)

        self.cancel_button = tk.Button(self, text="Отмена", command=self.destroy)
        self.cancel_button.grid(row=2, column=1)

        self.table = table

    def add_reservation(self):
        name = self.name_entry.get()
        time = self.time_entry.get()

        if not name:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните имя гостя.")
            return

        if not time:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните время бронирования.")
            return

        # Add the new food item
        new_reservation = Reservation(name, time)
        self.table.reservations.append(new_reservation)
        
        # Update the food listbox display
        restaurant_system.show_reservations()

        self.destroy()

class EditReservationDialog(tk.Toplevel):
    def __init__(self, parent, reservation_item):
        super().__init__(parent)
        self.title("Редактировать бронирование")

        self.reservation_item = reservation_item

        self.name_label = tk.Label(self, text="Имя гостя:")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)
        self.name_entry.insert(0, self.reservation_item.name)

        self.time_label = tk.Label(self, text="Время бронирования:")
        self.time_label.grid(row=1, column=0, sticky="w")
        self.time_entry = tk.Entry(self)
        self.time_entry.grid(row=1, column=1)
        self.time_entry.insert(0, self.reservation_item.time)

        self.save_button = tk.Button(self, text="Сохранить", command=self.save_reservation)
        self.save_button.grid(row=2, columnspan=2)

        self.cancel_button = tk.Button(self, text="Отмена", command=self.destroy)
        self.cancel_button.grid(row=2, column=1, padx=5, pady=5)

    def save_reservation(self):
        name = self.name_entry.get()
        time = self.time_entry.get()

        if not name:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните имя гостя.")
            return

        if not time:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните время бронирования.")
            return

        # Update the existing reservation logic here

        self.destroy()

class Table:

    def __init__(self, name):
        
        self.name = name
        self.reservations = []

class Reservation:

    def __init__(self, name, time):

        self.name = name
        self.time = time

class food:

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price



class DinerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Закусочная")
        self.root.geometry("1000x800")

        self.tables = []
        self.selected_table = None

        self.show_title_screen()


    def show_title_screen(self):
        self.clear_widgets()

        menu_button = tk.Button(self.root, image=menubutton_img, text= "Меню", command=self.show_menu, borderwidth=0)
        menu_button.pack(side=LEFT, padx = 50)

        create_table_button = tk.Button(self.root, image=reservationbutton_img, text="Зал", command=self.show_tables, borderwidth=0)
        create_table_button.pack(side=RIGHT, padx = 50)

    def show_menu(self):
        self.clear_widgets()
        
        back_button = tk.Button(self.root, text="Назад", command=self.show_title_screen)
        back_button.pack(anchor="nw", padx = 10, pady = 10)

        # Фрейм тривью
        self.tree_frame = Frame(root)
        self.tree_frame.pack(pady=20)

        # Полоска
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Создал тривью
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        self.tree_scroll.config(command=self.my_tree.yview)

        # Меню
        self.my_tree['columns'] = ("Блюдо", "Ингридиенты", "Цена")

        # Меню поле
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Блюдо", anchor=W, width=150)
        self.my_tree.column("Ингридиенты", anchor=CENTER, width=400)
        self.my_tree.column("Цена", anchor=W, width=150)

        # Названия
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Блюдо", text="Блюдо", anchor=W)
        self.my_tree.heading("Ингридиенты", text="Ингридиенты", anchor=CENTER)
        self.my_tree.heading("Цена", text="Цена", anchor=W)

        # Дата
        self.data = []

        global count
        count=0

        for record in self.data:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('oddrow',))

            count += 1

        self.add_frame = Frame(root)
        self.add_frame.pack(pady=20)

        #Названия
        self.nl = Label(self.add_frame, text="Блюдо")
        self.nl.grid(row=0, column=0)

        self.il = Label(self.add_frame, text="Ингридиенты")
        self.il.grid(row=0, column=1)

        self.tl = Label(self.add_frame, text="Цена")
        self.tl.grid(row=0, column=2)

        #Ввод
        self.name_box = Entry(self.add_frame)
        self.name_box.grid(row=1, column=0)

        self.description_box = Entry(self.add_frame, width=75)
        self.description_box.grid(row=1, column=1)

        self.price_box = Entry(self.add_frame)
        self.price_box.grid(row=1, column=2)

        # Add Record
        def add_record():
            self.my_tree.tag_configure('oddrow', background="white")
            self.my_tree.tag_configure('evenrow', background="lightblue")

            global count
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(self.name_box.get(), self.description_box.get(), self.price_box.get()), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(self.name_box.get(), self.description_box.get(), self.price_box.get()), tags=('oddrow',))

            count += 1

            # Clear the boxes
            self.name_box.delete(0, END)
            self.description_box.delete(0, END)
            self.price_box.delete(0, END)

        # Remove all records
        def remove_all_records():
            for record in self.my_tree.get_children():
                self.my_tree.delete(record)

        # Remove one selected
        def remove_one():
            x = self.my_tree.selection()[0]
            self.my_tree.delete(x)

        # Select Record
        def select_record():
            # Clear entry boxes
            self.name_box.delete(0, END)
            self.description_box.delete(0, END)
            self.price_box.delete(0, END)

            # Grab record number
            selected = self.my_tree.focus()
            # Grab record values
            values = self.my_tree.item(selected, 'values')

            #temp_label.config(text=values[0])

            # output to entry boxes
            self.name_box.insert(0, values[0])
            self.description_box.insert(0, values[1])
            self.price_box.insert(0, values[2])

        # Save updated record
        def update_record():
            # Grab record number
            selected = self.my_tree.focus()
            # Save new data
            self.my_tree.item(selected, text="", values=(self.name_box.get(), self.description_box.get(), self.price_box.get()))

            # Clear entry boxes
            self.name_box.delete(0, END)
            self.description_box.delete(0, END)
            self.price_box.delete(0, END)

        # Create Binding Click function
        def clicker(e):
            select_record()

        # Save data to JSON file
        def save_data_to_json():
            data_to_save = []
            for child in self.my_tree.get_children():
                values = self.my_tree.item(child, 'values')
                data_to_save.append({
                    "Блюдо": values[0],
                    "Ингридиенты": values[1],
                    "Цена": values[2]
                })

            with open('diner_data.json', 'w') as f:
                json.dump(data_to_save, f, indent=4)

        # Load data from JSON file
        def load_data_from_json():
            remove_all_records()
            try:
                with open('diner_data.json', 'r') as f:
                    data = json.load(f)
                    for d in data:
                        self.my_tree.insert('', END, values=(d["Блюдо"], d["Ингридиенты"], d["Цена"]))
            except FileNotFoundError:
                print("No JSON file found.")



        # Create striped row tags
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

        #Buttons
        top_button_frame = tk.Frame(root)
        top_button_frame.pack(side="top", fill="x",padx=260)

        load_json = Button(top_button_frame, text="Загрузить меню", width=30, height=3, command=load_data_from_json)
        load_json.grid(row=0, column=0, padx=10, pady=10)

        save_json = Button(top_button_frame, text="Сохранить меню", width=30, height=3, command=save_data_to_json)
        save_json.grid(row=0, column=1, padx=10, pady=10)
        
        button_frame = tk.Frame(root, width = 300)
        button_frame.pack(padx=10, pady=10)

        update_button = Button(button_frame, text="Сохранить изменения", command=update_record, width = 20, height = 2)
        update_button.grid(row=0, column=0)

        add_record_food = Button(button_frame, text="Добавить блюдо", command=add_record, width = 20, height =2)
        add_record_food.grid(row=1, column=0)

        remove_all_button = Button(button_frame, text="Очистить меню", command=remove_all_records, width = 20, height =2)
        remove_all_button.grid(row=3, column=0)

        remove_one_food = Button(button_frame, text="Удалить блюдо", command=remove_one, width = 20, height =2)
        remove_one_food.grid(row=2, column=0)


        
        self.my_tree.bind("<ButtonRelease-1>", clicker)


    def save_tables_to_json(self):
        data = []

        for table in self.tables:
            table_data = {
                "name": table.name,
                "reservations": [{"name": reservation.name, "time": reservation.time} for reservation in table.reservations]
            }
            data.append(table_data)

        with open("tables.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_tables_from_json(self):
        self.tables.clear()
        try:
            with open("tables.json", "r") as file:
                data = json.load(file)
                for table_data in data:
                    table = Table(table_data["name"])
                    for reservation_data in table_data["reservations"]:
                        reservation = Reservation(reservation_data["name"], reservation_data["time"])
                        table.reservations.append(reservation)
                    self.tables.append(table)
                messagebox.showinfo("Успешно", "Информация о бронировании загружена")
                self.show_tables()
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Сохраненная информация не найдена")

    def show_tables(self):
        self.clear_widgets()

        back_button = tk.Button(self.root, text="Назад", command=self.show_title_screen)
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Listbox to display tables
        table_label = tk.Label(self.root, text="Столы:")
        table_label.pack()

        table_listbox = tk.Listbox(self.root, selectmode="single", width=20, height=10, font=(50))
        for table in self.tables:
            table_listbox.insert(tk.END, table.name)
        table_listbox.pack()

        top_button_frame_tables = tk.Frame(root)
        top_button_frame_tables.pack(side="top", fill="x",padx=260)

        load_button = tk.Button(top_button_frame_tables, text="Загрузить расписание брони", command=self.load_tables_from_json, width=30, height=2)
        load_button.grid(row=0, column=0, padx=10, pady=10)

        save_json = tk.Button(top_button_frame_tables, text="Сохранить расписание брони", command=self.save_tables_to_json, width=30, height=2)
        save_json.grid(row=0, column=1, padx=10, pady=10)

        button_frame = tk.Frame(root, width = 300)
        button_frame.pack(padx=10, pady=10)

        add_button = tk.Button(button_frame, text="Добавить столик", command= lambda: self.add_table(table_listbox), width=20, height=2)
        add_button.grid(row=1, column=0)
        
        rename_button = tk.Button(button_frame, text="Изменить номер", command= lambda: self.rename_table(table_listbox), width=20, height=2)
        rename_button.grid(row=2, column=0)

        select_button = tk.Button(button_frame, text="Показать бронь столика", command=lambda: self.select_table(table_listbox), width=20, height=2)
        select_button.grid(row=0, column=0)

        delete_button = tk.Button(button_frame, text="Удалить столик", command=lambda: self.delete_table(table_listbox), width=20, height=2)
        delete_button.grid(row=3, column=0)

    def add_table(self, table_listbox):
        # Open a dialog to get the new table's name
        dialog = tk.simpledialog.askstring("Добавить столик", "Введите номер стола:")
        if dialog:
            new_table = Table(dialog)
            self.tables.append(new_table)
            table_listbox.insert(tk.END, dialog)

    def delete_table(self, table_listbox):
        selected_index = table_listbox.curselection()
        if selected_index:
            del self.tables[selected_index[0]]
            self.clear_widgets()
            self.show_tables()

    def rename_table(self, table_listbox):
        selected_index = table_listbox.curselection()
        if selected_index:
            old_name = self.tables[selected_index[0]].name
            new_name = tk.simpledialog.askstring("Изменить номер стола", f"Введите новый номер '{old_name}':")
            if new_name:
                self.tables[selected_index[0]].name = new_name
                table_listbox.delete(selected_index)
                table_listbox.insert(selected_index, new_name)

    def select_table(self, table_listbox):
        selected_index = table_listbox.curselection()
        if selected_index:
            self.selected_table = self.tables[selected_index[0]]
            self.show_reservations()

    def show_reservations(self):
        self.clear_widgets()

        back_button = tk.Button(self.root, text="Назад", command=self.show_tables)
        back_button.pack(anchor="nw", padx=10, pady=10)

        reservation_label = tk.Label(self.root, text="Бронирование:")
        reservation_label.pack()

        # Display selected table's reservations
        reservations_listbox = tk.Listbox(self.root, selectmode="single", width=20, height=10, font=(50))
        for reservation in self.selected_table.reservations:
            reservations_listbox.insert(tk.END, reservation.name + " - " + reservation.time)
        reservations_listbox.pack()

        top_button_frame_reserve = tk.Frame(root)
        top_button_frame_reserve.pack(side="top", fill="x",padx=330)

        add_reservation_button = tk.Button(top_button_frame_reserve, text="Добавить бронирование", command=lambda: self.add_reservation(), width=20, height=3)
        add_reservation_button.grid(row=0, column=0, padx=10, pady=10)

        delete_reservation_button = tk.Button(top_button_frame_reserve, text="Удалить бронирование", command=lambda: self.delete_reservation(reservations_listbox), width=20, height=3)
        delete_reservation_button.grid(row=0, column=1, padx=10, pady=10)

    def add_reservation(self):
        dialog = AddReservationDialog(self.root, self.selected_table)
        self.root.wait_window(dialog)

    def delete_reservation(self, reservation_listbox):
        selected_index = reservation_listbox.curselection()
        if selected_index:
            del self.selected_table.reservations[selected_index[0]]
            self.clear_widgets()
            self.show_reservations()

    def edit_reservation(self, reservation_listbox):
        selected_table_index = self.tables.index(self.selected_table)
        selected_index = reservation_listbox.curselection()

        if selected_index:
            reservation_item = self.selected_table.reservations[selected_index[0]]
            dialog = EditReservationDialog(self.root, reservation_item)
            self.root.wait_window(dialog)

            new_name = dialog.name_entry.get()
            new_time = dialog.time_entry.get()

            if new_name:
                self.selected_table.reservations[selected_index[0]].name = new_name
                self.selected_table.reservations[selected_index[0]].time = new_time

                reservation_listbox.delete(selected_index)
                reservation_listbox.insert(selected_index, new_name + " - " + new_time)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

restaurant_system = DinerApp(root)

root.mainloop()



