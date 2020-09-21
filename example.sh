
cat rain74560.cdf | python3 qplot time,pcp,p &

cdfmerge final74560.cdf '' MASKseasons.cdf '' |\
cdfmath "pcp MASKsummer * rainSummer =" |\
python3 qplot time,rainSummer,p &

#cdfmerge final74560.cdf '' MASKseasons.cdf '' |\
#cdfmath "pcp MASKsummer * rainSummer =" |\
#python3 qplot rainSummer,p &

cdfmerge final74560.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim sf 0 1 | python3 qplot sf,rainSummer,k.,p &

cdfmerge final74560.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim sf 0 1 | python3 qplot ii,sf,k.,p &

cdfmerge final74560.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | cdfvlim rainSummer 5 20 | cdfvlim sf 0 1 | python3 qplot sf,rainSummer,k.,p &



#cdfmerge final74560.cdf '' MASKseasons.cdf '' | cdfmath "pcp MASKsummer * rainSummer =" | python3 qplot rainSummer,sf,p &
