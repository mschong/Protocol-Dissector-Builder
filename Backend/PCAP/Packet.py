class Packet:
    def __init__(self,data):
        for attribute in data:
            setattr(self, attribute, data[attribute])
    def __iter__(self):
        for PacketField,PacketValue in self.__dict__.items():
            yield PacketField,PacketValue
