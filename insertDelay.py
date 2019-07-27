import os
import xlrd 


#adjacencyListy = [(0, 1), (0, 2), (0, 4), (1, 2), (3, 4)]
#adjacencyListy = [(0, 10), (0, 4), (0, 6), (0, 7), (1, 11), (1, 7), (2, 10), (2, 12), (2, 6), (3, 9), (3, 7), (5, 10), (6, 9), (6, 10), (6, 7), (7, 9), (7, 10), (8, 11), (11, 13)]
#adjacencyListy=[(0, 12), (0, 6), (0, 14), (1, 28), (1, 9), (1, 12), (1, 25), (1, 31), (2, 8), (2, 3), (2, 12), (2, 29), (2, 30), (3, 28), (3, 10), (3, 23), (4, 28), (4, 15), (5, 9), (5, 17), (6, 14), (7, 15), (8, 25), (8, 28), (9, 12), (9, 28), (9, 23), (10, 26), (10, 30), (11, 12), (11, 29), (12, 34), (12, 17), (12, 26), (12, 28), (12, 30), (13, 18), (13, 28), (15, 22), (16, 32), (16, 35), (16, 30), (19, 30), (20, 21), (21, 26), (21, 27), (22, 29), (23, 28), (24, 30), (25, 28), (26, 28), (26, 29), (28, 32), (28, 29), (28, 30), (30, 36), (30, 31), (33, 36)]

#adjacencyListy = [(0, 20), (1, 32), (2, 17), (2, 28), (3, 40), (3, 13), (3, 30), (4, 28), (5, 28), (5, 19), (5, 20), (5, 38), (5, 14), (6, 41), (6, 36), (6, 22), (7, 16), (7, 18), (8, 25), (8, 26), (8, 11), (9, 41), (9, 19), (9, 28), (9, 12), (9, 23), (10, 14), (11, 41), (11, 13), (11, 14), (11, 23), (11, 28), (12, 28), (12, 22), (12, 14), (12, 41), (13, 28), (13, 38), (15, 41), (15, 22), (16, 41), (16, 18), (16, 28), (16, 38), (18, 35), (18, 41), (18, 21), (18, 22), (19, 37), (20, 28), (21, 24), (22, 39), (22, 27), (22, 28), (23, 28), (23, 33), (28, 34), (28, 41), (28, 36), (28, 29), (28, 31), (30, 41), (32, 41), (36, 37), (38, 41)]


adjacencyListy = [(0, 38), (0, 9), (0, 12), (0, 13), (0, 22), (0, 30), (1, 34), (1, 44), (1, 29), (2, 16), (2, 43), (2, 47), (3, 31), (4, 17), (4, 20), (5, 18), (5, 21), (6, 14), (7, 40), (7, 10), (7, 14), (8, 33), (9, 30), (10, 34), (10, 37), (10, 17), (10, 21), (10, 25), (10, 30), (11, 17), (11, 43), (11, 28), (11, 30), (12, 17), (14, 36), (14, 39), (14, 17), (14, 21), (14, 27), (14, 30), (15, 18), (17, 32), (17, 43), (17, 40), (17, 44), (17, 18), (17, 20), (17, 21), (17, 46), (17, 30), (17, 31), (18, 41), (19, 26), (19, 30), (20, 30), (21, 38), (21, 39), (21, 44), (21, 23), (21, 25), (21, 42), (21, 30), (22, 45), (22, 30), (24, 30), (25, 40), (25, 27), (30, 35), (30, 37), (30, 40), (30, 44), (30, 43), (30, 47), (31, 45), (31, 41), (33, 45), (34, 44), (35, 47), (37, 40), (40, 44), (42, 48), (43, 44)]


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
	file1.write("sudo dpkg -i tcconfig_0.19.0_amd64.deb\n")
	file1.write("sudo tc qdisc del dev eth0 root\n")
	file1.close()
	print((enodeDir[i]))

  
loc = ("minerDistribution.xls") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

sheet1 = wb.sheet_by_index(1) 

sheet.cell_value(0, 0) 

for i in range(13):
	print (i)
	delaysDirRow = {}
	for j in range(13):
            if sheet1.cell_value(i+1,j+1) == "":
                delaysDirRow[sheet1.cell_value(0,j+1)] = "0.4ms"
            else:
                delaysDirRow[sheet1.cell_value(0,j+1)] = 	sheet1.cell_value(i+1,j+1)
		#print (sheet1.cell_value(i+1,j+1),)
		#print (sheet1.cell_value(0,j))
	delaysDir[sheet1.cell_value(i+1,0)] = delaysDirRow




for pair in adjacencyListy:
	file1 = open("delays/delay"+str(pair[0])+".sh","a")
	print (pair[0],)
	print (pair[1],)
	print (enodeDir[pair[0]].strip('\n'),)
	print (enodeDir[pair[1]].strip('\n'),)
	print (sheet.cell_value(pair[0]+1,4),)
	print (sheet.cell_value(pair[1]+1,4))
	print (delaysDir[sheet.cell_value(pair[0]+1,4)][sheet.cell_value(pair[1]+1,4)],)
	delayValue=str(delaysDir[sheet.cell_value(pair[0]+1,4)][sheet.cell_value(pair[1]+1,4)])[:-2]
	print("delayValue : "+str(float(delayValue)),)
	file1.write("sudo tcset eth0 --add --delay "+str(float(delayValue))+"ms --dst-network "+enodeDir[pair[1]])
	file1.close()

	#print(("sudo tcset eth0 --add --delay "+str(delaysDir[sheet.cell_value(pair[0]+1,2)][sheet.cell_value(pair[1]+1,2)])+" --dst-network "+enodeDir[pair[1]].strip('\n')))





