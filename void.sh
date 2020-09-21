filename="$1"
while read t
do
#here each line is defined as the varible "name". Our file names are listed one per line. This allows us to use ${name} in place of the filename anywhere we need it in the script. This script will go down the list of the filenames in the specified text file and 
 name="$t"

#date variables are defined here. the first number specifies which column to start from, the second number specifies how many spaces or columns to go forward. it reads those columns and assigns the number in those columns as that variable. if it is not obvious, this expects the datestamps in the filenames to be in the format YYYYMMDD.HH.******* where the stars represent anything. In our case it is the station number and possible a file extension.
#      year=${t:0:4}
#      month=${t:4:2}
#      day=${t:6:2}
#      hour=${t:9:2}
#x=$(date -u --date="$year-$month-$day $hour:00:00 UTC")
#utc=$(date --date="$x" +%s)
#rdate="$((${utc} - 157766400))"
#fdate="$((${rdate} / 86400))"

cat 20161231.12.72403.cdf | cdfvlim p -9999 -9998 | cdfvlim index -9999 -9998 | cdfvlim t -9999 -9998 | cdfvlim dp -9999 -9998 | cdfvlim rh -9999 -9998 | cdfvlim mr -9999 -9998 | cdfvlim dir -9999 -9998 | cdfvlim knot -9999 -9998 | cdfvlim thta -9999 -9998 | cdfvlim thte -9999 -9998 | cdfvlim thtv -9999 -9998  > debug2/${name}.cdf

#rm tocat/${name}.cdf

#mv cont/${name}.cdf tocat

#echo ${x}

done < "$filename"


