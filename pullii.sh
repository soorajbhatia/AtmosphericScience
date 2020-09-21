filename="$1"
while read t
do
name="$t"
echo ${name}
cdflook < ${name} > tmp.asc
grep 'ii = ' tmp.asc > tmp1.asc
rm tmp.asc
sed 's/ii = //g' tmp1.asc >> ../iilist75to16.asc
rm tmp1.asc
done < "$filename"
