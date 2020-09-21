
#use: voidfilesToCandis.sh {name of file being read}, can be used to cycle through any file list
filename="$1"
while read line
do 
	name="$line"
#put what you need done here
	cat cattest/197501*72797.cdf | cdfextr -s z | cdflook 
 > cont/${name}
done < "$filename"
