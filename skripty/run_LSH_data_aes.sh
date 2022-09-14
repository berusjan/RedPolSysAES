
exec 2> output_LSH_dataAESa.txt
exec 1>&2

printf "MERENI VYPOCTU LSH3\n"

printf "AES\n"

printf "\nSR(n,4,4,8) - 128bit klic:\n"

##neni 2. pokus - delsi limit
##zatim timeout 48h

printf "==========================================\nSR(1,4,4,8)\n"
f=0
#for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 #1024 #2048 
for i in 96 64 48 32 16 8
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..15}
	do
		if [[ $f -eq 3 ]] ##vyskocit ze vseho
		then
			f=4
			break
		elif [[ $f -eq 2 ]] ##LSH nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 3h python3 experiments.py -n 1 -r 4 -c 4 -e 8 --num $i --fstore --fname "./textdata/data_1448_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=3
				echo "timeout pri --num $i, pok $j data"
			fi		
		elif [[ $f -eq 1 ]] ##f=1 - druhy pokus - data i LSH
		then
			printf "===\n --num $i, pok $j --ml --LSH --sep\n"
			timeout 3h python3 experiments.py -n 1 -r 4 -c 4 -e 8 --num $i --fstore --fname "./textdata/data_1448_${i}_${j}.txt" --ml --mlmeth "LSH" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j LSH"
			fi
		else ##f=0 - start - data i LSH
			printf "===\n --num $i, pok $j --ml --LSH --sep\n"
			timeout 3h python3 experiments.py -n 1 -r 4 -c 4 -e 8 --num $i --fstore --fname "./textdata/data_1448_${i}_${j}.txt" --ml --mlmeth "LSH" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j LSH"
			fi			
		fi		
	done
done



