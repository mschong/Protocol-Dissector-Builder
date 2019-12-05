import pytest
from project import Project

def test_create_project_firstparam():
    project = Project("New project")
    assert project.name == "New project"
    assert project.editDate == None
    assert project.description == None
    assert project.protocol == None
    assert project.change_protocol == None
    assert project.src_port == None
    assert project.dst_port == None
    assert project.author == None
    assert project.path == None
    assert project.dissector == None

def test_create_project_secondparam():
    project = Project(None , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'protocol': "UDP",
        'change_protocol': "TCP",
        'src_port': "1234",
        'dst_port': "8080",
        'author': "author1",
        'path': "",
        'dissector': ""

    })
    assert project.name == "New project in JSON"
    assert project.JSON['name'] == "New project in JSON"
    assert project.JSON['created'] == "10/31/2019"
    assert project.JSON['edited'] == "10/31/2019"
    assert project.JSON['author'] == "author1"
    assert project.JSON['description'] == "filler description for testing purposes"
    assert project.JSON['protocol'] == "UDP"
    assert project.JSON['change_protocol'] == "TCP"
    assert project.JSON['src_port'] == "1234"
    assert project.JSON['dst_port'] == "8080"
    assert project.JSON['author'] == "author1"
    assert project.JSON['path'] == ""
    assert project.JSON['dissector'] == ""
    assert project.dateCreated == "10/31/2019"
    
    assert project.editDate == "10/31/2019"
    assert project.description == "filler description for testing purposes"
    assert project.protocol == "UDP"
    assert project.change_protocol == "TCP"
    assert project.src_port == "1234"
    assert project.dst_port == "8080"
    assert project.author == "author1"
    assert project.path == ""
    assert project.dissector == None

def test_create_project_allparams():
    project = Project("New project" , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'protocol': "UDP",
        'change_protocol': "TCP",
        'src_port': "1234",
        'dst_port': "8080",
        'author': "author1",
        'path': "",
        'dissector': ""
    })
    assert project.name == "New project in JSON"
    assert project.JSON['name'] == "New project in JSON"
    assert project.JSON['created'] == "10/31/2019"
    assert project.JSON['edited'] == "10/31/2019"
    assert project.JSON['description'] == "filler description for testing purposes"
    assert project.JSON['author'] == "author1"
    assert project.JSON['protocol'] == "UDP"
    assert project.JSON['change_protocol'] == "TCP"
    assert project.JSON['src_port'] == "1234"
    assert project.JSON['dst_port'] == "8080"
    assert project.JSON['path'] == ""
    assert project.JSON['dissector'] == ""

    assert project.editDate == "10/31/2019"
    assert project.description == "filler description for testing purposes"
    assert project.protocol == "UDP"
    assert project.change_protocol == "TCP"
    assert project.src_port == "1234"
    assert project.dst_port == "8080"
    assert project.author == "author1"
    assert project.path == ""
    assert project.dissector == None
    

def test_create_project_without_params():
    project = Project()
    assert project.name == None
    assert project.editDate == None
    assert project.description == None
    assert project.protocol == None
    assert project.change_protocol == None
    assert project.src_port == None
    assert project.dst_port == None
    assert project.author == None
    assert project.path == None
    assert project.dissector == None

def test_get_JSON():
    project = Project("New project" , JSON = {
        'name' : "New project in JSON",
        'created' : "10/31/2019",
        'edited' : "10/31/2019",
        'description': "filler description for testing purposes",
        'protocol': "UDP",
        'change_protocol': "TCP",
        'src_port': "1234",
        'dst_port': "8080",
        'author': "author1",
        'path': "",
        'dissector': ""
    })

    test_json = project.get_JSON()

    assert test_json['name'] == "New project in JSON"
    assert test_json['created'] == "10/31/2019"
    assert test_json['edited'] == "10/31/2019"
    assert test_json['description'] == "filler description for testing purposes"
    assert test_json['author'] == "author1"
    assert test_json['protocol'] == "UDP"
    assert test_json['change_protocol'] == "TCP"
    assert test_json['src_port'] == "1234"
    assert test_json['dst_port'] == "8080"
    assert test_json['path'] == ""
    assert test_json['dissector'] == None