-- Protocol Definition
protocol = Proto('Nested loops','testing nested loops' )

 -- Declaration of fields
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ 
 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "ud" )
 print('Hello World');
end 
 
local port = DissectorTable.get("tcp.port") 
port:add(919,protocol)