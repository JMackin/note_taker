import io
import os


class FileMaker:

    def __init__(self, jlmnote):
        # JlmNote.note_attrs = {'timestamp': self.ts, 'title': self.title, 'subject': self.subject, 'tags': self.tags}
        attrs = jlmnote.get_attrs()
        self.subject = attrs['timestamp']
        self.title = attrs['title']
        self.content = attrs['content']
        self.iscmd = attrs['iscmd']
        self.tag_set = attrs['tag_set']

    def write_to_file(self):

        with open(os.fspath(str(self.title + '.jlmtxt')), 'w') as fo:
            fo.write(str(self.content))

    def setisCmd(self, iscmd):
        self.iscmd = iscmd

    def get_is_cmd(self):
        return True if self.isCmd else False

    def add_tags(self, *tags):
        pass

    