class Field:
    def __init__(self,data):
        self.showname= ""
        self.size=0
        for attribute in data:
            setattr(self, attribute, data[attribute])
