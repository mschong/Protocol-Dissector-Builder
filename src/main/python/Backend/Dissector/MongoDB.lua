protocol = Proto("MongoDB",  "MongoDB Protocol")


    message_length = ProtoField.int32("mess","length",base.DEC)

    request_id = ProtoField.int32("request_id","reqID",base.DEC)

    response_id = ProtoField.int32("response_id","resID",base.DEC)

    opcode = ProtoField.int32("opcode","opcode",base.DEC)


protocol.fields = {  message_length ,  request_id ,  response_id ,  opcode   }

function protocol.dissector(buffer, pinfo, tree)
  length = buffer:len()
  if length == 0 then return end

  pinfo.cols.protocol = protocol.name

  local subtree = tree:add(protocol, buffer(), "MongoDB Protocol Data")
  

    
{
    
    
        subtree:add(message_length,buffer(0,4))
               
    
        subtree:add(request_id,buffer(4,4))
               
    
        subtree:add(response_id,buffer(8,4))
               
    
        subtree:add(opcode,buffer(12,4))
               
    
  
end

local tcp_port = DissectorTable.get("tcp.port")
tcp_port:add(59274, protocol)