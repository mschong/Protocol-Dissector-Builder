class Protocol:
    def __init__(self,data):
        for attribute in data:
            setattr(self, attribute, data[attribute])
    def __iter__(self):
        for ProtocolField,ProtocolValue in self.__dict__.items():
            yield ProtocolField,ProtocolValue
