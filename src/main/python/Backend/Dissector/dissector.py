'''
Author : Daniel Ornelas
'''
class DissectorGenerator():
    '''
    Class to handle all dissector generation functions

    Attributes:
        dissector (dict) : Dictionary containing dissector to be exported
    '''
    dissector = {}

    def parse_json(self, json):
        '''
        Parse dissector json into less detailed json containing only dissector related fields

        Args:
            json : dissector in json format
        '''
        #Set basic dissector fields
        self.dissector['name'] = json['name']
        self.dissector['description'] = json['description']
        self.dissector['subtree_name'] = json['change_protocol']
        self.dissector['port_type'] = json['protocol']
        self.dissector['port_number'] = json['src_port']
        self.dissector['fields'] = []
        #Get start of dissector
        value = json['dissector']['START']
        #Initialize set to avoid field duplication
        seen = set()
        self.parse_aux(value, json, seen)
        print("Done parsing lua file")

    def parse_aux(self, value, json, seen):
        '''
        Auxiliary recursive function to parse dissector

        Args:
            value: current field
            json: the complete fields json
            seen: set of visited fields
        '''
        if str(value) == 'END':
            return
        if value in seen:
            return
        #Get type of field
        wtype = json['dissector'][value]['Type']
        seen.add(value)
        #Recurse the true and false paths
        if wtype in ('Decision', 'while', 'for'):
            self.parse_aux(json['dissector'][value]['true'], json, seen)
            self.parse_aux(json['dissector'][value]['false'], json, seen)
            return
        #parse the field
        if  wtype == 'Field':
            self.parse_field(json['dissector'][value])
        return self.parse_aux(json['dissector'][value]['next_field'], json, seen)

    def parse_field(self, field_json):
        '''
        Function to parse field attributes into the dissector.
        Args:
            field_json : current field as json
        '''
        #Create temporary dict to store fields
        temp = {}
        temp['name'] = field_json['Name']
        temp['type'] = field_json['Data Type'].lower()
        temp['abbrev'] = field_json['Abbreviation']
        temp['desc'] = field_json['Description']
        #Calculate field size
        temp['size'] = self.get_size(field_json['Var Size'])
        temp['display_type'] = field_json['Base']
        #add field if it has not been added before
        if temp not in self.dissector['fields']:
            self.dissector['fields'].append(temp)

    def get_size(self, size_json):
        '''
        Get the size of a field

        Args:
            size_json : field size json value
        Yields:
            field size: as int if size are bytes or as string if defined by another variable
        '''
        size = size_json['editText']
        #convert to bytes
        if size_json['combobox'] == "BITS":
            return int(size/2)
        #return string value if variable or field
        if size_json['combobox'] == "Field" or size_json['combobox'] == "Variable":
            return size
        #already in bytes
        return int(size)

    def fields_to_lua(self):
        '''
        Declare fields in lua script

        Yields : Fields declaration string in lua
        '''
        fields_string = ""
        #Traverse fields and add to a string
        for field in self.dissector['fields']:
            field_string = "{} = ProtoField.{}('{}.{}', '{}', base.{}) \n".format(field['name'], field['type'], self.dissector['name'], field['abbrev'], field['desc'], field['display_type'])
            fields_string += field_string
        return fields_string

    def logic_to_lua(self, json):
        '''
        Generate dissect function for lua script

        Args:
            json : dissector as a json
        Yields:
            data string containing dissect function
        '''
        #Get start of dissector
        value = json['dissector']['START']
        print(value)
        #Call recursive auxiliary function
        data = self.logic_to_lua_aux(value, " ", json, 0, 1)
        #Add end statement
        data += "end \n"
        return data

    def logic_to_lua_aux(self, value, result, json, offset, indent):
        '''
        Auxiliary recursive function  to process dissect function

        Args:
            value : the current field
            result : the current resulting string
            json : the fields json
            offset : the current field size offset
            indent : level of lua script indentation
        Yields:
            String containing dissect function
        '''
        print("curr : {}".format(value))
        if str(value) == 'END':
            return result
        #Get current field and type
        curr = json['dissector'][value]
        wtype = json['dissector'][value]['Type']
        if wtype == 'End Loop':
            return result
        #Process fields
        if  wtype == 'Field':
            #Add field on correct endian format
            if curr['LE'] == "true":
                res = "\t " * indent
                res += "subtree:add_le({},buffer({},{})) \n".format(curr['Name'], offset, self.get_size(curr['Var Size']))
            else:
                res = "\t " * indent
                res += "subtree:add({},buffer({},{})) \n".format(curr['Name'], offset, self.get_size(curr['Var Size']))
            #Process field size when size is fixed
            if self.is_number(self.get_size(curr['Var Size'])):
                #split size value by space
                chunks = str(offset).split(' ')
                #length of 1 indicates only an integer, safe to add the current size
                if len(chunks) == 1:
                    offset += self.get_size(curr['Var Size'])
                #length > 1 indicates variable size, add to current bytes and append variable
                else:
                    num = int(chunks[0])
                    print(num)
                    num += int(self.get_size(curr['Var Size']))
                    print(num)
                    chunks[0] = str(num)
                    offset = ' '.join(chunks)
            #Process field size when size is variable
            else:
                offset = '{} + {}'.format(str(offset), self.get_size(curr['Var Size']))
            result += res
            return self.logic_to_lua_aux(curr['next_field'], result, json, offset, indent)
        #Process decision fields by traversing on true and false paths
        elif wtype == 'Decision':
            decision = curr['Condition']
            res = "\t " * indent
            res += "if({}) then \n ".format(self.get_decision(decision))
            result += self.logic_to_lua_aux(curr['true'], res, json, offset, indent+1)
            res = "\t " * indent
            res += "else \n "
            result += self.logic_to_lua_aux(curr['false'], res, json, offset, indent+1)
            result += "\t " * indent
            result += 'end \n '
            return result
        #Process while loops. parse conditions and recurse true false
        elif wtype == 'while':
            loop = curr['Condition']
            res = "while({})\n do \n ".format(self.get_decision(loop))
            result += self.logic_to_lua_aux(curr['true'], res, json, offset, indent+1)
            result += "\t " * indent
            result += 'end \n '
            res = " "
            result += self.logic_to_lua_aux(curr['false'], res, json, offset, indent+1)
            result += "\t " * indent
            result += '\n'
            return result
        #Process for loops, parse conditions and recurse true false
        elif wtype == 'for':
            loop = curr['Expressions']
            res = "\t " * indent
            res += " for {}, {}, {} do \n ".format(loop['exp1'], loop['exp2'], loop['exp3'])
            result += self.logic_to_lua_aux(curr['true'], res, json, offset, indent+1)
            result += "\t " * indent
            result += ' end \n '
            res = "\t " * indent
            result += self.logic_to_lua_aux(curr['false'], res, json, offset, indent)
            result += '\n'
            return result
        #Process codeblocks, get codeblock data and store in result
        elif wtype == 'CodeBlock':
            result += "\t " * indent
            result += curr['Code']
            result += "\n "
            return self.logic_to_lua_aux(curr['next_field'], result, json, offset, indent)
        #Process variables,
        elif wtype == 'Variable':
            result += "\t " * indent
            result += "{} = {} \n".format(curr['Name'], self.get_value(curr['Data Type'], curr['Value']))
            return self.logic_to_lua_aux(curr['next_field'], result, json, offset, indent)

    def get_decision(self, decision_list):
        '''
        Process decision fields

        Args:
            decision_list : list of decision operators and operands
        Yields:
            String adding the list values separated by a space
        '''
        #Replace OR,AND,!= to lua accepted values
        for i, item in enumerate(decision_list):
            if item in ("OR", "AND"):
                decision_list[i] = item.lower()
            if item == "!=":
                decision_list[i] = "~="
        return " ".join(decision_list)

    def get_value(self, data_type, value):
        '''
            Get value for variable fields

            Args:
                data_type : type of data for the field
                value : value of the field
            Yields:
                value as int if is a number or as string if is a variable or string
        '''
        if data_type == 'number':
            #check if value is number or reference to another variable
            if self.is_number(value):
                return int(value)
        return str(value)

    def is_number(self, num):
        '''
        Check if input is a number

        Args:
            num : number to be processed
        Yields:
            true if is a number, otherwise false
        Raises:
            ValueError: if input is not a valid number
        '''
        try:
            int(num)
            return True
        except ValueError:
            return False

    def add_headers(self, workspace, json):
        '''
        In charge of writing to lua file

        Args:
            workspace: current workspace
            json: project json
        '''
        #Create lua file in corresponding directory
        f = open("{}/Lua/{}.lua".format(workspace, self.dissector['name']), "w+")
        #Write boilerplate code
        f.write("-- Protocol Definition\n")
        headers = "protocol = Proto('{}','{}' )\n".format(self.dissector['name'], self.dissector['description'])
        f.write(headers)
        f.write("\n -- Declaration of fields\n")
        #Declare fields
        fields = self.fields_to_lua()
        f.write("{} \n".format(fields))
        f.write("\n -- Adding fields to protocol fields attribute \n")
        f.write("protocol.fields ={ ")
        print("Writing fields")
        for field in self.dissector['fields']:
            #Skip comma if last field
            if field == self.dissector['fields'][-1]:
                f.write(f"{field['name']} ")
            else:
                f.write("{}, ".format(field['name']))
        f.write("} \n")
        print("Fields completed")
        f.write("\n -- Dissector function \n")
        f.write("function protocol.dissector(buffer,pinfo,tree) \n")
        f.write("\t pinfo.cols.protocol = protocol.name \n")
        f.write('\t local subtree = tree:add(protocol, buffer(), "{}" )\n'.format(self.dissector['subtree_name']))
        #Get dissect function string
        logic = self.logic_to_lua(json)
        f.write("{} \n".format(logic))
        f.write('local port = DissectorTable.get("{}.port") \n'.format(self.dissector['port_type']))
        f.write('port:add({},protocol)'.format(self.dissector['port_number']))
        f.close()
