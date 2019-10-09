import datetime
import ntpath
import sys
import xml.etree.ElementTree as ET
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
sys.path.insert(1, "../../../../")
from Project import project
from Workspace import workspace
import json


class Loader():

    workspace = None
    project_pool = []

  
    def save_workspace(self):
            JSON = self.workspace.get_JSON()
            f = open("{}.json".format(self.workspace.name) ,"w+")
            f.write(json.dumps(JSON))
            f.close()
    
    def loadworkspace(self, file):
        print("[+] Opening Workspace from {}".format(file) )
        with open(file) as f:
            data = json.loads(f.read())
        self.workspace = workspace.Workspace(JSON=data)
        return self.workspace.name
      
    def new_workspace(self,ws_name,ws_created,ws_edited):
        self.workspace = workspace.Workspace(ws_name, None)
        self.workspace.startDate = ws_created
        self.workspace.editDate = ws_edited
        self.save_workspace()
  
       

   
    

  



  
