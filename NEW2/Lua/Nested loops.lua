-- Protocol Definition
protocol = Proto('Nested loops','testing nested loops' )

 -- Declaration of fields
length = ProtoField.unit16('length of field','Nested loops.len',base.OCT) 
No Name 4 = ProtoField.double('fff','Nested loops.fffff',base.DEC) 
No Name 2 = ProtoField.int64('ee','Nested loops.ee',base.HEX) 
No Name 3 = ProtoField.unit64('ff','Nested loops.ff',base.HEX) 
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ length, No Name 4, No Name 2, No Name 3 } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "ud" )
 	 subtree:add(length,buffer(0,4)) 
	 if length => 0 then 
 		 if response > 4 then 
 		 subtree:add(No Name 4,buffer(4,1)) 
	 else 
 		 subtree:add(No Name 2,buffer(4,5)) 
	 end 
 		 else 
 		 if hello <= 4 then 
 		 subtree:add(No Name 2,buffer(4,5)) 
	 else 
 		 subtree:add(No Name 3,buffer(4,4)) 
	 end 
 		 end 
 	end 
 
local port = DissectorTable.get("tcp.port") 
port:add(919,protocol)