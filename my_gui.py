from tkinter import *
from tkinter import ttk
import ttkbootstrap
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
import russian_tool
import img_scrape
import threading

WIDTH = 40
SCRL_HEIGHT = 8
SCRL_WIDTH = 50
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

        self.entry_query = ttk.Entry(mainframe, textvariable=self.stringvar_query, width=SCRL_WIDTH)
        self.scrl_gen_defns_en = ScrolledText   (mainframe, height=SCRL_HEIGHT, width=SCRL_WIDTH)
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
        
        self.entry_query.grid         (column=1, row=0, sticky=(W, E))
        self.scrl_gen_defns_en.grid   (column=1, row=1, sticky=(W, E))
        self.scrl_gen_conjs_decls.grid(column=1, row=2, sticky=(W, E))
        self.scrl_gen_related.grid    (column=1, row=3, sticky=(W, E))
        self.scrl_gen_synos.grid      (column=1, row=4, sticky=(W, E))
        self.scrl_gen_examples.grid   (column=1, row=5, sticky=(W, E))
        self.scrl_out_en.grid         (column=5, row=1, sticky=(W, E))
        self.scrl_out_ru.grid         (column=5, row=2, sticky=(W, E))
        self.scrl_out_conjs_decls.grid(column=5, row=3, sticky=(W, E))
        self.scrl_out_examples.grid   (column=5, row=4, sticky=(W, E))
        self.scrl_out_related.grid    (column=5, row=5, sticky=(W, E))
        self.scrl_out_synos.grid      (column=5, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Query:").grid(column=0, row=0, sticky=W)
        ttk.Label(mainframe, text="Generated Definitions (en):").grid(column=0, row=1, sticky=W)
        ttk.Label(mainframe, text="Generated Conjugations/\nDeclensions:").grid(column=0, row=2, sticky=W)
        ttk.Label(mainframe, text="Generated Examples:").grid(column=0, row=5, sticky=W)
        ttk.Label(mainframe, text="Generated Related:").grid(column=0, row=3, sticky=W)
        ttk.Label(mainframe, text="Generated Synonyms:").grid(column=0, row=4, sticky=W)
        ttk.Label(mainframe, text="Out English Field:").grid(column=4, row=1, sticky=W)
        ttk.Label(mainframe, text="Out Russian Field:").grid(column=4, row=2, sticky=W)
        ttk.Label(mainframe, text="Out Conjugations/\nDeclensions Field:").grid(column=4, row=3, sticky=W)
        ttk.Label(mainframe, text="Out Examples Field:").grid(column=4, row=4, sticky=W)
        ttk.Label(mainframe, text="Out Related Field:").grid(column=4, row=5, sticky=W)
        ttk.Label(mainframe, text="Out Synonyms Field:").grid(column=4, row=6, sticky=W)

        ttk.Button(mainframe, text="Img Search", command=self.button_img_search).grid(column=3, row=0, padx=10)
        ttk.Button(mainframe, text="Clear", command=self.button_clear).grid(column=4, row=0, padx=10)
        ttk.Button(mainframe, text="Search", command=self.button_search).grid(column=2, row=0)
        ttk.Button(mainframe, text="Submit", command=self.button_submit).grid(column=3, row=7, pady=20)
        ttk.Button(mainframe, text="Syno Search", command=self.button_syno_search).grid(column=2, row=4)
        ttk.Button(mainframe, text="Ex Search", command=self.button_ex_search).grid(column=2, row=5)


    def list_to_str(self, list_in, extra_line=False):
        out = ""
        for elem in list_in:
            out += str(elem)
            out += "\n"
            if extra_line == True:
                out += "\n"
        return out

    def button_img_search(self):

        query = self.stringvar_query.get()

        print(f"[Img Search] Scraping images ({query})")
        # Scrape images
        task = threading.Thread(target=img_scrape.get_imgs, args=(query,30,))
        task.start()

    def button_ex_search(self):

        query = self.stringvar_query.get()

        print(f"[Ex Search] Examples ({query})")
        examples = russian_tool.generate_field_exs(query)
        if examples != None:
            str_examples = self.list_to_str(examples, extra_line = True)
            self.scrl_gen_examples.insert(INSERT, str_examples)

    def button_syno_search(self):

        query = self.stringvar_query.get()

        print(f"[Syno Search] Synonyms ({query})")
        synos = russian_tool.generate_field_synos(query)
        if synos != None:
            str_synos = self.list_to_str(synos, extra_line = True)
            self.scrl_gen_synos.insert(INSERT, str_synos)

    def button_clear(self):
        print("clear")
        self.scrl_gen_defns_en.delete("1.0", END)
        self.scrl_gen_conjs_decls.delete("1.0", END)
        self.scrl_gen_examples.delete("1.0", END)
        self.scrl_gen_related.delete("1.0", END)
        self.scrl_gen_synos.delete("1.0", END)

    def button_search(self):

        self.button_clear()

        query = self.stringvar_query.get()
        print(f"[Search] Query:{query}")

        print(f"[Search] Wikipedia")
        wikipedia_fields = russian_tool.generate_field_en(query)
        defns_en = wikipedia_fields[russian_tool.DEFNS_EN]
        decls    = wikipedia_fields[russian_tool.DECLS]
        conjs    = wikipedia_fields[russian_tool.CONJS]
        misc     = wikipedia_fields[russian_tool.MISC]
        if defns_en != None:
            str_defns_en = self.list_to_str(defns_en)
            self.scrl_gen_defns_en.insert(INSERT, str_defns_en)
        if decls != None:
            str_decls = self.list_to_str(decls)
            self.scrl_gen_conjs_decls.insert(INSERT, str_decls)
        if conjs != None:
            str_conjs = self.list_to_str(conjs)
            self.scrl_gen_conjs_decls.insert(INSERT, str_conjs)
        if misc != None:
            str_misc = self.list_to_str(misc)
            self.scrl_gen_related.insert(INSERT, str_misc)

    def button_submit(self):
        print("submit")

#root = Tk()
#GUI(root)
#root.mainloop()
#print("Exited application")
