stations="72797 72694 72597 72493 72393 72293 74004 72274 72376 72388 72489 72582 72681 72786 72776 72572 72476 72672 72768 72469 72365 72364 72265 72363 72451 72562 72662 72764 72659 72558 72456 72646 72357 72249 72240 72248 72340 72440 72649 72747 72645 74455 74560 72235 72233 72634 72632 72426 72327 72230 72215 72214 72206 72208 72305 72317 72318 72520 72403 72402 72528 72518 72494 72389 72712 72501"

#stations="72797 72694 72206"

#stations="72365"
#years="1975 1976 1977 1978 1979 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 1990 1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016"

hours="00 12"

for station in $stations
do
	for hour in $hours
	do
		cdfcatf *.${hour}.${station}.cdf | cdfcat time 0 3000000 2500000 > ../0012catted/${station}.${hour}.cdf
        	echo "${hour}Z ${station} complete"
	done
done
