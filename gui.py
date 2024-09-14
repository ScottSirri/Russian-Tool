from tkinter import *
from tkinter import ttk
import ttkbootstrap
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText

WIDTH = 40
SCRL_HEIGHT = 5
SCRL_WIDTH = 20
IMGS_HEIGHT = 5
IMGS_WIDTH = 20

class GUI:
    
    def __init__(self, root):
        root.title("Russian Anki Application")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        mainframe = ttk.Frame(root, padding="3 3 3 3")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        mainframe.columnconfigure(1, weight=2)
        mainframe.columnconfigure(5, weight=2)
        for i in range(10):
            mainframe.rowconfigure(i, weight=1)

        self.stringvar_query = StringVar()
        self.stringvar_quick = StringVar()
        """
        self.stringvar_gen_defns_en = StringVar()
        self.stringvar_gen_defns_ru = StringVar()
        self.stringvar_gen_conjs_decls = StringVar()
        self.stringvar_gen_examples = StringVar()
        self.stringvar_gen_related = StringVar()
        self.stringvar_gen_synos = StringVar()
        self.stringvar_out_ru = StringVar()
        self.stringvar_out_en = StringVar()
        self.stringvar_out_conjs_decls = StringVar()
        self.stringvar_out_examples = StringVar()
        self.stringvar_out_related = StringVar()
        self.stringvar_out_synos = StringVar()
        """

        self.entry_query = ttk.Entry(mainframe, textvariable=self.stringvar_query, width=SCRL_WIDTH)
        self.entry_quick = ttk.Entry(mainframe, textvariable=self.stringvar_quick, width=SCRL_WIDTH)
        self.scrl_gen_defns_en = ScrolledText   (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_gen_defns_ru = ScrolledText   (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_gen_conjs_decls = ScrolledText(mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_gen_examples = ScrolledText   (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_gen_related = ScrolledText    (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_gen_synos = ScrolledText      (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_out_ru = ScrolledText         (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_out_en = ScrolledText         (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_out_conjs_decls = ScrolledText(mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_out_examples = ScrolledText   (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_out_related = ScrolledText    (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.scrl_out_synos = ScrolledText      (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
        self.frame_imgs = ttk.Frame(mainframe, height=IMGS_HEIGHT, width=IMGS_WIDTH)
        
        self.entry_query.grid         (column=1, row=0, sticky=(W, E))
        self.scrl_gen_defns_en.grid   (column=1, row=1, sticky=(W, E))
        self.scrl_gen_defns_ru.grid   (column=1, row=2, sticky=(W, E))
        self.scrl_gen_conjs_decls.grid(column=1, row=3, sticky=(W, E))
        self.scrl_gen_examples.grid   (column=1, row=4, sticky=(W, E))
        self.scrl_gen_related.grid    (column=1, row=5, sticky=(W, E))
        self.scrl_gen_synos.grid      (column=1, row=6, sticky=(W, E))
        self.frame_imgs.grid          (column=1, row=7, sticky=(W, E))
        self.entry_quick.grid         (column=1, row=8, sticky=(W, E))
        self.scrl_out_en.grid         (column=5, row=1, sticky=(W, E))
        self.scrl_out_ru.grid         (column=5, row=2, sticky=(W, E))
        self.scrl_out_conjs_decls.grid(column=5, row=3, sticky=(W, E))
        self.scrl_out_examples.grid   (column=5, row=4, sticky=(W, E))
        self.scrl_out_related.grid    (column=5, row=5, sticky=(W, E))
        self.scrl_out_synos.grid      (column=5, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Query:").grid(column=0, row=0, sticky=W)
        ttk.Label(mainframe, text="Quick Query:").grid(column=0, row=8, sticky=W)
        ttk.Label(mainframe, text="Generated Definitions (en):").grid(column=0, row=1, sticky=W)
        ttk.Label(mainframe, text="Generated Definitions (ru):").grid(column=0, row=2, sticky=W)
        ttk.Label(mainframe, text="Generated Conjugations/\nDeclensions:").grid(column=0, row=3, sticky=W)
        ttk.Label(mainframe, text="Generated Examples:").grid(column=0, row=4, sticky=W)
        ttk.Label(mainframe, text="Generated Related:").grid(column=0, row=5, sticky=W)
        ttk.Label(mainframe, text="Generated Synonyms:").grid(column=0, row=6, sticky=W)
        ttk.Label(mainframe, text="Image Options:").grid(column=0, row=7, sticky=W)
        ttk.Label(mainframe, text="Out English Field:").grid(column=4, row=1, sticky=W)
        ttk.Label(mainframe, text="Out Russian Field:").grid(column=4, row=2, sticky=W)
        ttk.Label(mainframe, text="Out Conjugations/\nDeclensions Field:").grid(column=4, row=3, sticky=W)
        ttk.Label(mainframe, text="Out Examples Field:").grid(column=4, row=4, sticky=W)
        ttk.Label(mainframe, text="Out Related Field:").grid(column=4, row=5, sticky=W)
        ttk.Label(mainframe, text="Out Synonyms Field:").grid(column=4, row=6, sticky=W)

        ttk.Button(mainframe, text="Generate", command=self.button_generate).grid(column=2, row=0, padx=10)
        ttk.Button(mainframe, text="Clear", command=self.button_clear).grid(column=3, row=0, padx=10)
        ttk.Button(mainframe, text="Search", command=self.button_search).grid(column=2, row=8)
        ttk.Button(mainframe, text="Submit", command=self.button_submit).grid(column=3, row=9, pady=20)

    def button_generate(self):
        print("generate")

    def button_clear(self):
        self.stringvar_query.set("")
        self.stringvar_quick.set("")
        self.scrl_gen_defns_en.delete("1.0", END)
        self.scrl_gen_defns_ru.delete("1.0", END)
        self.scrl_gen_conjs_decls.delete("1.0", END)
        self.scrl_gen_examples.delete("1.0", END)
        self.scrl_gen_related.delete("1.0", END)
        self.scrl_gen_synos.delete("1.0", END)
        self.scrl_out_en.delete("1.0", END)
        self.scrl_out_ru.delete("1.0", END)
        self.scrl_out_conjs_decls.delete("1.0", END)
        self.scrl_out_examples.delete("1.0", END)
        self.scrl_out_related.delete("1.0", END)
        self.scrl_out_synos.delete("1.0", END)
        print("clear")

    def button_search(self):
        print("search")

    def button_submit(self):
        print("submit")


class FeetToMeters:

    def __init__(self, root):

        root.title("Feet to Meters")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
       
        self.feet = StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        self.meters = StringVar()

        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)
        
    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass

root = Tk()
#FeetToMeters(root)
GUI(root)
root.mainloop()
print("Exited application")
