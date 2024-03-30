import tkinter as tk
from menu import open_menu_window

root = tk.Tk()
root.title('Main Window')

# Create a button to open the menu window
open_menu_button = tk.Button(root, text="Open Menu Window", command=open_menu_window)
open_menu_button.pack()

root.mainloop()