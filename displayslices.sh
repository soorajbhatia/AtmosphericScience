stations="72797 72694 72597 72493 72393 72293 74004 72274 72376 72388 72489 72582 72681 72786 72776 72572 72476 72672 72768 72469 72365 72364 72265 72363 72451 72562 72662 72764 72659 72558 72456 72646 72357 72249 72240 72248 72340 72440 72649 72747 72645 74455 74560 72235 72233 72634 72632 72426 72327 72230 72215 72214 72206 72208 72305 72317 72318 72520 72403 72402 72528 72518 72494 72389 72712 72501"

for station in $stations
do

cdflook < ${station}.cdf > tmp.asc
echo $station >> tmp1.asc
grep 'UTCtime 1 0 l 1' tmp.asc >> tmp1.asc
rm tmp.asc
#sed 'UTCtime 1 0 l 1 time' tmp1.asc >> slicelist.asc
#rm tmp1.asc

done