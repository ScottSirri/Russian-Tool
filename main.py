import russian_tool
from tkinter import *
from tkinter import ttk
import my_gui


root = Tk()
gui = my_gui.GUI(root)
root.mainloop()
print("main mainloop ended")
sys.exit()

fields = russian_tool.generate_card_fields()
for field in fields:
    print(f"{field}: {fields[field]}")
    print()
