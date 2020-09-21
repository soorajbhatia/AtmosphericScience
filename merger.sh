stations="72597 72393 72293 72274 72376 72388 72489 72582 72681 72786 72776 72572 72476 72672 72768 72469 72365 72364 72265 72363 72451 72562 72662 72764 72659 72558 72456 72357 72249 72248 72340 72440 72649 72747 74455 74560 72233 72520" 
#72797 72694 72206 look into these files
#72493 reserved for the first file that is used to cat all the other files into, this one is not in the station list above.
#72240 72645 72235 72634 72632 72426 72327 72230 72215 72214 72208 72305 72317 72318 72403 72402 72528 72518 72501 #74004 72712 <last two are just to get it to work (to get rid of the damn bad buffer/not enough buffer space error

cp f72493.cdf tmp.cdf

i=1
for station in $stations
do
	cat f${station}.cdf > tmp1.cdf
#cdfextr sf$i #cdfmath "sf sf$i ="
	cdfmerge tmp.cdf '' tmp1.cdf "$i" | cdfmath "time time$i =" | cdfextr -s time > tmp0.cdf

	mv tmp0.cdf tmp.cdf

	i=`echo "$i + 1" | bc`
	#echo $i

	
done
