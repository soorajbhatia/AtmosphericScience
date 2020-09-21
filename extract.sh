
#use: voidfilesToCandis.sh {name of file being read}, can be used to cycle through any file list
filename="$1"
while read line
do 
	name="$line"
#put what you need done here
	cat ${name} | cdfextr sf ii time >> ../trial2/${name}
done < "$filename"
