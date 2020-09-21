#use: Wyomingtocdf.sh {name of file being read}, can be used to cycle through any file list
filename="$1"
while read line
do 
	name="$line"
#put what you need done here

##### sat frac using Sooraj's variables
#cat ${name} | cdfinterp z 0 250 81 > ${name}

cat ${name} | cdfvlim t -100 100 | cdfmath "p 100 * 287 t 273 + * / rho =" | cdfentropy -d p t dp ent satmr | cdfmath "mr 1000 / rho * pw =" | cdfmath "satmr 1000 / rho * satpw =" | cdfwindow z 0 15000 | cdfdefint z | cdfmath "pw satpw / sf =" | cdfextr sf > ${name}sf


#### instability index using Sooraj's variables 
cat ${name} | cdfvlim t -100 100 | cdfmath "p 100 * 287 t 273 + * / rho =" | cdfnewent p t mr ent ents | cdfrdim z 1000 3000 > low.cdf
cat ${name} | cdfvlim t -100 100 | cdfmath "p 100 * 287 t 273 + * / rho =" | cdfnewent p t mr ent ents | cdfrdim z 5000 7000 > high.cdf
cdfmerge low.cdf '' high.cdf '' | cdfmath "ents ents. - ii =" > ${name}ii

done < "$filename"

rm low.cdf
rm high.cdf
