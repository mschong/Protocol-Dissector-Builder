
import sys
import os.path

class Project:
    attributes = []
    name = None

    def __init__(self, name):
        self.name = name

    def save_project(self,filename,file_contents=None):
    
        f = open(filename ,"w+")
        f.write(file_contents)
        f.close()

    def open_project(self,filename):
        if os.path.isfile(filename):
            f = open(filename,"r")
            if f.mode == 'r':
                content = f.read()
                print(content)
        else:
            print("File not found - {0}".format(filename))