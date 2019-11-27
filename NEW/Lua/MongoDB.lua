-- Protocol Definition
protocol = Proto('MongoDB','MongoDB Protocol' )

 -- Declaration of fields
message_length = ProtoField.int8('messageLength','MongoDB.mongodb.messagelen',base.DEC) 
request_id = ProtoField.int32('requestID','MongoDB.mongodb.requestid',base.DEC) 
response_to = ProtoField.int32('responseTo','MongoDB.mongodb.response',base.DEC) 
opcode = ProtoField.int32('Opcode','MongoDB.mongodb.opcode',base.DEC) 
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ message_length, request_id, response_to, opcode } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "mongodb" )
 	 subtree:add(message_length,buffer(0,2)) 
	 subtree:add(request_id,buffer(2,2)) 
	 subtree:add(response_to,buffer(4,2)) 
	 subtree:add(opcode,buffer(6,2)) 
end 
 
local port = DissectorTable.get("tcp.port") 
port:add(59274,protocol)