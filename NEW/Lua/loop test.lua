-- Protocol Definition
protocol = Proto('loop test','loop to lua' )

 -- Declaration of fields
No Name 1 = ProtoField.int32('loop','loop test.loop',base.HEX) 
No Name 2 = ProtoField.unit24('dd','loop test.dd',base.OCT) 
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ No Name 1, No Name 2 } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "looping" )
 	 	 if response == 0 then 
	 subtree:add(No Name 1,buffer(0,1)) 
	 	 else 
	 subtree:add(No Name 2,buffer(0,3)) 
	 end 
end 
 
local port = DissectorTable.get("udp.port") 
port:add(1,protocol)