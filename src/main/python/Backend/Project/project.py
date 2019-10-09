
import sys
import os.path
import json 
class Project:
    attributes = []
    name = None
    dateCreated = None
    editDate = None
    description = None
    author = None

    JSON = {
        'name' : name,
        'created' : dateCreated,
        'edited' : editDate,
        'description' : description,
        'author' : author
    }

    def __init__(self, name):
        self.name = name

    def save_project(self,filename,file_contents=None):
    
        f = open(filename ,"w+")
        f.write(json.dumps(self.JSON))
        f.close()

    def open_project(self,filename):
        if os.path.isfile(filename):
            f = open(filename,"r")
            if f.mode == 'r':
                content = f.read()
                print(content)
        else:
            print("File not found - {0}".format(filename))

