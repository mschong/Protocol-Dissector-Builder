
"""
Author : Daniel Ornelas
"""
class Project:
    """
    A class to store project information.

    A project has a 1:1 relation with a dissector.

    Attributes:
        name (string) : Name of the project
        date_created (Date) : Date of project creation
        edit_date (Date) : Last edited date
        description (string) : Description of the project
        protocol (string) : source layer of the dissector
        change_protocol (string) : Name to be given to subtree result of dissector
        src_port (int) : Source port number
        dst_port (int) : Destination port number
        author (string) : Author of the project
        path (string) : Path to the project file
        dissector (dict) : Dissector represented in json string format
    """
    name = None
    date_created = None
    edit_date = None
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
        'created' : date_created,
        'edited' : edit_date,
        'description' : description,
        'protocol' : protocol,
        'change_protocol': change_protocol,
        'src_port' : src_port,
        'dst_port' : dst_port,
        'author' : author,
        'dissector' : {},
        'path' : path
    }
    def __init__(self, name=None, JSON=None):
        if JSON is None:
            self.name = name
        else:
            self.JSON = JSON
            self.name = JSON['name']
            self.date_created = JSON['created']
            self.edit_date = JSON['edited']
            self.description = JSON['description']
            self.protocol = JSON['protocol']
            self.change_protocol = JSON['change_protocol']
            self.src_port = JSON['src_port']
            self.dst_port = JSON['dst_port']
            self.author = JSON['author']
            self.path = JSON['path']
            self.dissector = JSON['dissector']

    def add_fields(self, json):
        """
        Set dissector attribute

        Args:
            json : dissector fields in json format
        """
        self.dissector = json

    def get_json(self):
        """
        Get project as json

        Yields: project in json format
        """
        self.JSON['name'] = self.name
        self.JSON['created'] = self.date_created
        self.JSON['edited'] = self.edit_date
        self.JSON['description'] = self.description
        self.JSON['protocol'] = self.protocol
        self.JSON['change_protocol'] = self.change_protocol
        self.JSON['src_port'] = self.src_port
        self.JSON['dst_port'] = self.dst_port
        self.JSON['author'] = self.author
        self.JSON['path'] = self.path
        self.JSON['dissector'] = self.dissector
        return self.JSON
        