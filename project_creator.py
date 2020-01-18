from project_items import File, Folder
import os
import json

class StructureReader(object):

    def read_folder_from_dict(self, folder_dict):
        folder_name = folder_dict.get('name')
        description = folder_dict.get('description')
        result = Folder(name=folder_name,
                        description=description,
                        path='')
        files = folder_dict.get('files', [])
        folders = folder_dict.get('subfolders', [])

        for f in files:
            result.add_file(self.read_file_from_dict(f))

        for f in folders:
            folder = self.read_folder_from_dict(f)
            result.add_subfolder(folder)

        return result

    def read_file_from_dict(self, file_dict):
        result = File(name=file_dict.get('name'))
        result.content = file_dict.get('content')
        return result

    def print_cwd(self):
        return os.getcwd()

class StructureDumper(object):

    def file_to_dict(self, file):

        file_dict = {}
        name = file.name
        content = file.content
        file_dict['name'] = name
        file_dict['content'] = content
        return file_dict

    def folder_to_dict(self, folder):

        name = folder.name
        description = folder.description
        files = [self.file_to_dict(f) for f in folder.get_files()]
        subfolders = [self.folder_to_dict(sf) for sf in folder.get_folder()]
        path = folder.get_path()

        folder_dict = {'name': name,
                       'description': description,
                       'path': path,
                       'subfolders': subfolders,
                       'files': files}

        return folder_dict


class ProjectCreator(object):

    def __init__(self, project_file, project_name, project_path):
        self.structure_reader = StructureReader()
        with open(project_file,'r') as f:
            self.project_dict = json.load(f)
        self.project = self.structure_reader.read_folder_from_dict(self.project_dict)
        self.project.path = project_path
        self.name = project_name
        self.project_dict['path'] = project_path
        self.project_dict['name'] = project_name



    def read_structure_from_dict(self, project_dict):
        project = self.structure_reader.read_folder_from_dict(project_dict)
        return project

    def write_file(self, file, path):

        with open(path,'w') as f:
            f.write(file.content)

    def write_folder(self, subfolder=None, mother_folder_path='', is_root=True):

        if subfolder is None:
            subfolder = self.project

        if not mother_folder_path:
            mother_folder_path = self.project.path

        if is_root:
            os.mkdir(subfolder.path)
        else:
            subfolder.path = os.path.join(mother_folder_path, subfolder.name)
            os.mkdir(subfolder.path)

        files_path = subfolder.path
        for file in subfolder.get_files():
            if file is None:
                break
            file_path = os.path.join(files_path, file.name)
            self.write_file(file,file_path)

        for sf in subfolder.get_folder():
            if sf is None:
                break
            self.write_folder(sf,mother_folder_path=subfolder.path,is_root=False)

if __name__=='__main__':
    pc = ProjectCreator('data_science_structure','Test Project',"/home/vlad/Projects/Test Project")
    pc.write_folder()






