-- Protocol Definition
protocol = Proto('MongoDB','MongoDB Protocol' )

 -- Declaration of fields
message_length = ProtoField.int32('MongoDB.message_length',messageLength,base.DEC) 
request_id = ProtoField.int32('MongoDB.request_id',RequestID,base.DEC) 
response_to = ProtoField.int32('MongoDB.response_to',responseTo,base.Select base) 
opcode = ProtoField.int32('MongoDB.opcode',opCode,base.DEC) 
flags = ProtoField.int32('MongoDB.flags',flags,base.DEC) 
full_coll_name = ProtoField.string('MongoDB.full_coll_name',fullCollectionName,base.OCT) 
number_to_skip = ProtoField.int32('MongoDB.number_to_skip',numberToSkip,base.DEC) 
number_to_return = ProtoField.int32('MongoDB.number_to_return',numberToReturn,base.DEC) 
query = ProtoField.none('MongoDB.query',query,base.HEX) 
response_flags = ProtoField.int32('MongoDB.response_flags',responseFlags,base.DEC) 
cursor_id = ProtoField.int32('MongoDB.cursor_id',cursorId,base.DEC) 
starting_from = ProtoField.int32('MongoDB.starting_from',startingFrom,base.DEC) 
number_returned = ProtoField.int32('MongoDB.number_returned',numberReturned,base.DEC) 
document = ProtoField.none('MongoDB.document',document,base.HEX) 
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ message_length, request_id, response_to, opcode, flags, full_coll_name, number_to_skip, number_to_return, query, response_flags, cursor_id, starting_from, number_returned, document } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "mongodb" )
 	 length = buffer:len()
 	 if length == 0 then 
 	 	 return
 	 	 	 else 
 	 	 subtree:add(message_length,buffer(0,4)) 
	 	 subtree:add(request_id,buffer(4,4)) 
	 	 subtree:add(response_to,buffer(8,4)) 
	 	  local opcode_number = buffer(12,4):le_uint()
    local opcode_name = get_opcode_name(opcode_number)
 	 	 subtree:add(opcode,buffer(12,4)) 
	 	 if opcode_name == "OP_QUERY" then 
 	 	 	 local flags_number = buffer(16,4):le_uint()
        local flags_description = get_flag_description(flags_number)
 	 	 	 subtree:add(flags,buffer(16,4)) 
	 	 	 local string_length
 	 	 	  for i=20, length-1, 1 
 	 do 
 	 	 	 	 if uffer(i,1):le_uint() == 0 then 
 	 	 	 	 	   string_length = i - 20
                break
 	 	 	 	 	 	 	 	 	 else 
 	 	 	 	 	 end 
 	 	 	  end 
  	 	 	 subtree:add(full_coll_name,buffer(20,1)) 
	 	 	 subtree:add(number_to_skip,buffer(21,4)) 
	 	 	 subtree:add(number_to_return,buffer(25,4)) 
	 	 	 subtree:add(query,buffer(29,1)) 
	 	 	 
	 	 else 
 	 	 	 if opcode_name == "OP_REPLY" then 
 	 	 	 	 subtree:add(response_flags,buffer(16,4)) 
	 	 	 	 subtree:add(cursor_id,buffer(20,8)) 
	 	 	 	 subtree:add(starting_from,buffer(28,4)) 
	 	 	 	 subtree:add(number_returned,buffer(32,4)) 
	 	 	 	 subtree:add(document,buffer(36,1)) 
	 	 	 	 	 	 	 else 
 	 	 	 	 end 
 end 
 end 
 end 
 
local port = DissectorTable.get("tcp.port") 
port:add(59274,protocol)