"""
Contains typical project structure elements: files and folders.

"""
import os

class Project(object):

    def __init__(self):
        pass

class Folder(object):

    def __init__(self, name, path, description=''):
        self.name = name
        self.description = description
        self.subfolders = []
        self.files = []
        self.path = path

    def add_subfolder(self, subfolder):
        subfolder.add_path(os.path.join(self.get_path(),subfolder.name))
        self.subfolders.append(subfolder)

    def add_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def remove_subfolder(self, name):
        self.subfolders = [f for f in self.subfolders if f.name != name]

    def add_file(self, file):
        self.files.append(file)

    def remove_file(self, name):
        self.subfolders = [f for f in self.files if f.name != name]

    def add_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def get_folder(self):
        for folder in self.subfolders:
            yield folder

    def get_files(self):
        for file in self.files:
            yield file


class File(object):

    def __init__(self, name):

        self.name = name
        self.content = ''

