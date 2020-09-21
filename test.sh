function runLoop {
	i=1
	for i in {1..15341}
	do
  	  t=$i
  	  t1=`echo "$i - 0.5" | bc -l`
  	  t2=$i
  	  foo=$(printf "%1d" $i)
  	  #cat $prof |\
  	  #cat ${station}.cdf |\
  	  #cdfrdim time $t1 $t2 |\
  	  #cdfextr -rs time |\
  	  #cdfmath "$t time =" > TMPav/tmp"${foo}".cdf
  	  #echo "Finished $i file: $foo out of 15341"
	  #echo $foo
	  echo $t1
	done
	}
	runLoop

