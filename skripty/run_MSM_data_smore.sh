
exec 2> output_MSM_dataSMX.txt
exec 1>&2


printf "MERENI VYPOCTU MSM smore\n"


printf "\nSR(n,2,2,4) - 16bit klic:\n"

printf "==========================================\nSR(1,2,2,4)\n"
for i in 8 12 16 32 48 64 96 128 256 384 512 #1024 #2048 
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_1224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_1224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done



printf "==========================================\nSR(2,2,2,4)\n"
f=0
for i in 8 12 16 32 48 64 96 128 #256 384 512 #1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 2 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_2224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 2 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_2224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


printf "==========================================\nSR(3,2,2,4)\n"
f=1
for i in 8 12 16 32 48 64 96 #128 #256 512 #1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 3 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_3224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 3 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_3224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


###dodedlat znovu od 4 s1
printf "==========================================\nSR(3,2,2,4)\n"
f=1
for i in 8 12 16 32 48 64 96 #128 #256 512 #1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 3 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_3224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 3 -r 2 -c 2 -e 4 --num $i --fload --fname "./textdata/data_3224_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done

sleep 10
pkill -u berusjan magma.exe



###############
###############
###############


printf "\nSR(n,4,2,4) - 32bit klic:\n"

printf "==========================================\nSR(1,4,2,4)\n"
f=0
for i in 8 12 16 32 48 64 96 128 256 384 512 #1024 #2048 
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 4 -c 2 -e 4 --num $i --fload --fname "./textdata/data_1424_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 4 -c 2 -e 4 --num $i --fload --fname "./textdata/data_1424_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


##vyzkouset dry
printf "==========================================\nSR(2,4,2,4)\n"
f=0
#for i in 4 8 12 16 32 48 64 96 128 #256 #512 1024 #2048 
for i in 96 64 48 32 16 12 8
do
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "./textdata/data_2424_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fload --fname "./textdata/data_2424_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


sleep 10
pkill -u berusjan magma.exe



##################

printf "\nSR(1,2,4,4) - 32bit klic:\n"

printf "==========================================\nSR(1,2,4,4)\n"
f=0
for i in 8 12 16 32 48 64 96 128 256 384 #512 1024 #2048 
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 4 -e 4 --num $i --fload --fname "./textdata/data_1244_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 4 -e 4 --num $i --fload --fname "./textdata/data_1244_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


printf "==========================================\nSR(2,2,4,4)\n"
f=0
#for i in 4 8 12 16 32 48 64 96 128 #256 #512 1024 #2048 
for i in 96 64 48 32 16 12 8 128
do
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 2 -r 2 -c 4 -e 4 --num $i --fload --fname "./textdata/data_2244_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 2 -r 2 -c 4 -e 4 --num $i --fload --fname "./textdata/data_2244_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


sleep 10
pkill -u berusjan magma.exe



#################
#################

printf "\nSR(1,4,4,4) - 64bit klic:\n"

printf "==========================================\nSR(1,4,4,4)\n"
f=0
for i in 8 12 16 32 48 64 96 128 256 #384 #512 1024 #2048 
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 4 -c 4 -e 4 --num $i --fload --fname "./textdata/data_1444_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 4 -c 4 -e 4 --num $i --fload --fname "./textdata/data_1444_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done

#################
#################

printf "\nSR(1,2,2,8) - 32bit klic:\n"

printf "==========================================\nSR(1,2,2,8)\n"
f=0
for i in 8 12 16 32 48 64 96 128 #256 384 512 #1024 #2048 
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 2 -e 8 --num $i --fload --fname "./textdata/data_1228_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 2 -e 8 --num $i --fload --fname "./textdata/data_1228_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done

sleep 10
pkill -u berusjan magma.exe




#################
#################

printf "\nSR(1,4,2,8) - 64bit klic:\n"

printf "==========================================\nSR(1,4,2,8)\n"
f=0
for i in 16 32 48 64 96 128 #256 384 512 #1024 #2048 
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 4 -c 2 -e 8 --num $i --fload --fname "./textdata/data_1428_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 4 -c 2 -e 8 --num $i --fload --fname "./textdata/data_1428_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


##################

printf "\nSR(1,2,4,8) - 64bit klic:\n"
printf "==========================================\nSR(1,2,4,8)\n"
f=0
for i in 16 32 48 64 96 128 #256 384 #512 #1024 #2048 
do
	f=0
	printf "=======================\n --num $i\n"
	for j in {10..19}
	do
		if [[ $f -eq 2 ]] ##vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##2.pokus kdyby nahodou
		then
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 4 -e 8 --num $i --fload --fname "./textdata/data_1248_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j 2.pokus"
			fi
		else ##f=0 - start - data 1. pokus
			printf "===\n --num $i, pok $j --ml --MSM --sep\n"
			timeout 6h python3 experiments.py -n 1 -r 2 -c 4 -e 8 --num $i --fload --fname "./textdata/data_1248_${i}_${j}.txt" --ml --mlmeth "MSM" --sep
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j 1.pokus"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##2. pokus dlouhy - konec vseho
	then
		echo "timeout for2"
		break
	fi
done



##################
##################
##################


