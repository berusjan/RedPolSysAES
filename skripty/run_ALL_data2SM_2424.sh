
exec 2> output_ALL_data2SM_2424a.txt
exec 1>&2


printf "MERENI VYPOCTU LSH2\n+nacitani dat\n"




printf "\nSR(2,4,2,4) - 32bit klic:\n"
f=0
printf "==========================================\nSR(2,4,2,4)\n"
#for i in 8 12 16 32 48 64 96 128 256 #384 #512 #1024 #2048 
#for i in 128 96 64 48 32 16 #12 8
for i in 32 # 96 64 12 8
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..12}
	do
		sleep 10
		pkill -u berusjan magma.exe	
		if [[ $f -eq 3 ]] ##vyskocit ze vseho
		then
			f=4
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --LSH --sep\n"
			timeout 24h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "../in/data_2424_${i}_${j}.txt" --ml --mlmeth "LSH"  --sep
			if [[ $? -eq 124 ]]
			then
				f=3
				echo "timeout pri --num $i, pok $j 2.pokus"
				sleep 10
				pkill -u berusjan magma.exe
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --LSH --sep\n"
			timeout 24h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "../in/data_2424_${i}_${j}.txt" --ml --mlmeth "LSH"  --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
				sleep 10
				pkill -u berusjan magma.exe
			fi
		fi		
	done
	if [[ $f -eq 4 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done

sleep 10
pkill -u berusjan magma.exe




#################
#################
#################


#printf "MERENI VYPOCTU PAM2\n+nacitani dat\n"




#printf "\nSR(2,4,2,4) - 32bit klic:\n"
#f=0
#printf "==========================================\nSR(2,4,2,4)\n"
##for i in  96 64 48 32 16
#for i in  32 48 64
#do
#	f=0
#	printf "=======================\n --num $i\n"
#	for j in {10..16}
#	do
#		sleep 10
#		pkill -u berusjan magma.exe	
#		if [[ $f -eq 3 ]] ##vyskocit ze vseho
#		then
#			f=4
#			break
#		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
#		then
#			printf "===\n --num $i, pok $j --ml --PAM --sep\n"
#			timeout 24h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "../in/data_2424_${i}_${j}.txt" --ml --mlmeth "PAM"  --sep
#			if [[ $? -eq 124 ]]
#			then
#				f=3
#				echo "timeout pri --num $i, pok $j 2.pokus"
#				sleep 10
#				pkill -u berusjan magma.exe
#			fi
#		else ##f=0 - start - data 1. pokus
#			printf "===\n --num $i, pok $j --ml --PAM --sep\n"
#			timeout 24h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "../in/data_2424_${i}_${j}.txt" --ml --mlmeth "PAM"  --sep
#			if [[ $? -eq 124 ]]
#			then
#				f=1
#				echo "timeout pri --num $i, pok $j 1.pokus"
#				sleep 10
#				pkill -u berusjan magma.exe
#			fi
#		fi		
#	done
#	if [[ $f -eq 4 ]] ##2. pokus dlouhy - konec vseho
#	then
#		echo "timeout for2"
#		break
#	fi
#done

#sleep 10
#pkill -u berusjan magma.exe





##################
##################
##################


#printf "MERENI VYPOCTU MSM2\n+nacitani dat\n"




#printf "\nSR(2,4,2,4) - 32bit klic:\n"
#f=0
#printf "==========================================\nSR(2,4,2,4)\n"
##for i in  96 64 48 32 16
#for i in  32 48 64
#do
#	f=0
#	printf "=======================\n --num $i\n"
#	for j in {10..16}
#	do
#		sleep 10
#		pkill -u berusjan magma.exe	
#		if [[ $f -eq 3 ]] ##vyskocit ze vseho
#		then
#			f=4
#			break
#		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
#		then
#			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
#			timeout 24h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "../in/data_2424_${i}_${j}.txt" --ml --mlmeth "MSM"  --sep
#			if [[ $? -eq 124 ]]
#			then
#				f=3
#				echo "timeout pri --num $i, pok $j 2.pokus"
#				sleep 10
#				pkill -u berusjan magma.exe
#			fi
#		else ##f=0 - start - data 1. pokus
#			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
#			timeout 24h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "../in/data_2424_${i}_${j}.txt" --ml --mlmeth "MSM"  --sep
#			if [[ $? -eq 124 ]]
#			then
#				f=1
#				echo "timeout pri --num $i, pok $j 1.pokus"
#				sleep 10
#				pkill -u berusjan magma.exe
#			fi
#		fi		
#	done
#	if [[ $f -eq 4 ]] ##2. pokus dlouhy - konec vseho
#	then
#		echo "timeout for2"
#		break
#	fi
#done

#sleep 10
#pkill -u berusjan magma.exe


