
filename="$1"
while read t
do
name="$t"
echo ${name}
cdflook < ${name} > tmp.asc
grep 'sf = ' tmp.asc > tmp1.asc
rm tmp.asc
sed 's/sf = //g' tmp1.asc >> ../sflist75to16.asc
rm tmp1.asc
done < "$filename"
