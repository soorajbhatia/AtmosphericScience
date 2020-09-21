
#stations below 200m
stations="72493 72206 72240 72233 72305 72402 72208 72501 72214 72694 72797 72248 72235 72403 72518 72393 72293 72249 72340 74560 72230 72327 72712"

#74004 had some error. It had 15340 time slices instead of the 15341 all of the others had. For efficiency's sake, I chose to throw this station data out instead of trying to figure out what happenend.

#all stations
#stations="72597 72493 72393 72293 74004 72274 72376 72388 72489 72582 72681 72786 72776 72572 72476 72672 72768 72469 72365 72364 72265 72363 72451 72562 72662 72764 72659 72558 72456 72357 72249 72240 72248 72340 72440 72649 72747 72645 74455 74560 72235 72233 72634 72632 72426 72327 72230 72215 72214 72208 72305 72317 72318 72520 72403 72402 72528 72518 72494 72389 72712 72501"

#stations="72248"
hours="00 12"

for station in $stations
do 

for hour in $hours
do
echo "now doing ${station}.${hour}.cdf"

cat 0012catted/final${station}.${hour}.cdf |\
cdfwindow time 1826 13879 |\
cdfmath "time 1826 - time2 =" |\
cdfinvindex time time2 |\
cdfmath "time2 1 + time =" |\
cdfinvindex time2 time |\
cdfextr -s time z > newIIrain2/${station}.${hour}.cdf

cdfmerge newIIrain2/${station}.${hour}.cdf '' precip/rain${station}.cdf '' > newIIrain2/pcp${station}.${hour}.cdf
rm newIIrain2/${station}.${hour}.cdf

#uniget final72230.00.nc | cdfextr -s z time | cdfderiv dthtadz thta z | cdfderiv dmrdz mr z | cdfderiv drhdz rh z | cdfextr -r sf. sf.. | uniput -r test72230.00.nc

done

done

