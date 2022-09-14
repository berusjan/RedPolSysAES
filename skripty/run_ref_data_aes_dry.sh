
exec 2> output_ref_data_dryAESa.txt
exec 1>&2

printf "MERENI VYPOCTU REF AES\n"

printf "AES\n"

printf "\nSR(n,4,4,8) - 128bit klic:\n"



printf "==========================================\nSR(1,4,4,8)\n"
f=0
#for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 #1024 #2048 
for i in 8 16 32 48 64 96
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..14}
	do
		printf "===\n --num $i, pok $j --dry\n"
		timeout 2h python3 experiments.py -n 1 -r 4 -c 4 -e 8 --num $i --fload --fname "../in/data_1448_${i}_${j}.txt" --dry
	done
done



