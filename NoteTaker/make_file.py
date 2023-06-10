import os

class FileMaker:

    def __init__(self, subject: str, title: str, content: str, tag_set: set = None):
        self.subject = subject
        self.title = title
        self.content = content
        if tag_set is not None:
            self.tag_set = tag_set


    def open_write_file(self):
        file_stream = open(self.title)


    def add_tags(self, *tags):
        s_tag = self.note_tags.get()

        if s_tag not in self.note_tags.get():
            pass
