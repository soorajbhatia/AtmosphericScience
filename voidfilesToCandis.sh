
#use: voidfilesToCandis.sh {name of file being read}, can be used to cycle through any file list
filename="$1"
while read line
do 
	name="$line"
#put what you need done here
	cat baddata | cdftable p z t dp rh mr dir knot thta thte thtv | cdfcat index 0 1000 5000 | cdfmath "-999 ii =" | cdfmath "-999 sf =" | cdfinvindex index z > tocat/${name}
done < "$filename"
