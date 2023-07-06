import NoteTaker.take_note
from NoteTaker import take_note, make_file, db_agent
import datetime


class Orchestrator:

    def __init__(self):

        self.dt = datetime
        self.dt_now = self.dt.datetime.now()
        self.ts = self.dt.date.strftime(self.dt_now, '%d%m%y-%H%M%S')
        self.jlmnote = None
        self.build_jlmnote()
        self.filemaker = None

    def receive(self, jlmnote):
        self.jlmnote = jlmnote

    def call_filemaker(self):
        if self.jlmnote is None:
            self.jlmnote = take_note.build_jlmnote(tuple((self.dt, self.ts)))

        self.filemaker = make_file.FileMaker(self.jlmnote)

    def set_timestamp(self):
        self.dt = datetime
        self.dt_now = self.dt.datetime.now()
        self.ts = self.dt.date.strftime(self.dt_now, '%d%m%y-%H%M%S')

    def get_note_attrs(self):
        return self.jlmnote.get_attrs()

    def build_jlmnote(self):
        self.jlmnote = take_note.JlmNote(self.ts)

    def get_jlmnote(self):
        return self.jlmnote

    def run_gui(self):
        dt_tup = tuple((self.dt.datetime, self.ts))
        take_note.make_note_gui(self.jlmnote, ts=dt_tup)
