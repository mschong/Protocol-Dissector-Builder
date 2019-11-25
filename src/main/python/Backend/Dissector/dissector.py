from jinja2 import Environment, FileSystemLoader

class Dissector_Generator():
   
    dissector = {}
  
    def __init__(self):
      
        self.file_loader = FileSystemLoader('src/main/python/Backend/Dissector/templates')
        self.env = Environment(loader=self.file_loader)
        self.template = self.env.get_template('dissector.lua')
       
    
    def parse_json(self,JSON):
        print("Parsing to lua file")
        self.dissector['name'] = JSON['name']
        self.dissector['description'] = JSON['description']
        self.dissector['subtree_name'] = JSON['change_protocol']
        self.dissector['port_type'] = JSON['protocol'] #NEED TO ADD THIS FIELD
        self.dissector['port_number'] = JSON['src_port']
        self.dissector['fields'] = []

        value = JSON['dissector']['START']
        print(value)

        while str(value) != 'END':
            temp = {}
            temp['name'] = JSON['dissector'][value]['Name']
            temp['type'] = JSON['dissector'][value]['Data Type'].lower()
            temp['filter'] = JSON['dissector'][value]['Abbreviation']
            temp['label'] = JSON['dissector'][value]['Description']
            temp['size'] = int(self.get_size(JSON['dissector'][value]['Var Size']))
            temp['display_type'] = JSON['dissector'][value]['Base']
            self.dissector['fields'].append(temp)
            value = JSON['dissector'][value]['next_field']
            print(value)
        print("Done parsing lua file")
    
    def get_size(self,sizeJSON):
        size = sizeJSON['editText']
        if sizeJSON['combobox'] == "BYTES":
            size *= 2
        return size

    def export_lua(self,workspace):
        print("Exporting to lua file")
        output = self.template.render(dis = self.dissector)
        print(output)
        if workspace is None:
            f = open("{}.lua".format(self.dissector['name']) ,"w+")
        else:
            f = open("{}/Lua/{}.lua".format(workspace,self.dissector['name']) ,"w+")
        f.write(output)
        f.close()
        print("Lua file exported into workspace/Lua")

if __name__ == "__main__":

    message_length = {}
    message_length['name'] = "message_length"
    message_length['type'] = "int32"
    message_length['filter'] = "mess"
    message_length['label'] = "length"
    message_length['size'] = 4
    message_length['display_type'] = "DEC"
    message_length['next_field'] = 'request'

    request = {}
    request['name'] = "request_id"
    request['type'] = "int32"
    request['filter'] = "request_id"
    request['label'] = "reqID"
    request['size'] = 4
    request['display_type'] = "DEC"
    request['next_field'] = 'end_field'

    JSON = {}
    JSON['name'] = "ddd"
    JSON['description'] = "TST"
    JSON['protocol'] = "TCP"
    JSON['change_protocol'] = "TEST"
    JSON['src_port'] = "800"
    JSON['fields'] ={}
    JSON['fields']['start_field']= {}
    JSON['fields']['start_field']['next_field'] = 'message_length'
    JSON['fields']['message_length'] = message_length
    JSON['fields']['request'] = request

   


   
    c.parse_json(JSON)
    c.export_lua(None)