"""
Authors:
    Daniel Ornelas
    Ernesto Vazquez
"""
import os
import json
import sys
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
sys.path.insert(1, "../../../../")
from Backend.Project import project
from Backend.Workspace import workspace
from Backend.Dissector import dissector
from Backend.Writer import writer
class Loader():
    """
    This class works as a manager for dissector, project, and workspace classes.

    Delegate data coming from pyro to inner classes.

    Attributes:
        workspace (Workspace) saves a reference to the current loaded workspace
    """
    workspace = None

    def __init__(self):
        print("sys.path: ", sys.path)
        self.workspace = workspace.Workspace()
    #WORKSAPCE FUNCTIONS
    def save_workspace(self):
        '''
        save workspace information
        get JSON from current workspace and update json file
        '''
        JSON = self.workspace.get_json()
        print(JSON)
        #Save workspace in .pdbws extension
        path = self.workspace.wpath.strip()
        name = self.workspace.name.strip()
        _file = open("{}/{}.pdbws".format(path, name), "w+")
        _file.write(json.dumps(JSON, indent=4))
        _file.close()

    def load_workspace(self, filename):
        '''
        load a workspace already created.

        Args:
            filename (string) : path to workspace file
        Yields:
            Name of the loaded workspace
        '''
        print("[+] Opening Workspace from {}".format(filename))
        with open(filename) as _file:
            data = json.loads(_file.read())
        self.workspace = workspace.Workspace(JSON=data)
        return self.workspace.JSON

    def new_workspace(self, ws_name, ws_created, ws_edited):
        '''
        Creates a new workspace object with the given name. saves the workspace afterwards.

        Args:
            ws_name (String) : name of the workspace
            ws_created (Date) : Date of creation
            ws_edited (Date) : Current date
        Yields:
            Path to newly created workspace file
        '''
        #store workspace reference
        self.workspace = workspace.Workspace(ws_name.strip(), None)
        self.workspace.start_date = ws_created
        self.workspace.edit_date = ws_edited
        self.workspace.wpath = "{}/{}".format(os.getcwd().strip(), self.workspace.name.strip())
        #Create directories needed by thhe workspace
        os.mkdir(self.workspace.name.strip())
        os.mkdir("{}/Lua".format(self.workspace.wpath))
        #Save the workspace
        self.save_workspace()
        return self.workspace.wpath

    def close_workspace(self):
        '''
        Close a workspace
        '''
        self.workspace = None
    #Project functions
    def new_project(self, p_name, p_author, p_desc,
                    p_created, p_edited, protocol, change_protocol, src_port, dst_port):
        '''
        Create a new project.
        Args:
            p_name (String) : name of project.
            p_author (string) : name of author.
            p_desc (string) : description of project
            p_created (Date) : Date of creation
            p_edited (Date) : Current date
            protocol (string) : source protocol layer
            change_protocol (string) : subtree protocol name
            src_port (int) : Source port number
            dst_port (int) : Destination port number

        '''
        #Set project attributes
        proj = project.Project(p_name.strip())
        proj.description = p_desc
        proj.date_created = p_created
        proj.edit_date = p_edited
        proj.author = p_author
        proj.path = "{}/{}.pdbproj".format(self.workspace.wpath, proj.name)
        proj.protocol = protocol
        proj.change_protocol = change_protocol
        proj.src_port = src_port
        proj.dst_port = dst_port
        #Add project to current workspace and save it
        self.workspace.add_project_to_workspace(proj.path)
        self.save_project(proj.path, proj)

    def save_project(self, p_path, proj):
        '''
        Save project to .pdbproj extension file in json format

        Args:
            p_path (string) : path to project file
            proj (Project) : project to be saved
        '''
        _file = open("{}".format(p_path), "w+")
        _file.write(json.dumps(proj.get_json(), indent=4))
        _file.close()
        #save workspace after adding project
        self.save_workspace()

    def import_project(self, filename):
        '''
        Import an existing project from another workspace

        Args:
            filename : path to file of project to be imported
        '''
        with open(filename) as _file:
            data = json.loads(_file.read())
        #Create .pdbproj file in current workspace, add to project and save
        proj = project.Project(JSON=data)
        proj.path = "{}/{}.pdbproj".format(self.workspace.wpath, proj.name)
        self.workspace.add_project_to_workspace(proj.path)
        self.save_project(proj.path, proj)

    def save_dissector_attributes(self, fields, workspace, p_name):
        '''
        Save dissector json into project.

        Args:
            fields (String) : dissector fields in json format
            workspace (string) : path to workspace file
            p_name (string) : name of project in which data will be saved
        '''
        #load workspace and get current project
        ws_json = self.load_workspace(workspace)
        p_path = "{}/{}.pdbproj".format(ws_json['path'], p_name)
        with open(p_path) as _file:
            p_json = json.loads(_file.read())
            print("JSON = {}".format(p_json))
        #Create project, add fields, and save
        proj = project.Project(JSON=p_json)
        proj.add_fields(fields)
        self.save_project(p_path, proj)

    def get_dissector_attributes(self, workspace, p_name):
        '''
        Get dissector from a project

        Args:
            worskpace (Workspace) : Workspace to read from
            p_name (string) : name of project to read from
        Yields:
            dissector attributes as json
        '''
        #Get workspace and project files
        ws_json = self.load_workspace(workspace)
        print("ws json: {}".format(ws_json))
        p_path = "{}/{}.pdbproj".format(ws_json['path'], p_name)
        print("project path: {}".format(p_path))
        with open(p_path) as _file:
            p_json = json.loads(_file.read())
        print("project json: {}".format(p_json))
        return p_json['dissector']
    #Dissector Functions
    def export_lua_script(self, workspace, project):
        '''
        Generates current project dissector as lua file

        Args:
            workspace (string) : workspace to read fron
            project (string) : name of selected project
        '''
        ws_json = self.load_workspace(workspace)
        p_path = "{}/{}.pdbproj".format(ws_json['path'], project)
        with open(p_path) as _file:
            p_json = json.loads(_file.read())
        print("JSON = {}".format(p_json))
        #send json to generator class
        generator = dissector.DissectorGenerator()
        generator.parse_json(p_json)
        generator.add_headers(ws_json['path'], p_json)
