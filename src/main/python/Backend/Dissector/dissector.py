from jinja2 import Environment, FileSystemLoader

class Dissector_Generator():
   
    dissector = {}

    
    

    def parse_json(self,JSON):
        self.dissector['name'] = JSON['name']
        self.dissector['description'] = JSON['description']
        self.dissector['subtree_name'] = JSON['change_protocol']
        self.dissector['port_type'] = JSON['protocol'] 
        self.dissector['port_number'] = JSON['src_port']
        self.dissector['fields'] = []
        value = JSON['dissector']['START']
        self.parse_aux(value,JSON)
        print("Done parsing lua file")

  

    def parse_aux(self,value,JSON):
        if str(value) == 'END':
            return
        wtype = JSON['dissector'][value]['Type']
        if  wtype == 'Field':
            self.parse_field(JSON['dissector'][value])
            return self.parse_aux(JSON['dissector'][value]['next_field'],JSON)
        else :
            self.parse_aux(JSON['dissector'][value]['true'],JSON)
            self.parse_aux(JSON['dissector'][value]['false'],JSON)
    
    def parse_field(self,fieldJSON):
        temp = {}
        temp['name'] = fieldJSON['Name']
        temp['type'] = fieldJSON['Data Type'].lower()
        temp['abbrev'] = fieldJSON['Abbreviation']
        temp['desc'] = fieldJSON['Description']
        temp['size'] = int(self.get_size(fieldJSON['Var Size']))
        temp['display_type'] = fieldJSON['Base']
        if temp not in self.dissector['fields']:
            self.dissector['fields'].append(temp)
 
    def get_size(self,sizeJSON):
        size = int(sizeJSON['editText'])
        if sizeJSON['combobox'] == "BITS":
            size /= 2
        return size

    def fields_to_lua(self):
        fields_string = ""
        for field in self.dissector['fields']:
            field_string = "{} = ProtoField.{}('{}','{}.{}',base.{}) \n".format(field['name'],field['type'],field['desc'],self.dissector['name'],field['abbrev'],field['display_type'])
            fields_string += field_string   
        return fields_string

    def logic_to_lua(self,JSON):
        value = JSON['dissector']['START']
        print(value)
        data = self.logic_to_lua_aux(value," ",JSON,0)
        data += "end \n"
        return data

    def logic_to_lua_aux(self,value,result,JSON,offset):
        if str(value) == 'END':
    
            return result
        curr = JSON['dissector'][value]
        wtype = JSON['dissector'][value]['Type']
        if  wtype == 'Field':
            r = "\t subtree:add({},buffer({},{})) \n".format(curr['Name'],offset,int(self.get_size(curr['Var Size'])))
            offset += int(self.get_size(curr['Var Size']))
            result += r
            return self.logic_to_lua_aux(curr['next_field'],result,JSON,offset)
        elif wtype == 'Decision':
            decision = curr['Condition']
            r = "\t if {} {} {} then \n \t".format(decision['operand1'],decision['operator1'],decision['operand2'])
            
            result += self.logic_to_lua_aux(curr['true'],r,JSON,offset)
            
            r = "\t else \n \t"
           
            result += self.logic_to_lua_aux(curr['false'],r,JSON,offset)
            
            result += '\t end \n \t'
            return result
        elif wtype == 'While':
            pass
            
    def no_jinja_headers(self,workspace,JSON):
        f = open("{}/Lua/{}.lua".format(workspace,self.dissector['name']) ,"w+")
        f.write("-- Protocol Definition\n")
        headers = "protocol = Proto('{}','{}' )\n".format(self.dissector['name'],self.dissector['description'])
        f.write(headers)
      
        f.write("\n -- Declaration of fields\n")
        fields = self.fields_to_lua()
        f.write("{} \n".format(fields))
        f.write("\n -- Adding fields to protocol fields attribute \n")
        f.write("protocol.fields ={ ")
        print("Writing fields")
        for field in self.dissector['fields']:
            if field == self.dissector['fields'][-1]:
                f.write(f"{field['name']} ")
                f.write("} \n")
            else :
                f.write("{}, ".format(field['name']))
        print("Fields completed")
        f.write("\n -- Dissector function \n")
        f.write("function protocol.dissector(buffer,pinfo,tree) \n")
        f.write("\t pinfo.cols.protocol = protocol.name \n")
        f.write('\t local subtree = tree:add(protocol, buffer(), "{}" )\n'.format(self.dissector['subtree_name']))
        logic = self.logic_to_lua(JSON)
        f.write("{} \n".format(logic))
       
        f.write('local port = DissectorTable.get("{}.port") \n'.format(self.dissector['port_type']))
        f.write('port:add({},protocol)'.format(self.dissector['port_number']))
        f.close()
        
    

 # def __init__(self):
        
    #     # self.file_loader = FileSystemLoader('src/main/python/Backend/Dissector/templates')
    #     # self.env = Environment(loader=self.file_loader)
    #     # self.template = self.env.get_template('dissector.lua')
        
       
    
    # def parse_json(self,JSON):
    #     print("Parsing to lua file")
    #     self.dissector['name'] = JSON['name']
    #     self.dissector['description'] = JSON['description']
    #     self.dissector['subtree_name'] = JSON['change_protocol']
    #     self.dissector['port_type'] = JSON['protocol'] #NEED TO ADD THIS FIELD
    #     self.dissector['port_number'] = JSON['src_port']
    #     self.dissector['fields'] = []
    #     self.dissector['decisions'] = []

    #     value = JSON['dissector']['START']
    #     print(value)

    #     while str(value) != 'END':
    #         wtype = JSON['dissector'][value]['Type']
    #         if  wtype == 'Field':
    #             parse_field(JSON['dissector'][value])
    #         elif wtype == 'Decision':
    #             parse_decision(JSON['dissector'][value])
    #         value = JSON['dissector'][value]['next_field']
    #         print(value)
    #     print("Done parsing lua file")
    
    # def parse_field(self,fieldJSON):
    #     temp = {}
    #     temp['name'] = fieldJSON['Name']
    #     temp['type'] = fieldJSON['Data Type'].lower()
    #     temp['abbrev'] = fieldJSON['Abbreviation']
    #     temp['desc'] = fieldJSON['Description']
    #     temp['size'] = int(self.get_size(fieldJSON['Var Size']))
    #     temp['display_type'] = ['Base']
    #     self.dissector['fields'].append(temp)

    # def parse_decision(self,decisionJSON):
    #     temp = {}
    #     conditions = decisionJSON['Condition']
    #     temp['operand1'] = conditions['operand1']
    #     temp['operator1'] = conditions['operator1']
    #     temp['operand2'] = conditions['operand2']
        
    #     #HANDLE TRUE OR FALSE


    # def get_size(self,sizeJSON):
    #     size = sizeJSON['editText']
    #     if sizeJSON['combobox'] == "BYTES":
    #         size *= 2
    #     return size

    # def export_lua(self,workspace):
    #     print("Exporting to lua file")
    #     output = self.template.render(dis = self.dissector)
    #     print(output)
    #     if workspace is None:
    #         f = open("{}.lua".format(self.dissector['name']) ,"w+")
    #     else:
    #         f = open("{}/Lua/{}.lua".format(workspace,self.dissector['name']) ,"w+")
    #     f.write(output)
    #     f.close()
    #     print("Lua file exported into workspace/Lua")