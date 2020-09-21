#stations="72597 72493 72393 72293 74004 72274 72376 72388 72489 72582 72681 72786 72776 72572 72476 72672 72768 72469 72365 72364 72265 72363 72451 72562 72662 72764 72659 72558 72456 72357 72249 72240 72248 72340 72440 72649 72747 72645 74455 74560 72235 72233 72634 72632 72426 72327 72230 72215 72214 72208 72305 72317 72318 72520 72403 72402 72528 72518 72712 72501 72797 72694 72206"



stations="72376"

for station in $stations
do

#cdfmerge final${station}.cdf '' MASKseasons.cdf '' |\
#cdfmath "pcp MASKsummer * rainSummer =" |\
#python3 qplot time,rainSummer,k.,p timerainSummer${station} jpg

#cdfmerge final74560.cdf '' MASKseasons.cdf '' |\
#cdfmath "pcp MASKsummer * rainSummer =" |\
#python3 qplot rainSummer,p &

#cdfmerge f${station}.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim sf 0 1 | python3 qplot sf,rainSummer,k.,p  sfrainSummer${station} jpg

#cdfmerge f${station}.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim sf 0 1 | python3 qplot ii,sf,k.,p  iisf${station} jpg

#cdfmerge final${station}.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim sf 0 1 | cdfvlim rainSummer 0.1 300 | cdfmath "rainSummer 0 * 1 + maskRain =" | cdfmath "sf maskRain * sfMasked =" | python3 qplot ii,sf,k.,p/ii,sfMasked,r.,p  #iisf0.1rainSummer5.20${station} jpg

cdfmerge f72597.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim rainSummer 0.1 20 | cdfvlim sf 0 1 | python3 qplot sf,rainSummer,k.,p #sf0.1rain5.20Summer${station} jpg



done
