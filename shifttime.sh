files=`ls *.cdf`

for file in $files 
do 
	cat ${file} | cdfmath "time 0.5 - temptime =" | cdfinvindex time temptime | cdfmath "temptime time =" | cdfinvindex temptime time > timeshifted/${file}

done
