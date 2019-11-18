import pytest
from project import Project

def test_create_project_firstparam():
    project = Project("New project")
    assert project.name == "New project"
    assert project.JSON['name'] == None
    assert project.JSON['created'] == None
    assert project.JSON['edited'] == None
    assert project.JSON['description'] == None
    assert project.JSON['author'] == None

def test_create_project_secondparam():
    project = Project(None , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'author': "lorna"
    })
    assert project.name == "New project in JSON"
    assert project.JSON['name'] == "New project in JSON"
    assert project.JSON['created'] == "10/31/2019"
    assert project.JSON['edited'] == "10/31/2019"
    assert project.JSON['description'] == "filler description for testing purposes"
    assert project.JSON['author'] == "lorna"
    assert project.startDate == "10/31/2019"
    assert project.editDate == "10/31/2019"

def test_create_project_allparams():
    project = Project("New project" , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'author': "lorna"
    })
    assert project.name == "New project"
    assert project.JSON['name'] == "New project in JSON"
    assert project.JSON['created'] == "10/31/2019"
    assert project.JSON['edited'] == "10/31/2019"
    assert project.JSON['description'] == "filler description for testing purposes"
    assert project.JSON['author'] == "lorna"
    assert project.startDate == "10/31/2019"
    assert project.editDate == "10/31/2019"
    

def test_create_project_without_params():
    project = Project()
    assert project.name == None
    assert project.JSON['name'] == None
    assert project.JSON['projects'] == None
    assert project.JSON['created'] == None
    assert project.JSON[''] 

def test_get_JSON():
    project = Project("New project" , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'author': "lorna"
    })
    test_json = project.get_JSON()
    assert test_json['name'] == "New project in JSON"
    assert test_json['created'] == "10/31/2019"
    assert test_json['edited'] == "10/31/2019"
    assert test_json['description'] == "filler description for testing purposes"
    assert test_json['author'] == "lorna"
