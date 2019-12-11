-- Protocol Definition
protocol = Proto('gamespy','Gamespy protocol' )

 -- Declaration of fields
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "gamespy" )
 -- CODEBLOCK START 
	 local tab = {  -- tab[i][j] = xor(i-1, j-1)
  {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, },
  {1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, },
  {2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, },
  {3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12, },
  {4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11, },
  {5, 4, 7, 6, 1, 0, 3, 2, 13, 12, 15, 14, 9, 8, 11, 10, },
  {6, 7, 4, 5, 2, 3, 0, 1, 14, 15, 12, 13, 10, 11, 8, 9, },
  {7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8, },
  {8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, },
  {9, 8, 11, 10, 13, 12, 15, 14, 1, 0, 3, 2, 5, 4, 7, 6, },
  {10, 11, 8, 9, 14, 15, 12, 13, 2, 3, 0, 1, 6, 7, 4, 5, },
  {11, 10, 9, 8, 15, 14, 13, 12, 3, 2, 1, 0, 7, 6, 5, 4, },
  {12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3, },
  {13, 12, 15, 14, 9, 8, 11, 10, 5, 4, 7, 6, 1, 0, 3, 2, },
  {14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 0, 1, },
  {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, },
}
cipher = {103, 97, 109, 101, 115, 112, 121}
size = buffer:len()
 -- CODEBLOCK END 
	 index = 1 
	 decoded = "" 
	  for i=0, size-1, 1 do 
 	 	 res = 0 
	 	 c = 1 
	 	 a = 0 
	 	 b = 0 
-- CODEBLOCK START 
	 	 a = buffer(i,1):uint()
b = cipher[index]
 -- CODEBLOCK END 
while(a > 0 and b > 0)
 do 
 	 	 	 a2 = 0 
	 	 	 b2 = 0 
-- CODEBLOCK START 
	 	 	 a2 = a%16
b2 = b%16
 -- CODEBLOCK END 
-- CODEBLOCK START 
	 	 	 res = res + tab[a2+1][b2+1]*c
  a = (a-a2)/16
  b = (b-b2)/16
  c = c*16
 -- CODEBLOCK END 
	 	 end 
  -- CODEBLOCK START 
	 	 	 res = res + a*c + b*c
 -- CODEBLOCK END 
-- CODEBLOCK START 
	 	 	 decoded = decoded .. string.char(res)
index = index + 1

 -- CODEBLOCK END 
	 	 	 if(index == 8) then 
 -- CODEBLOCK START 
	 	 	 	 index = 1
 -- CODEBLOCK END 
	 	 	 else 
 	 	 	 end 
 	 	 
	  end 
 	 -- CODEBLOCK START 
	 subtree:add(buffer(0,size), "Decoded: " .. decoded)
 -- CODEBLOCK END 

end 
 
local port = DissectorTable.get("tcp.port") 
port:add(28900,protocol)