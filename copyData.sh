var=61
while [ $var -le 75 ]; do
	echo $var
	mkdir d$var
	mv NumberOfTransactionsInBlock_$var* d$var
	mv gasLimitGasUsed_$var* d$var
	var=$((var+1))
done