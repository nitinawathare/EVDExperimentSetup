import os

adjacencyListy = [(0, 1), (0, 2), (0, 4), (1, 2), (3, 4)]
enodeDir = []
#i=0
with open('static.txt') as fp:
    for line in fp:
    	#print line
    	enodeDir.append(line)

length = len(enodeDir)
for i in range(length): 
    file1 = open("staticJsonFiles/static.json"+str(i),"w") 
    file1.write("["+"\n")
    file1.close()
    print(enodeDir[i])

for pair in adjacencyListy:  
	file1 = open("staticJsonFiles/static.json"+str(pair[0]),"a")
	file2 = open("staticJsonFiles/static.json"+str(pair[1]),"a")
	file1.write('"'+enodeDir[pair[1]].strip('\n')+'"'+","+"\n")
	file2.write('"'+enodeDir[pair[0]].strip('\n')+'"'+","+"\n")
	file1.close()
	file2.close()

for i in range(length): 
	file1 = open("staticJsonFiles/static.json"+str(i),"a") 
	file1.seek(-2, os.SEEK_END)
	file1.truncate()
	file1.write("\n"+"]"+"\n")