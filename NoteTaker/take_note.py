import os
from NoteTaker import make_file as mkf
import subprocess
import datetime
import tkinter as tk
from tkinter import ttk



class NoteTaker(tk.Frame):

    def __init__(self, master, nowdate: datetime, title: str, subjects: tuple, subject: str, tag_set: set):
        super().__init__(master)

        # 3x5 grid

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure(0, weight=1)

        self.frame = ttk.Frame()
        self.frame.grid_configure(in_=self.master)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.frame.grid()

        self.chosen_tags = ""
        self.tag_set_CV = set()
        if len(tag_set) != 0:
            self.tag_set_CV = tag_set
        self.last_added = ''

        self.chosen_subject = subject
        self.note_title = title

        now = nowdate.now()
        self.now_stamp = nowdate.strftime(now, "%d%m%y-%H%M%S")

        label_txt = f"Note: {self.note_title}"
        label_txt_sbj = f"Subject:"
        label_txt_tags = f"Tags:"


        #Note Label
        self.label_n = ttk.Label(self.master, justify="left", text=label_txt)
        self.label_n.grid(column=0, row=4, padx=5, pady=5, in_=self.frame)

        #Subject Label
        self.label_s = ttk.Label(self.master, justify="left", text=label_txt_sbj)
        self.label_s.grid(column=0, row=0, padx=5, pady=5, in_=self.frame)

        #Chosen subject label
        self.label_s_chs = ttk.Label(self.master, justify="center", text=self.chosen_subject)
        self.label_s_chs.grid(column=1, row=1, padx=5, pady=5, in_=self.frame)

        #tag Label
        self.label_t = ttk.Label(self.master, justify="left", text=label_txt_tags)
        self.label_t.grid(column=0, row=2, padx=5, pady=5, in_=self.frame)

        #Chosen Tags list
        self.label_t_chs = ttk.Label(self.master, justify="left", text='')
        self.label_t_chs.grid(column=1, row=3, padx=5, pady=2, in_=self.frame)
        self.tag_count = 0

        #Tags combobox
        self.cbox_tags_var = tk.StringVar()
        self.cbox_tags = ttk.Combobox(self.master, values=subjects, textvariable=self.cbox_tags_var, exportselection=True)
        # self.cbox_tags.bind('<Button-1><ButtonRelease>', self.selected_tags)
        self.cbox_tags.bind('<Key-Return>', self.selected_tags)
        self.cbox_tags.bind('<Control-z>', self.undo_tag_select, add=True)
        self.cbox_tags.grid(column=1, row=2, padx=5, pady=5, in_=self.frame)

        #Subject combobox
        self.cbox_s_var = tk.StringVar()
        self.cbox_s = ttk.Spinbox(self.master, values=subjects, textvariable=self.cbox_s_var, exportselection=True, state='readonly')
        self.cbox_s.bind('<Key-Return>', self.selected_subject)
        self.cbox_s.grid(column=1, row=0, padx=5, pady=2, in_=self.frame)

        child_frame = ttk.Frame()
        #Entry entry
        self.entry_txt = tk.StringVar()
        self.entry = ttk.Entry(self.master, justify="left", exportselection=True, textvariable=self.entry_txt)
        self.entry.bind('<Key-Return>', self.submit_entry)
        self.entry.grid_rowconfigure(index=5, weight=3)
        self.entry.grid_columnconfigure(index=2, weight=3)
        self.entry.grid(column=0, row=5, columnspan=4, rowspan=3, padx=5, pady=7, sticky=tk.N+tk.E+tk.S+tk.W, in_=self.frame)

        self.lastline = ttk.Button(self.master, text="Save", command=)
        self.lastline.grid(column=2, row=8, padx=5, pady=5, in_=self.frame)

        ### DEBUGGING
        cmdlst = \
            [self.frame.winfo_geometry(),
             self.frame.grid_info(),
             self.frame.grid_anchor(),
             self.frame.grid_size(),
             ]

        [print(i) for i in cmdlst]
        ###

    def submit_entry(self, event):

        recv_entry(str(self.entry_txt))

    def selected_tags(self, event):

        if '' in self.tag_set_CV:
            self.tag_set_CV.discard('')
            return
        elif len(str(self.cbox_tags_var.get())) == 0:
            self.tag_set_CV.discard('')
            return
        else:
            self.last_added = str(self.cbox_tags_var.get()).strip()
            self.tag_set_CV.add(self.last_added)
            self.label_t_chs.__setitem__('text', f"> {self.tag_set_CV.__str__().strip('{}')}")
            print(str(self.tag_set_CV))

    def undo_tag_select(self, event):

        self.tag_set_CV.discard(self.last_added)
        self.label_t_chs.__setitem__('text', f"> {self.tag_set_CV.__str__().strip('{}')}")
        print(str(self.tag_set_CV))


    def selected_subject(self, event):

        if self.chosen_subject == '':
            return
        elif len(self.cbox_s_var.get()) == 0:
            return
        else:
            self.chosen_subject = (str(self.cbox_s_var.get()))
            self.label_s_chs.__setitem__('text', f"> {self.chosen_subject.__str__().strip()}")
            self.note_title = f'{self.now_stamp}_{self.chosen_subject}'
            self.label_n.__setitem__('text', f'{self.now_stamp}_{self.chosen_subject.strip()}')
            print(str(self.chosen_subject))


def make_note(title: str = None, subject: str = None, *tags):
    dt = datetime
    dtnow = dt.datetime.now()
    now_stamp = dt.datetime.strftime(dtnow, '%d%m%y-%H%M%S')

    if subject is None:
        subject = "Misc"
    if title is None:
        title = f"{now_stamp}_{subject}"
    if len(set(*tags,)) != 0:
        tag_set = {i for i in tags}
    else:
        tag_set = {'', }

    wndw_master = tk.Tk()
    app_win = NoteTaker(wndw_master, dt.datetime, title, get_subjects(), subject, tag_set)
    app_win.master.winfo_geometry()

    app_win.mainloop()


def get_subjects():

    with open(os.getenv('SUBJECTS_FILE'), 'r') as sbjct_f:
        subs = tuple((i.strip() for i in sbjct_f.readlines()))
        return subs


def update_tags(new_tags):
    with open(os.getenv('TAGS_FILE'), 'r') as tags_f:
        tags = set((j.strip() for j in tags_f.readlines()))


def recv_entry(entry: str):
    pass

def recv_title(title: str):
    pass

def recv_subj(subj: str):
    pass

def recv_tags(tags: tuple):
    pass

def submit_entry(entry: str, title: str):
    pass