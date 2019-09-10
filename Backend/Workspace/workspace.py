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

class Workspace:
    name = None
    projects = None

    def __init__(self, name, projects):
        print("[+] Initializing Workspace " + name)
        self.name = name
        self.projects = projects

    def updateworkspace(self):
        print("[+] Updating workspace " + self.name)
