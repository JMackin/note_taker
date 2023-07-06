import os
from NoteTaker import orchestrate
import subprocess
from dotenv import load_dotenv
import datetime
import tkinter as tk
from tkinter import ttk


wndw_master = tk.Tk()

class NoteTaker(tk.Frame):
    def __init__(self, master, dt: tuple, title: str, subjects: tuple, subject: str, tag_set: set, jlmnote):
        super().__init__(master)

        # 3x5 grid

        #
        self.jlmnote = jlmnote

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
        self.note_content = ""

        #now = dt.now()
        self.now_stamp = dt

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
        self.entry = ttk.Entry(self.master, justify="left", textvariable=self.entry_txt, exportselection=True)
        self.entry.bind('<Key-Return>', self.pass_to_maker)
        self.entry.grid_rowconfigure(index=5, weight=3)
        self.entry.grid_columnconfigure(index=2, weight=3)
        self.entry.grid(column=0, row=5, columnspan=4, rowspan=3, padx=5, pady=7, sticky=tk.N+tk.E+tk.S+tk.W, in_=self.frame)

        self.lastline = ttk.Button(self.master, text="Save", command=self.pass_to_maker)
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

    def pass_to_maker(self, event=None):

        self.note_content = (str(self.entry_txt.get()))
        recv_entry(self.note_content, self.jlmnote)
        recv_subj(str(self.chosen_subject), self.jlmnote)
        recv_title(str(self.note_title), self.jlmnote)
        recv_tags(self.tag_set_CV, self.jlmnote)

        wndw_master.destroy()

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


class JlmNote:
    def __init__(self, now_stamp):
        self.ts = now_stamp
        self.title = ""
        self.subject = ""
        self.content = ""
        self.tags = set()
        self.iscmd = False
        self.note_attrs = {}
        self.update_attrs()

    def set_title(self, title: str):
        self.title = title
        self.note_attrs['title'] = self.title

    def set_content(self, entry: str):
        self.content = entry
        self.note_attrs['content'] = self.content

    def set_subject(self, subject: str):
        self.subject = subject
        self.note_attrs['subject'] = self.subject

    def set_tags(self, tags: set):
        self.tags = (self.tags | tags) if (self.tags - tags) else (self.tags - (self.tags-tags))
        self.note_attrs['tags'] = self.tags

    def set_iscmd(self, iscmd: bool):
        self.iscmd = iscmd
        self.note_attrs['iscmd'] = self.iscmd

    def update_attrs(self):
        self.note_attrs = {'timestamp': self.ts, 'title': self.title, 'content': self.content,
                           'subject': self.subject, 'tags': self.tags, 'iscmd': self.iscmd}

    def get_attrs(self):
        return self.note_attrs


def make_note_gui(jlmnote, *tags, ts: tuple, title: str = None, subject: str = None):
    now_stamp = ts[1]
    dt = ts[0]

    if subject is None:
        subject = "Misc"
    if title is None:
        title = f"{now_stamp}_{subject}"
    if len(set(*tags,)) != 0:
        tag_set = {i for i in tags}
    else:
        tag_set = {'', }

    app_win = NoteTaker(wndw_master, dt, title, get_subjects(), subject, tag_set, jlmnote)
    app_win.master.winfo_geometry()
    app_win.mainloop()


def build_jlmnote(now_stamp):

    jlmnote = JlmNote(now_stamp)

    return jlmnote


def handoff(jlmnote):

    pass

def get_subjects():

    with open(os.getenv('SUBJ_FILE'), 'r') as sbjct_f:
        subs = tuple((i.strip() for i in sbjct_f.readlines()))
        return subs


def update_tags(new_tags):
    with open(os.getenv('TAGS_FILE'), 'r+') as tags_f:
        tags = set((i.strip() for i in tags_f.readlines()))
        tags.update(new_tags)
        tags_f.writelines(i for i in tags)


def recv_entry(entry: str, jlmnote: JlmNote):
    jlmnote.set_content(entry)


def recv_title(title: str, jlmnote: JlmNote):
    jlmnote.set_title(title)


def recv_subj(subj: str, jlmnote: JlmNote):
    jlmnote.set_subject(subj)


def recv_tags(tags: set, jlmnote: JlmNote):
    jlmnote.set_tags(tags)
