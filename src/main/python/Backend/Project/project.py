
import sys
import os.path
import json 
class Project:
    
    name = None
    dateCreated = None
    editDate = None
    description = None
    protocol = None
    change_protocol = None
    src_port = None
    dst_port = None
    author = None
    path = None
    dissector = None

    JSON = {
        'name' : name,
        'created' : dateCreated,
        'edited' : editDate,
        'description' : description,
        'protocol' : protocol,
        'change_protocol': change_protocol,
        'src_port' : src_port,
        'dst_port' : dst_port,
        'author' : author,
        'dissector' : {},
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
           self.protocol = JSON['protocol']
           self.change_protocol = JSON['change_protocol']
           self.src_port = JSON['src_port']
           self.dst_port = JSON['dst_port']
           self.author = JSON['author']
           self.path = JSON['path']
           

 

     
   
    def get_JSON(self):
        self.JSON['name'] = self.name
        self.JSON['created'] = self.dateCreated
        self.JSON['edited'] = self.editDate
        self.JSON['description'] = self.description
        self.JSON['protocol'] = self.protocol
        self.JSON['change_protocol'] = self.change_protocol
        self.JSON['src_port'] = self.src_port
        self.JSON['dst_port'] = self.dst_port
        self.JSON['author'] = self.author
        self.JSON['path'] = self.path
        return self.JSON




