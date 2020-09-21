list="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38"

#plottingList=""
#sfMaskedList=""

#echo -n "cdfmerge tmp.cdf '' MASKseasons.cdf '' | cdfmath 'pcp MASKsummer * rainSummer =' | cdfvlim sf 0 1 | cdfvlim rainSummer 0.1 300 | cdfmath 'rainSummer 0 * 1 + maskRain =' | cdfmath 'sf maskRain * sfMasked =' "

for station in $list
do
 # plottingList="$plottingList/ii${station},sf${station},k.,p/ii${statin},sfMasked${station},r.,p"
  echo -n "| cdfmath 'time time${station} ='"
 # echo -n "|cdfmath 'pcp${station} MASKsummer * rainSummer${station} =' | cdfvlim sf${station} 0 1 | cdfvlim rainSummer${station} 0.1 300 | cdfmath 'rainSummer${station} 0 * 1 + maskRain${station} * sfMasked${station} ='"
done


#echo "| qplot ii,sf,k.,p/sf1,ii1,k.,p/sf2,ii2,k.,p/sf3,ii3,k.,p/sf4,ii4,k.,p/sf5,ii5,k.,p/sf6,ii6,k.,p/sf7,ii7,k.,p/sf8,ii8,k.,p/sf9,ii9,k.,p/sf10,ii10,k.,p/sf11,ii11,k.,p/sf12,ii12,k.,p/sf13,ii13,k.,p/sf14,ii14,k.,p/sf15,ii15,k.,p/sf16,ii16,k.,p/sf17,ii17,k.,p/sf18,ii18,k.,p/sf19,ii19,k.,p/sf20,ii20,k.,p/sf21,ii21,k.,p/sf22,ii22,k.,p/sf23,ii23,k.,p/sf24,ii24,k.,p/sf25,ii25,k.,p/sf26,ii26,k.,p/sf27,ii27,k.,p/sf28,ii28,k.,p/sf29,ii29,k.,p/sf30,ii30,k.,p/sf31,ii31,k.,p/sf32,ii32,k.,p/sf33,ii33,k.,p/sf34,ii34,k.,p/sf35,ii35,k.,p/sf36,ii36,k.,p/sf37,ii37,k.,p/sf38,ii38,k.,p/-200,250,50,0,1,0.2,ax  iisfallMasked png"

#cdfmerge tmp.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim sf 0 1 | cdfvlim rainSummer 0.1 300 | cdfmath "rainSummer 0 * 1 + maskRain =" | cdfmath "sf maskRain * sfMasked =" | qplot ii,sf,k.,p/sf1,ii1,k.,p/sf2,ii2,k.,p/sf3,ii3,k.,p/sf4,ii4,k.,p/sf5,ii5,k.,p/sf6,ii6,k.,p/sf7,ii7,k.,p/sf8,ii8,k.,p/sf9,ii9,k.,p/sf10,ii10,k.,p/sf11,ii11,k.,p/sf12,ii12,k.,p/sf13,ii13,k.,p/sf14,ii14,k.,p/sf15,ii15,k.,p/sf16,ii16,k.,p/sf17,ii17,k.,p/sf18,ii18,k.,p/sf19,ii19,k.,p/sf20,ii20,k.,p/sf21,ii21,k.,p/sf22,ii22,k.,p/sf23,ii23,k.,p/sf24,ii24,k.,p/sf25,ii25,k.,p/sf26,ii26,k.,p/sf27,ii27,k.,p/sf28,ii28,k.,p/sf29,ii29,k.,p/sf30,ii30,k.,p/sf31,ii31,k.,p/sf32,ii32,k.,p/sf33,ii33,k.,p/sf34,ii34,k.,p/sf35,ii35,k.,p/sf36,ii36,k.,p/sf37,ii37,k.,p/sf38,ii38,k.,p/-200,250,50,0,1,0.2,ax  iisfallMasked png

#echo ${sfMaskedList}${plottingList}
