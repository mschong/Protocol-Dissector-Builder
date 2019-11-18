import pytest
from workspace import Workspace
from project import Project

def test_create_workspace_firstparam():
    workspace = Workspace("New Workspace")
    assert workspace.name == "New Workspace"
    assert workspace.JSON['name'] == None
    assert workspace.JSON['projects'] == {}
    assert workspace.JSON['created'] == None
    assert workspace.JSON['edited'] == None
    assert workspace.JSON['path'] == None

def test_create_workspace_secondparam():
    workspace = Workspace(None , JSON = {
        'name' : "New Workspace in JSON",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    assert workspace.name == "New Workspace in JSON"
    assert workspace.JSON['name'] == "New Workspace in JSON"
    assert workspace.JSON['projects'] == {}
    assert workspace.JSON['created'] == "10/31/2019"
    assert workspace.JSON['edited'] == "10/31/2019"
    assert workspace.JSON['path'] == 'path'

def test_create_workspace_allparams():
    workspace = Workspace( "New Workspace", JSON = {
        'name' : "New Workspace",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    assert workspace.name == "New Workspace"
    assert workspace.JSON['projects'] == {}
    assert workspace.JSON['created'] == "10/31/2019"
    assert workspace.JSON['edited'] == "10/31/2019"
    assert workspace.JSON['path'] == 'path'
    

def test_create_workspace_without_params():
    workspace = Workspace()
    assert workspace.name == None
    assert workspace.JSON['name'] == None
    assert workspace.JSON['projects'] == {}
    assert workspace.JSON['created'] == None
    assert workspace.JSON['edited'] == None
    assert workspace.JSON['path'] == None

def test_get_JSON():
    workspace = Workspace(None , JSON = {
        'name' : "New Workspace in JSON",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    assert workspace.name == "New Workspace in JSON"
    
    test_json = workspace.get_JSON()
    assert test_json['name'] == "New Workspace in JSON"
    assert test_json['projects'] == {}
    assert test_json['created'] == "10/31/2019"
    assert test_json['edited'] == "10/31/2019"
    assert test_json['path'] == 'path'
    
def test_addProjectToWorkspace_oneProject():
    project = Project("New project" , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'author': "lorna"
    })
    
    workspace = Workspace( "New Workspace", JSON = {
        'name' : "New Workspace",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    
    workspace.addProjectToWorkspace(project)
    test_json = workspace.get_JSON()

    assert test_json['projects'][0] == project
    assert workspace.projects[0] == project


def test_addProjectToWorkspace_twoProjects():
    project1 = Project("New project 1" , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'author': "lorna"
    })

    project2 = Project("New project 2" , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'author': "lorna"
    })
    
    workspace = Workspace( "New Workspace", JSON = {
        'name' : "New Workspace",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    
    workspace.addProjectToWorkspace(project1)
    workspace.addProjectToWorkspace(project2)
    test_json = workspace.get_JSON()

    assert test_json['projects'][0] == project1
    assert workspace.projects[0] == project1
    assert test_json['projects'][1] == project2
    assert workspace.projects[1] == project2


def test_addProjectToWorkspace_noProject():
    workspace = Workspace( "New Workspace", JSON = {
        'name' : "New Workspace",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    
    workspace.addProjectToWorkspace()
    test_json = workspace.get_JSON()

    assert test_json['projects'] == None
    assert workspace.projects == None


def test_addProjectToWorkspace_int():
    workspace = Workspace( "New Workspace", JSON = {
        'name' : "New Workspace",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019"
    })
    
    workspace.addProjectToWorkspace(1)
    test_json = workspace.get_JSON()

    assert test_json['projects'] == None
    assert workspace.projects == None


def test_addProjectToWorkspace_string():
    workspace = Workspace( "New Workspace", JSON = {
        'name' : "New Workspace",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    
    workspace.addProjectToWorkspace("random string")
    test_json = workspace.get_JSON()

    assert test_json['projects'] == None
    assert workspace.projects == None


def test_addProjectToWorkspace_float():
    workspace = Workspace( "New Workspace", JSON = {
        'name' : "New Workspace",
        'projects' : {},
        'created' : "10/31/2019",
        'edited': "10/31/2019",
        'path' : 'path'
    })
    
    assert workspace.addProjectToWorkspace(1.0) == None

