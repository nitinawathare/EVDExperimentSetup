import os
import xlrd 


'''adjacencyListy = [(0, 1), (0, 2), (0, 4), (1, 2), (3, 4)]
enodeDir = []

with open('ipList') as fp:
    for line in fp:
    	enodeDir.append(line)

length = len(enodeDir)
for i in range(length): 
	file1 = open("delays/delay"+str(i)+".sh","w") 
	file1.write("#!/bin/bash\n")
	file1.write("wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb\n")
	file1.write("sudo dpkg -i tcconfig_0.19.0_amd64.deb\n")
	file1.close()
	print(enodeDir[i])

delay = 0
for pair in adjacencyListy: 
	file1 = open("delays/delay"+str(pair[0])+".sh","a")
	file1.write("tcset ens3 --add --delay "+str(delay)+"ms --dst-network "+enodeDir[pair[1]])
	file1.close()'''

  
loc = ("minerDistribution.ods") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
sheet.cell_value(0, 0) 
print(sheet.row_values(1))