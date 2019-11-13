# # To compute Bessel value of given k, x
# def computeBessel(k, x, bsTh):
# 	m=0
# 	bsTh = math.pow(2,-40)
# 	besselVal = 0
# 	prevTerm = 100
# 	while True:
# 		term1 = Decimal(-1)
# 		term2 = Decimal(1.0)
# 		term3 = Decimal(1.0)
# 		if m%2==0:
# 			term1 = Decimal(1)
					
# 		term2 = Decimal(math.pow(x/Decimal(2), 2*m+k))
# 		term2 = term2/fact(m)
# 		term2 = term2/fact(m+k)

# 		termProb = term1*term2
# 		besselVal = besselVal+termProb
# 		if abs(termProb-prevTerm) < bsTh:
# 			break
# 		prevTerm = termProb	
# 		m=m+1

# 	print("besselVal", "m", m, round(besselVal,10))
# 	return besselVal



# # We want the Pr[A-B>0]> 1-bwTh
# def skellamBound(meanH, meanA):	
# 	termTh = Decimal(math.pow(2,-32)) # Terminate computing probability of each term
# 	bsTh = Decimal(math.pow(2,-32))	# Stop computing Bessel if each term is smaller
# 	sProb = Decimal(0)
# 	k=1
# 	# print("meanH: ", round(meanH,5),"meanA: ", round(meanA,5))
# 	while True: 
# 		term1 = Decimal(math.exp(Decimal(-1)*(meanH+meanA)))
# 		meanRatio = meanH/meanA
# 		term2 = Decimal(math.pow(meanRatio,k/2))	
# 		x = Decimal(2.0)*Decimal(math.sqrt(meanH*meanA))
# 		term3 = computeBessel(k, x, bsTh)

# 		termProb = term1*term2*term3
# 		sProb = sProb + termProb
# 		if termProb < termTh:
# 			# print ("sProb", round(term1,10), round(term2,10), round(term3,10))
# 			print ("sProb", round(sProb,10))
# 			return sProb
# 		k=k+1	
