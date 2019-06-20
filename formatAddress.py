def formatAddress(fileName):
	matrixAddress = []
	sortAddress = []
	emptyAddress = []

	file = open(fileName, "r")
	data = file.readlines()

	for line in data:	
		info = line.rstrip().split(':')
		if info[0] == 'matrix': 
			matrixAddress.append(info[1])
		elif info[0] == 'sort':
			sortAddress.append(info[1])
		elif info[0] == 'empty': 
			emptyAddress.append(info[1])

	print("Matrix Address")
	print("{",)
	for item in matrixAddress:
		print("common.HexToAddress(\""+str(item)+"\"),") ,
	print("}")

	print("Sort Address")
	print("{",)
	for item in sortAddress:
		print("common.HexToAddress(\""+str(item)+"\"),") ,
	print("}")

	print("Empty Address")
	print("{",)
	for item in emptyAddress:
		print("common.HexToAddress(\""+str(item)+"\"),") ,
	print("}")


formatAddress('/home/sourav/EVD-Expt/allContractAddress')

