-- Protocol Definition
protocol = Proto('gamespy','gamespy protocol' )

 -- Declaration of fields
 

 -- Adding fields to protocol fields attribute 
protocol.fields ={ } 

 -- Dissector function 
function protocol.dissector(buffer,pinfo,tree) 
	 pinfo.cols.protocol = protocol.name 
	 local subtree = tree:add(protocol, buffer(), "gamespy" )
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
 	 local number index = 1 
	 local string decoded = "" 
	 local number size = buffer:len() 
	  for i=0, size-1, 1 do 
 	 	 local number res = 0 
	 	 local number c = 0 
	 	 local number a = 0 
	 	 local number b = 0 
	 	 a = buffer(i,1):uint()
b = cipher[index]
 while(a > 0  and b > 0)
 do 
 	 	 	 local number a2 = a % 16 
	 	 	 local number b2 = b % 16 
	 	 	  res = res + tab[a2+1][b2+1]*c
    a = (a-a2)/16
    b = (b-b2)/16
    c = c*16
 	 	 end 
  	 	 	 res = res + a*c + b*c

 	 	 	 decoded = decoded .. string.char(res)
		
		index = index + 1
 	 	 	 if index == 8 then 
 	 	 	 	 index = 1
 	 	 	 else 
 	 	 	 end 
 	 	 
	  end 
 	
    subtree:add(buffer(0,size), "Decoded: " .. decoded)
 
end 
 
local port = DissectorTable.get("tcp.port") 
port:add(28900,protocol)