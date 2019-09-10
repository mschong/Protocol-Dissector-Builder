#
# This class defines a Project
# TODO: We need to define all attributes of project.
# a project can contain 0 to many bit, byte, multi-bit, multi-byte, length widgets, loops
# and conditonal edges
# created by evazquez
#
import sys
class Project:
    attributes = []
    name = None

    def __init__(self, name):
        self.name = name