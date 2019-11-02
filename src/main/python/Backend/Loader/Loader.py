import datetime
import ntpath
import sys
import xml.etree.ElementTree as ET
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
sys.path.insert(1, "../../../../")
from Project import project
from Workspace import workspace
import os
import json


class Loader():

    workspace = None
    

    def __init__(self):
        self.workspace = workspace.Workspace()
        

    #WORKSAPCE FUNCTIONS

    '''
    save workspace information
    get JSON from current workspace and update json file
    '''
    def save_workspace(self):
            JSON = self.workspace.get_JSON()
            print(JSON)
           
            f = open("{}/{}.json".format(self.workspace.wpath.strip(),self.workspace.name.strip()) ,"w+")
            f.write(json.dumps(JSON))
            f.close()
    '''
    load a workspace already created
    Receives json filename, loads into JSON object and updates the current workspace object
    returns the name of the workspace
    '''
    def loadworkspace(self, filename):
        print("[+] Opening Workspace from {}".format(filename) )
        with open(filename) as f:
            data = json.loads(f.read())
        self.workspace = workspace.Workspace(JSON=data)
        self.project_pool = self.workspace.JSON['projects']
        return self.workspace.JSON
    '''
    Creates a new workspace object with the given name. saves the workspace afterwards.
    '''
    def new_workspace(self,ws_name,ws_created,ws_edited):
        self.workspace = workspace.Workspace(ws_name.strip(), None)
        self.workspace.startDate = ws_created
        self.workspace.editDate = ws_edited
        self.workspace.wpath = "{}/{}".format(os.getcwd().strip(),self.workspace.name.strip())
        os.mkdir(self.workspace.name.strip())
        self.save_workspace()
        return self.workspace.wpath

    '''
    Close a workspace
    '''
    def close_workspace(self):
        self.workspace = None
        self.project_pool = {}
  
       

   
    #Project functions
    def new_project(self,p_name,p_author,p_desc,p_created,p_edited,):
        
        p = project.Project(p_name.strip())
        p.description = p_desc
        p.dateCreated = p_created
        p.editDate =p_edited
        p.author = p_author
        p.path = "{}/{}.json".format(self.workspace.wpath,p.name)
        self.workspace.addProjectToWorkspace(p.path)
        self.save_project(p.path,p)
    

    def save_project(self,p_path,p):
        f = open("{}".format(p_path) ,"w+")
        f.write(json.dumps(p.get_JSON()))
        f.close()
        self.save_workspace()

    def import_project(self,filename):
        
     
        with open(filename) as f:
            data = json.loads(f.read())
            print("ABOUT TO PRINT DATA")
            print(data)
            print("DATA PRINTED")

        p = project.Project(JSON = data)
        p.path = "{}/{}.json".format(self.workspace.wpath,p.name) 
        self.workspace.addProjectToWorkspace(p.path)
        self.save_project(p.path,p)

            
    def open_project(self,p_name):
        pass


  



  
