
#this script creates cdf files with a time variable. It it currently formatted to work for data beginning with the year 1980
 
#USAGE: ./timestamper.sh {filelistname.txt} 

#this is of course just an example for the case of one station, the 74560. I may forget to update these comments when we move on to doing all of the stations. 
#utc time in seconds of 00Z Jan 1st, 1985 =
#in order to ensure that rounding errors with the computer because of large numbers do not screw up our analysis, we measured the date and time of our soundings from this start date. We call this "rdate" for relative date. utc is UNIX or POSIX time. x is just the date in the specified format. each line of the text file you specify the script to read through is defined as the variable t, and the year, month, day, and hour of this line is defined as varibles with those names, respectively. I know the script will work for ASCII format text files. I do not know if it works for any other formats. 

filename="$1"
while read t
do
#here each line is defined as the varible "name". Our file names are listed one per line. This allows us to use ${name} in place of the filename anywhere we need it in the script. This script will go down the list of the filenames in the specified text file and 
 name="$t"

#date variables are defined here. the first number specifies which column to start from, the second number specifies how many spaces or columns to go forward. it reads those columns and assigns the number in those columns as that variable. if it is not obvious, this expects the datestamps in the filenames to be in the format YYYYMMDD.HH.******* where the stars represent anything. In our case it is the station number and possible a file extension.
      year=${t:0:4}
      month=${t:4:2}
      day=${t:6:2}
      hour=${t:9:2}
x=$(date -u --date="$year-$month-$day $hour:00:00 UTC")
utc=$(date --date="$x" +%s)
rdate="$((${utc} - 315532800))"
fdate=`echo "${rdate} / 86400" | bc -l`
#touch ${name}
cat ${name} | cdfmath "${utc} UTCtime =" | cdfmath "${rdate} rdate =" | cdfmath "${fdate} time =" > ../allcdfTimestamped/${name}
#echo $fdate
#echo $x
#echo $rdate
#rm ${name}
done < "$filename"

