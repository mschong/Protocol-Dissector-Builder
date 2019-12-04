-- Protocol Definition
protocol = Proto('health','Health Protocol' )

 -- Declaration of fields
version_buffer = ProtoField.int8('health.version',Version,base.DEC) 
field_health = ProtoField.int8('health.code',Code,base.HEX) 
groupid = ProtoField.int16('health.group',Group ID,base.DEC) 
workerguid = ProtoField.guid('health.guid',Worked ID,base.NONE) 
generated_health_name = ProtoField.string('health.status',Health Status,base.NONE) 
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ version_buffer, field_health, groupid, workerguid, generated_health_name } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "health" )
 	 subtree:add(version_buffer,buffer(0,1)) 
	 subtree:add(field_health,buffer(1,1)) 
	 subtree:add(groupid,buffer(2,2)) 
	 subtree:add(workerguid,buffer(4,16)) 
	 local table health_code_table = {"Healthy,"High Load","Failure"} 
	 local string health_code = buffer(1,1):uint() 
	 local string health_string = health_code_table[health_code] 
	 subtree:add(generated_health_name,buffer(20,1)) 
	 end 
 
local port = DissectorTable.get("udp.port") 
port:add(55055,protocol)