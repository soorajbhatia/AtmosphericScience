stations="72597 72493 72393 72293 74004 72274 72376 72388 72489 72582 72681 72786 72776 72572 72476 72672 72768 72469 72365 72364 72265 72363 72451 72562 72662 72764 72659 72558 72456 72357 72249 72240 72248 72340 72440 72649 72747 72645 74455 74560 72235 72233 72634 72632 72426 72327 72230 72215 72214 72208 72305 72317 72318 72520 72403 72402 72528 72518 72712 72501 72797 72694 72206" 
#didn't cat correctly
#72646 72494 72389 no precip data for these

for station in $stations
do
	function runLoop {
	i=1
	for i in {1..12054}
	do
  	  t=$i
  	  t1=`echo "$i - 0.5" | bc -l`
  	  t2=$i
  	  foo=$(printf "%010d" $i)
  	  #cat $prof |\
  	  cat iisf${station}.cdf |\
  	  cdfrdim time $t1 $t2 |\
  	  cdfextr -rs time |\
  	  cdfmath "$t time =" > TMPav/tmp"${foo}".cdf
	done
	}
	runLoop

	cdfcatf TMPav/* |\
	cdfcat time 0 30000 25000 > dailyavg${station}.cdf
	echo "Finished $station concatenation."
	cd TMPav
	rm *
	cd ..
done
