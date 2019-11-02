
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
    path = None

    JSON = {
        'name' : name,
        'created' : dateCreated,
        'edited' : editDate,
        'description' : description,
        'author' : author,
        'path' : path
    }

    def __init__(self, name = None, JSON = None):
        if JSON == None:
            self.name = name
        else:
           self.JSON = JSON
           self.name = JSON['name']
        
           self.dateCreated = JSON['created']
           self.editDate = JSON['edited']
           self.description = JSON['description']
           self.author = JSON['author']
           self.path = JSON['path']

 

     
   
    def get_JSON(self):
        self.JSON['name'] = self.name
        self.JSON['created'] = self.dateCreated
        self.JSON['edited'] = self.editDate
        self.JSON['description'] = self.description
        self.JSON['author'] = self.author
        self.JSON['path'] = self.path
        return self.JSON




