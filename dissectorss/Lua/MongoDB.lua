protocol = Proto("MongoDB",  "MongoDB Protocol")


    message_length = ProtoField.int8("mongodb.messagelen","messageLength",base.DEC)

    request_id = ProtoField.int32("mongodb.requestid","requestID",base.DEC)

    response_to = ProtoField.int32("mongodb.response","responseTo",base.DEC)

    opcode = ProtoField.int32("mongodb.opcode","Opcode",base.DEC)


protocol.fields = {  message_length ,  request_id ,  response_to ,  opcode   }

function protocol.dissector(buffer, pinfo, tree)
  length = buffer:len()
  if length == 0 then return end

  pinfo.cols.protocol = protocol.name

  local subtree = tree:add(protocol, buffer(), "mongodb")
  

    

    
    
        subtree:add(message_length,buffer(0,4))
               
    
        subtree:add(request_id,buffer(4,4))
               
    
        subtree:add(response_to,buffer(8,4))
               
    
        subtree:add(opcode,buffer(12,22))
               
    
  
end

local port = DissectorTable.get("tcp.port")
port:add(59274, protocol)