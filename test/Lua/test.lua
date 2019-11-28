-- Protocol Definition
protocol = Proto('test','test' )

 -- Declaration of fields
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "test" )
 global number size = 8 
end 
 
local port = DissectorTable.get("test.port") 
port:add(1,protocol)