import os
import xlrd 


#adjacencyListy = [(0, 1), (0, 2), (0, 4), (1, 2), (3, 4)]
adjacencyListy = [(0, 10), (0, 4), (0, 6), (0, 7), (1, 11), (1, 7), (2, 10), (2, 12), (2, 6), (3, 9), (3, 7), (5, 10), (6, 9), (6, 10), (6, 7), (7, 9), (7, 10), (8, 11), (11, 13)]

IpCountryMapping = {}
enodeDir = []
delaysDir = {}

with open('ipList') as fp:
    for line in fp:
    	enodeDir.append(line)

length = len(enodeDir)
for i in range(length): 
	file1 = open("delays/delay"+str(i)+".sh","w") 
	file1.write("#!/bin/bash\n")
	#file1.write("wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb\n")
	#file1.write("sudo dpkg -i tcconfig_0.19.0_amd64.deb\n")
	file1.write("sudo tc qdisc del dev eth0 root\n")
	file1.close()
	print(enodeDir[i])

  
loc = ("minerDistribution.xls") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

sheet1 = wb.sheet_by_index(1) 

sheet.cell_value(0, 0) 

for i in range(13):
        print i
	delaysDirRow = {}
	for j in range(13):
            if sheet1.cell_value(i+1,j+1) == "":
                delaysDirRow[sheet1.cell_value(0,j+1)] = "0.4ms"
            else:
                delaysDirRow[sheet1.cell_value(0,j+1)] = 	sheet1.cell_value(i+1,j+1)
		#print sheet1.cell_value(i+1,j+1),
		#print sheet1.cell_value(0,j)
	delaysDir[sheet1.cell_value(i+1,0)] = delaysDirRow




for pair in adjacencyListy:
	file1 = open("delays/delay"+str(pair[0])+".sh","a")
	print pair[0],
        print pair[1],
        print enodeDir[pair[0]].strip('\n'),
	print enodeDir[pair[1]].strip('\n'),
        print sheet.cell_value(pair[0]+1,4),
        print sheet.cell_value(pair[1]+1,4)
	print delaysDir[sheet.cell_value(pair[0]+1,4)][sheet.cell_value(pair[1]+1,4)],
	file1.write("sudo tcset eth0 --add --delay "+str(delaysDir[sheet.cell_value(pair[0]+1,4)][sheet.cell_value(pair[1]+1,4)])+" --dst-network "+enodeDir[pair[1]])
	file1.close()

	#print("sudo tcset eth0 --add --delay "+str(delaysDir[sheet.cell_value(pair[0]+1,2)][sheet.cell_value(pair[1]+1,2)])+" --dst-network "+enodeDir[pair[1]].strip('\n'))




