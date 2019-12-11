-- Protocol Definition
protocol = Proto('mongodb','mongodb Protocol' )

 -- Declaration of fields
message_length = ProtoField.int32('mongodb.message_length', 'messageLength', base.DEC) 
request_id = ProtoField.int32('mongodb.request_id', 'RequestID', base.DEC) 
response_to = ProtoField.int32('mongodb.response_to', 'responseTo', base.DEC) 
opcode = ProtoField.int32('mongodb.opcode', 'opCode', base.DEC) 
flags = ProtoField.int32('mongodb.flags', 'flags', base.DEC) 
full_coll_name = ProtoField.string('mongodb.full_coll_name', 'fullCollectionName', base.ASCII) 
number_to_skip = ProtoField.int32('mongodb.number_to_skip', 'numberToSkip', base.DEC) 
number_to_return = ProtoField.int32('mongodb.number_to_return', 'numberToReturn', base.DEC) 
query = ProtoField.none('mongodb.query', 'query', base.HEX) 
response_flags = ProtoField.int32('mongodb.response_flags', 'responseFlags', base.DEC) 
cursor_id = ProtoField.int32('mongodb.cursor_id', 'cursorId', base.DEC) 
starting_from = ProtoField.int32('mongodb.starting_from', 'startingFrom', base.DEC) 
number_returned = ProtoField.int32('mongodb.number_returned', 'numberReturned', base.DEC) 
document = ProtoField.none('mongodb.document', 'document', base.HEX) 
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ message_length, request_id, response_to, opcode, flags, full_coll_name, number_to_skip, number_to_return, query, response_flags, cursor_id, starting_from, number_returned, document } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "mongodb" )
 	 length = buffer:len() 
	 if(length == 0) then 
 -- CODEBLOCK START 
	 	 return
 -- CODEBLOCK END 
	 else 
 	 	 subtree:add_le(message_length,buffer(0,4)) 
	 	 subtree:add_le(request_id,buffer(4,4)) 
	 	 subtree:add_le(response_to,buffer(8,4)) 
	 	 opcode_number = buffer(12,4):le_uint() 
	 	 opcode_name = get_opcode_name(opcode_number) 
	 	 subtree:add(opcode,buffer(12,4)) 
	 	 if(opcode_name == "OP_QUERY") then 
 	 	 	 flags_number = buffer(16,4):le_uint() 
	 	 	 flags_description = get_flags_description(flag_number) 
	 	 	 subtree:add_le(flags,buffer(16,4)) 
	 	 	 string_length = 0 
	 	 	  for i=20, length-1, 1 do 
 	 	 	 	 if(buffer(i,1):le_uint() == 0) then 
 -- CODEBLOCK START 
	 	 	 	 	   string_length = i - 20
                break
 -- CODEBLOCK END 
	 	 	 	 else 
 	 	 	 	 end 
 	 	 	  end 
 	 	 	 	 	 	 subtree:add_le(full_coll_name,buffer(20,string_length)) 
	 	 	 subtree:add_le(number_to_skip,buffer(20 + string_length,4)) 
	 	 	 subtree:add_le(number_to_return,buffer(24 + string_length,4)) 
	 	 	 subtree:add_le(query,buffer(28 + string_length,length - string_length - 28)) 

	 	 else 
 	 	 	 if(opcode_name == "OP_REPLY") then 
 	 	 	 	 subtree:add_le(response_flags,buffer(16,4)) 
	 	 	 	 subtree:add_le(cursor_id,buffer(20,8)) 
	 	 	 	 subtree:add_le(starting_from,buffer(28,4)) 
	 	 	 	 subtree:add_le(number_returned,buffer(32,4)) 
	 	 	 	 subtree:add_le(document,buffer(36,length-36)) 
	 	 	 else 
 	 	 	 end 
 	 	 end 
 	 end 
 end 
 
local port = DissectorTable.get("tcp.port") 
port:add(27017,protocol)