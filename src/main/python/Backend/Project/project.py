
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

    def __init__(self, name = None, JSON = None):
        if JSON == None:
            self.name = name
        else:
           self.JSON = JSON
           self.name = JSON['name']
           self.projects = JSON['projects']
           self.startDate = JSON['created']
           self.editDate = JSON['edited']

 

     
   
    def get_JSON(self):
        self.JSON['name'] = self.name
        self.JSON['created'] = self.startDate
        self.JSON['edited'] = self.editDate
        self.JSON['description'] = self.description
        self.JSON['author'] = self.author
        return self.JSON




