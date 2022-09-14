
exec 2> output_ref_gen_dataX.txt
exec 1>&2


#parser.add_argument('-n', type=int, default=1, choices=range(1, 11))
#parser.add_argument('-r', type=int, default=2, choices=[[1, 2, 4]])
#parser.add_argument('-c', type=int, default=2, choices=[[1, 2, 4]])
#parser.add_argument('-e', type=int, default=4, choices=[[4, 8]])
#parser.add_argument('--num', type=int, default=1)
#parser.add_argument('--sep', default=False, action='store_true')
#parser.add_argument('--ml', default=False, action='store_true')
#parser.add_argument('--mlmeth', type=str, default='PAM', choices=[['PAM', 'MSM', 'LSH']])
#parser.add_argument('--fstore', default=False, action='store_true')
#parser.add_argument('--fload', default=False, action='store_true')
#parser.add_argument('--fname', type=str, default='../out/data.txt')

#timeout 3h python3 experiments.py -n 1 -r 2 -c 2 -e 4 --num 1



printf "GENEROVANI DAT PRO VYPOCET POLYNOMU \n+referenci reseni\n"


printf "\nSR(n,2,2,4) - 16bit klic:\n"

printf "==========================================\nSR(1,2,2,4)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_1224_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_1224_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done



printf "==========================================\nSR(2,2,2,4)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 #1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 2 -r 2 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_2224_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 2 -r 2 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_2224_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done



printf "==========================================\nSR(3,2,2,4)\n"
f=1
for i in 2 4 8 12 16 32 48 64 96 128 256 512 #1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		else ##ref nedobehlo - jen data
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 3 -r 2 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_3224_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


###############
###############
###############


printf "\nSR(n,4,2,4) - 32bit klic:\n"

printf "==========================================\nSR(1,4,2,4)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_1424_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_1424_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_1424_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


printf "==========================================\nSR(2,4,2,4)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 #512 1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_2424_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref
		then
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_2424_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 2 -r 4 -c 2 -e 4 --num $i --fstore --fname "./textdata/data_2424_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


################

printf "\nSR(1,2,4,4) - 32bit klic:\n"

printf "==========================================\nSR(1,2,4,4)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_1244_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref
		then
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_1244_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_1244_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


printf "==========================================\nSR(2,2,4,4)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 #512 1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 2 -r 2 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_2244_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 2 -r 2 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_2244_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 2 -r 2 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_2244_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done

###############
###############

###dodelat
##--num 256, pok 24 --dry, Cipher: SR(1,4,4,4)
##ValueError: The polynomial system could not be created due to too many 0-inversions.

###num 384 nebudu delat
##--num 384, pok 11,13,17-22,25,27,28 --dry, Cipher: SR(1,4,4,4)
##ValueError: The polynomial system could not be created due to too many 0-inversions.
printf "\nSR(1,4,4,4) - 64bit klic:\n"
printf "==========================================\nSR(1,4,4,4)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 384 #512 1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_1444_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref
		then
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_1444_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 4 -e 4 --num $i --fstore --fname "./textdata/data_1444_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
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
for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 2 -e 8 --num $i --fstore --fname "./textdata/data_1228_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref
		then
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 2 -e 8 --num $i --fstore --fname "./textdata/data_1228_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 2 -e 8 --num $i --fstore --fname "./textdata/data_1228_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


#################
#################

printf "\nSR(1,4,2,8) - 64bit klic:\n"

printf "==========================================\nSR(1,4,2,8)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 #1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 2 -e 8 --num $i --fstore --fname "./textdata/data_1428_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref
		then
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 2 -e 8 --num $i --fstore --fname "./textdata/data_1428_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 4 -c 2 -e 8 --num $i --fstore --fname "./textdata/data_1428_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done


##################

printf "\nSR(1,2,4,8) - 64bit klic:\n"
printf "==========================================\nSR(1,2,4,8)\n"
f=0
for i in 2 4 8 12 16 32 48 64 96 128 256 384 512 #1024 #2048 
do
	printf "=======================\n --num $i\n"
	for j in {10..29}
	do
		if [[ $f -eq 2 ]] ##ani data se nestihla - vyskocit ze vseho
		then
			f=3
			break
		elif [[ $f -eq 1 ]] ##ref nedobehlo - jen data
		then
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 4 -e 8 --num $i --fstore --fname "./textdata/data_1248_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=2
				echo "timeout pri --num $i, pok $j data"
			fi
		elif [[ $i -lt 32 || $i -eq 128 ]] ##ref
		then
			printf "===\n --num $i, pok $j\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 4 -e 8 --num $i --fstore --fname "./textdata/data_1248_${i}_${j}.txt"
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j data"
			fi
		else ##f=0 - start - data i referencni reseni
			printf "===\n --num $i, pok $j --dry\n"
			timeout 4h python3 experiments.py -n 1 -r 2 -c 4 -e 8 --num $i --fstore --fname "./textdata/data_1248_${i}_${j}.txt" --dry
			if [[ $? -eq 124 ]]
			then
				f=1
				echo "timeout pri --num $i, pok $j ref"
			fi
		fi		
	done
	if [[ $f -eq 3 ]] ##data se nestihla - konec vseho
	then
		echo "timeout for2"
		break
	fi
done



##################
##################
##################


