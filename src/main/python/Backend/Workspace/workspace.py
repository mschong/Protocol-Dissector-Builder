# Workspace class
# created by evazquez
#
# A Workspace for now will be a XML file with the following format
#
# <?xml version="1.0"?>
# <workspace name="workspace-template">
#     <project name="dissector-template">
#     </project>
# </workspace>
#
# Please note that we will need to agree (as a team) to define what a workspace and a project will be.
# For now, this will hopefully be sufficient for the presentation.
import json


class Workspace:
    name = None
    projects = None
    startDate = None
    editDate = None
    isEdited = False
    
   

    JSON = {
        'name' : name,
        'projects' : {},
        'created' : startDate,
        'edited': editDate,

    }

    
    def __init__(self, name = None ,JSON=None):
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
        self.JSON['projects'] = self.projects
        self.JSON['created'] = self.startDate
        self.JSON['edited'] = self.editDate
        return self.JSON


    def updateworkspace(self):
        print("[+] Updating workspace " + self.name)

    def addProjectToWorkspace(self,project):
        num_projects = len(self.workspace['projects'])
        
        self.workspace['projects']

        
    
