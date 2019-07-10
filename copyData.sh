var=0
while [ $var -le 8 ]; do
	mkdir d$var
	mv NumberOfTransactionsInBlock_$var* d$var
	mv gasLimitGasUsed_$var* d$var
	echo d$var
	var=$((var+1))
done 