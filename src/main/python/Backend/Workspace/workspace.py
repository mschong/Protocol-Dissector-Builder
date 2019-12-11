"""
Author : Daniel Ornelas
"""
class Workspace:
    """
    A class to store workspace information.

    A workspace contains metadata and information about the projects related to it.

    Attributes:
        name (string) : Name of the project.
        project (dict) : Dictionary containing paths to the projects linked to the workspace
        start_date (Date) : Date of workspace creation
        edit_date (Date) : Date of workspace last edited
        wpath (Date) : path to the workspace file (self)
        JSON : workspace attributes as json
    """

    name = None
    projects = None
    start_date = None
    edit_date = None
    wpath = None
    JSON = {
        'name' : name,
        'projects' : {},
        'created' : start_date,
        'edited': edit_date,
        'path' : wpath

    }

    def __init__(self, name=None, JSON=None):
        if JSON is None:
            self.name = name
        else:
            self.JSON = JSON
            self.name = JSON['name']
            self.projects = JSON['projects']
            self.start_date = JSON['created']
            self.edit_date = JSON['edited']
            self.wpath = JSON['path']

    def get_json(self):
        """
        Get workspace as json

        Yields: Workspace in json format
        """
        self.JSON['name'] = self.name
        self.JSON['projects'] = self.projects
        self.JSON['created'] = self.start_date
        self.JSON['edited'] = self.edit_date
        self.JSON['path'] = self.wpath
        return self.JSON

    def add_project_to_workspace(self, project):
        """
        Link a project to the workscape by adding it to the projects list

        Args:
            project (Project) : Project to be linked
        """
        if self.projects is None: #First project to be added
            self.projects = {}
            self.JSON['projects'] = {}
            self.JSON['projects'][0] = project
        else:
            size = len(self.projects)
            self.JSON['projects'][size] = project #Add project to last index
        self.projects = self.JSON['projects']
