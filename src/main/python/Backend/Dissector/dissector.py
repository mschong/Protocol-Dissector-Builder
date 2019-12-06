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
        seen = set()
        self.parse_aux(value,JSON,seen)
        print("Done parsing lua file")

  

    def parse_aux(self,value,JSON,seen):
        if str(value) == 'END':
            return
        if value in seen:
            return
        wtype = JSON['dissector'][value]['Type']
        seen.add(value)
        if wtype == 'Decision' or wtype == 'while' or wtype == 'for':
            self.parse_aux(JSON['dissector'][value]['true'],JSON,seen)
            self.parse_aux(JSON['dissector'][value]['false'],JSON,seen)
            return
        elif  wtype == 'Field':
            self.parse_field(JSON['dissector'][value])
        return self.parse_aux(JSON['dissector'][value]['next_field'],JSON,seen)
            
    
    def parse_field(self,fieldJSON):
        temp = {}
        temp['name'] = fieldJSON['Name']
        temp['type'] = fieldJSON['Data Type'].lower()
        temp['abbrev'] = fieldJSON['Abbreviation']
        temp['desc'] = fieldJSON['Description']
        temp['size'] = self.get_size(fieldJSON['Var Size'])
        temp['display_type'] = fieldJSON['Base']
        if temp not in self.dissector['fields']:
            self.dissector['fields'].append(temp)
 
    def get_size(self,sizeJSON):
        size = sizeJSON['editText']
        if sizeJSON['combobox'] == "BITS":
            return int(size/2)
            
        elif sizeJSON['combobox'] == "Field" or sizeJSON['combobox'] == "Variable":
            return size
        else :
            return int(size)
            


    def fields_to_lua(self):
        fields_string = ""
        for field in self.dissector['fields']:
            field_string = "{} = ProtoField.{}('{}.{}','{}',base.{}) \n".format(field['name'],field['type'],self.dissector['name'],field['abbrev'],field['desc'],field['display_type'])
            fields_string += field_string   
        return fields_string

    def logic_to_lua(self,JSON):
        value = JSON['dissector']['START']
        print(value)
        data = self.logic_to_lua_aux(value," ",JSON,0,1)
        data += "end \n"
        return data

    def logic_to_lua_aux(self,value,result,JSON,offset,indent):
        print("curr : {}".format(value))
        #result += "\t " * indent
        if str(value) == 'END':
            return result
        curr = JSON['dissector'][value]
        wtype = JSON['dissector'][value]['Type']

        if wtype == 'End Loop':
            return result
        if  wtype == 'Field':
            print("OFFSET : {}".format(offset))
            if curr['LE'] == "true":
                r = "\t " * indent
                r += "subtree:add_le({},buffer({},{})) \n".format(curr['Name'],offset,self.get_size(curr['Var Size']))
            else:
                r = "\t " * indent
                r += "subtree:add({},buffer({},{})) \n".format(curr['Name'],offset,self.get_size(curr['Var Size']))
            if(self.is_number(self.get_size(curr['Var Size']))):
                print("IS NUMBER")
                chunks = str(offset).split(' ')
                if len(chunks) == 1:
                 
                    offset += self.get_size(curr['Var Size'])
                else :
                    
                    num = int(chunks[0])
                    print(num)
                    num += int(self.get_size(curr['Var Size']))
                    print(num)
                    chunks[0] = str(num)
                    offset = ' '.join(chunks)


            else:
                offset = '{} + {}'.format(str(offset),self.get_size(curr['Var Size']))
            result += r
            return self.logic_to_lua_aux(curr['next_field'],result,JSON,offset,indent)
        elif wtype == 'Decision':
            decision = curr['Condition']
            r = "\t " * indent
            r += "if({}) then \n ".format(self.get_decision(decision))
            result += self.logic_to_lua_aux(curr['true'],r,JSON,offset,indent+1)
            r = "\t " * indent
            r += "else \n "
           
            result += self.logic_to_lua_aux(curr['false'],r,JSON,offset,indent+1)
            result += "\t " * indent
            result += 'end \n '
            return result
        elif wtype == 'while':
            loop = curr['Condition']
            r = "while({})\n do \n ".format(self.get_decision(loop))
            result += self.logic_to_lua_aux(curr['true'],r,JSON,offset,indent+1)
            result += "\t " * indent
            result += 'end \n '
            r = " "
            result += self.logic_to_lua_aux(curr['false'],r,JSON,offset,indent+1)
            result += "\t " * indent
            result += '\n'
            return result
        elif wtype == 'for':
            loop = curr['Expressions']
            r = "\t " * indent
            r += " for {}, {}, {} do \n ".format(loop['exp1'],loop['exp2'],loop['exp3'])
            result += self.logic_to_lua_aux(curr['true'],r,JSON,offset,indent+1)
            result += "\t " * indent
            result += ' end \n '
            r = "\t " * indent
            result += self.logic_to_lua_aux(curr['false'],r,JSON,offset,indent)
            result += '\n'
            return result
        elif wtype == 'CodeBlock':
            result += "\t " * indent
            result += curr['Code']
            result += "\n "
            return self.logic_to_lua_aux(curr['next_field'],result,JSON,offset,indent)
        elif wtype == 'Variable': 
            result += "\t " * indent
            result += "{} {} {} = {} \n".format(curr['Scope'],curr['Data Type'],curr['Name'],self.get_value(curr['Data Type'],curr['Value']))
            return self.logic_to_lua_aux(curr['next_field'],result,JSON,offset,indent)
        elif wtype == 'Do While':
            pass

    def get_decision(self,decision_list):
        return " ".join(decision_list)

    def get_value(self,data_type,value):
        if data_type == 'number':
            if self.is_number(value):
                return int(value)
        return str(value)
    
    def is_number(self,num):
        try:
            int(num)
            return True
        except ValueError:
            return False

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
            else :
                f.write("{}, ".format(field['name']))
        f.write("} \n")
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
