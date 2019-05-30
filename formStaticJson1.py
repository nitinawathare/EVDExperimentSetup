import os

#adjacencyListy = [(0, 1), (0, 2), (0, 4), (1, 2), (3, 4)]
#adjacencyListy = [(0, 12), (0, 6), (0, 14), (1, 28), (1, 9), (1, 12), (1, 25), (1, 31), (2, 8), (2, 3), (2, 12), (2, 29), (2, 30), (3, 28), (3, 10), (3, 23), (4, 28), (4, 15), (5, 9), (5, 17), (6, 14), (7, 15), (8, 25), (8, 28), (9, 12), (9, 28), (9, 23), (10, 26), (10, 30), (11, 12), (11, 29), (12, 34), (12, 17), (12, 26), (12, 28), (12, 30), (13, 18), (13, 28), (15, 22), (16, 32), (16, 35), (16, 30), (19, 30), (20, 21), (21, 26), (21, 27), (22, 29), (23, 28), (24, 30), (25, 28), (26, 28), (26, 29), (28, 32), (28, 29), (28, 30), (30, 36), (30, 31), (33, 36)]

enodeDir = []
#i=0
with open('static.txt') as fp:
    for line in fp:
    	#print line
    	enodeDir.append(line)

length = len(enodeDir)
counter = 0
for i in range(length): 
	file1 = open("staticJsonFiles/static.json"+str(i)+"_"+str(i),"w") 
	file1.write("["+"\n")
	file1.write('"'+enodeDir[counter].strip('\n')+'"'+"\n")
	file1.write("]")
	file1.close()
	counter = counter+1
	#print(enodeDir[i])