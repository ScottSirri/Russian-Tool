from tkinter import *
from tkinter import ttk
import ttkbootstrap
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
import russian_tool

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

        query = self.stringvar_query.get()
        print(query)

        # Obtain fields
        card_fields = russian_tool.generate_card_fields(query)

        # Unpack fields
        defns_ru = card_fields[russian_tool.DEFNS_RU]
        defns_en = card_fields[russian_tool.DEFNS_EN]
        decls = card_fields[russian_tool.DECLS]
        conjs = card_fields[russian_tool.CONJS]
        freq = card_fields[russian_tool.FREQ]
        examples = card_fields[russian_tool.EXAMPLES]
        imgs_dir = card_fields[russian_tool.IMGS_DIR]
        synos = card_fields[russian_tool.SYNOS]
        misc = card_fields[russian_tool.MISC]

        if defns_ru != None:
            str_defns_ru = str(defns_ru)
            self.scrl_gen_defns_ru.insert(INSERT, str_defns_ru)
        if defns_en != None:
            str_defns_en = str(defns_en)
            self.scrl_gen_defns_en.insert(INSERT, str_defns_en)
        if decls != None:
            str_decls = str(decls)
            self.scrl_gen_conjs_decls.insert(INSERT, str_decls)
        if conjs != None:
            str_conjs = str(conjs)
            self.scrl_gen_conjs_decls.insert(INSERT, str_conjs)
        if freq != None:
            str_freq = str(freq)
        if examples != None:
            str_examples = str(examples)
            self.scrl_gen_examples.insert(INSERT, str_examples)
        if imgs_dir != None:
            str_imgs_dir = str(imgs_dir)
        if synos != None:
            str_synos = str(synos)
            self.scrl_gen_synos.insert(INSERT, str_synos)
        if misc != None:
            str_misc = str(misc)
            self.scrl_gen_related.insert(INSERT, str_misc)


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

#root = Tk()
#GUI(root)
#root.mainloop()
#print("Exited application")
