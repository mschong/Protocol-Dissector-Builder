from jinja2 import Environment, FileSystemLoader

class Dissector_Generator():
    dissector = {}
    dissector['name'] = "MongoDB"
    dissector['description'] = "MongoDB Protocol"
    dissector['subtree_name'] = "MongoDB Protocol Data"
    dissector['port_type'] = "tcp"
    dissector['port_number'] = "59274"
    message_length = {}
    message_length['name'] = "message_length"
    message_length['type'] = "int32"
    message_length['filter'] = "mess"
    message_length['label'] = "length"
    message_length['size'] = 4
    message_length['display_type'] = "DEC"

    request = {}
    request['name'] = "request_id"
    request['type'] = "int32"
    request['filter'] = "request_id"
    request['label'] = "reqID"
    request['size'] = 4
    request['display_type'] = "DEC"

    response = {}
    response['name'] = "response_id"
    response['type'] = "int32"
    response['filter'] = "response_id"
    response['label'] = "resID"
    response['size'] = 4
    response['display_type'] = "DEC"

    opcode = {}
    opcode['name'] = "opcode"
    opcode['type'] = "int32"
    opcode['filter'] = "opcode"
    opcode['label'] = "opcode"
    opcode['size'] = 4
    opcode['display_type'] = "DEC"

    dissector['fields'] = [message_length,request,response,opcode]

    def __init__(self):
        
        self.file_loader = FileSystemLoader('templates')
        self.env = Environment(loader=self.file_loader)
        self.template = self.env.get_template('dissector.lua')
       

    def export_lua(self):

        output = self.template.render(dis = self.dissector)
        print(output)
        f = open("{}.lua".format(self.dissector['name']) ,"w+")
        f.write(output)
        f.close()

if __name__ == "__main__":
    c = Dissector_Generator()
    c.export_lua()