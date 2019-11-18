protocol = Proto("TEST",  "TST")


    message_length = ProtoField.int32("mess","length",base.DEC)

    request_id = ProtoField.int32("request_id","reqID",base.DEC)


protocol.fields = {  message_length ,  request_id   }

function protocol.dissector(buffer, pinfo, tree)
  length = buffer:len()
  if length == 0 then return end

  pinfo.cols.protocol = protocol.name

  local subtree = tree:add(protocol, buffer(), "TEST")
  

    
{
    
    
        subtree:add(message_length,buffer(0,4))
               
    
        subtree:add(request_id,buffer(4,4))
               
    
  
end

local tcp_port = DissectorTable.get("tcp.port")
tcp_port:add(800, protocol)