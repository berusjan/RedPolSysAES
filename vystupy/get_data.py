#!/usr/bin/env python3

import statistics as st

##nutno rucne vyodit cele pokusy ktere nedobehly - timeout a err
##nutno ve vysledku rucne prendat radek SR o jeden pokus niz nad num2

##pro smore
##nutno rucne vyfiltrovat zda je s2-psets0/s4-psets1/s8-psets2
##Ctrl+H - psets0/1/2 - za NIC - pak vratit zpet a dat dasli
##==\npsets0.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n



FILE = "output_LSH_dataAESaSM8.txt"

count=0
len_polys=[]
ps_key_vars=[]
ps_reduce_ml=[]
ps_all=[]
magma_ml=[]
keys=[]
mem=[]
key_all=[]
ps_all=[]
time_all=[]
len_polys_mean=0
ps_key_vars_mean=0
ps_reduce_ml_mean=0
ps_all_mean=0
magma_ml_mean=0
keys_mean=0
mem_mean=0
key_all_mean=0
time_all_mean=0
len_polys_stdev=0
ps_key_vars_stdev=0
ps_reduce_ml_stdev=0
ps_all_stdev=0
magma_ml_stdev=0
keys_stdev=0
mem_stdev=0
key_all_stdev=0
time_all_stdev=0


print("ps_count monom_count_mean monom_count_stdev make_ps_mean make_ps_stdev reduce_ps_mean reduce_ps_stdev prepare_ps_mean prepare_ps_stdev make_gb_mean make_gb_stdev make_variety_mean make_variety_stdev calculate_keys_mean calculate_keys_stdev time_all_mean time_all_stdev memory_mean memory_stedv")

#with open(FILE, 'r') as f:
with open(FILE, encoding="utf8", errors='ignore') as f:
	line=f.readline()
	while line:
		#print(line[0:6])
		if line[0:2] == "SR":
			print(line, end="")
		elif line[0:7] == " --num ":
			if "," in line:
				count+=1
			else:
				if count>0:
					len_polys_mean=round(st.mean(len_polys), 2)
					ps_key_vars_mean=round(st.mean(ps_key_vars), 2)
					ps_reduce_ml_mean=round(st.mean(ps_reduce_ml), 2)
					magma_ml_mean=round(st.mean(magma_ml), 2)
					if len(keys)<2:
						keys_mean=0
						mem_mean=0
						key_all_mean=0
					else:
						keys_mean=round(st.mean(keys), 2)
						mem_mean=round(st.mean(mem), 2)
						key_all_mean=round(st.mean(key_all), 2)
					ps_all_mean=round(st.mean(ps_all), 2)
					time_all_mean=round(st.mean(time_all), 2)
					len_polys_stdev = round(st.stdev(len_polys), 2)
					ps_key_vars_stdev = round(st.stdev(ps_key_vars), 2)
					#ps_reduce_ml_stdev = round(st.stdev(ps_reduce_ml), 2)
					#magma_ml_stdev=round(st.stdev(magma_ml), 2)
					if len(keys)<2:
						keys_stdev=0
						mem_stdev=0
						key_all_stdev=0
					else:
						keys_stdev=round(st.stdev(keys), 2)
						mem_stdev=round(st.stdev(mem), 2)
						key_all_stdev=round(st.stdev(key_all), 2)
					ps_all_stdev=round(st.stdev(ps_all), 2)
					time_all_stdev=round(st.stdev(time_all), 2)
				print( len_polys_mean,len_polys_stdev,
				ps_key_vars_mean,ps_key_vars_stdev,
				ps_reduce_ml_mean,ps_reduce_ml_stdev,
				ps_all_mean,ps_all_stdev,
				magma_ml_mean,magma_ml_stdev,
				keys_mean,keys_stdev,
				key_all_mean,key_all_stdev, 
				time_all_mean,time_all_stdev,
				mem_mean,mem_stdev)
				count=0
				len_polys=[]
				ps_key_vars=[]
				ps_reduce_ml=[]
				magma_ml=[]
				keys=[]
				mem=[]
				key_all=[]
				ps_all=[]
				time_all=[]
				#print("..........")		
				print(line[7:].rstrip("\n"), end=" ")
		elif line[0:22] == 'Time of "ps_key_vars":':
			#print("ps_key_vars")
			h=int(line[23])
			m=int(line[25:27])
			s=int(line[28:30])
			t=s+(60*m)+(60*60*h)
			ps_key_vars.append(t)
			ps_all.append(t)
			time_all.append(t)
			key_all.append(0)
		elif line[0:23] == 'Time of "ps_reduce_ml":':
			#print("ps_reduce_ml")
#			##predelano na dvouciferne h pro aes
#			h=int(line[24:26])
#			m=int(line[27:29])
#			s=int(line[30:32])
			##jednociferne h pro kratsi sifry
			h=int(line[24])
			m=int(line[26:28])
			s=int(line[29:31])
			t=s+(60*m)+(60*60*h)
			#t=t/3 ##pro PAM smore
			ps_reduce_ml.append(t)
			ps_all[-1]+=t
			time_all[-1]+=t
		elif line[0:19] == 'Time of "magma_ml":':
			#print("magma_ml")
#			##predelano na dvouciferne h pro aes
#			h=int(line[20:22])
#			m=int(line[23:25])
#			s=int(line[26:28])
			##jednociferne h pro kratsi sifry
			h=int(line[20])
			m=int(line[22:24])
			s=int(line[25:27])
			t=s+(60*m)+(60*60*h)
			magma_ml.append(t)
			time_all[-1]+=t
			key_all[-1]+=t
		elif line[0:15] == 'Time of "keys":':
			#print("keys")
			h=int(line[16])
			m=int(line[18:20])
			s=int(line[21:23])
			t=s+(60*m)+(60*60*h)
			keys.append(t)
			time_all[-1]+=t
			key_all[-1]+=t
		elif line[0:20] == 'Avg length of polys:':
			#print("len_polys")
			polys=line[21:]
			len_polys.append(int(polys.rstrip("\n")))
		elif line[0:12] == 'Used memory:':
			#print("mem")
			memory=line[13:-5]
			unit=line[-4:-2]
			if unit == "GB":
				#print(memory)
				flag=0
				c=0
				memorystr=""
				for i in memory:
					if i == ".":
						flag=1
					else:
						memorystr+=i
					if flag:
						c+=1
				while c<=3:
					memorystr+="0"
					c+=1
				#print(memorystr)	
				mem.append(int(memorystr))				
			else:
				mem.append(int(memory.rstrip("\n")))
			
		
		
		line=f.readline()
	len_polys_mean=round(st.mean(len_polys), 2)
	ps_key_vars_mean=round(st.mean(ps_key_vars), 2)
	ps_reduce_ml_mean=round(st.mean(ps_reduce_ml), 2)
	magma_ml_mean=round(st.mean(magma_ml), 2)
	if len(keys)<2:
		keys_mean=0
		mem_mean=0
		key_all_mean=0
	else:
		keys_mean=round(st.mean(keys), 2)
		mem_mean=round(st.mean(mem), 2)
		key_all_mean=round(st.mean(key_all), 2)
	ps_all_mean=round(st.mean(ps_all), 2)
	time_all_mean=round(st.mean(time_all), 2)
	len_polys_stdev=round(st.stdev(len_polys), 2)
	ps_key_vars_stdev=round(st.stdev(ps_key_vars), 2)
	#ps_reduce_ml_stdev=round(st.stdev(ps_reduce_ml), 2)
	#magma_ml_stdev=round(st.stdev(magma_ml), 2)
	if len(keys)<2:
		keys_stdev=0
		mem_stdev=0
		key_all_stdev=0
	else:
		keys_stdev=round(st.stdev(keys), 2)
		mem_stdev=round(st.stdev(mem), 2)
		key_all_stdev=round(st.stdev(key_all), 2)
	ps_all_stdev=round(st.stdev(ps_all), 2)
	time_all_stdev=round(st.stdev(time_all), 2)
	print( len_polys_mean,len_polys_stdev,
				ps_key_vars_mean,ps_key_vars_stdev,
				ps_reduce_ml_mean,ps_reduce_ml_stdev,
				ps_all_mean,ps_all_stdev,
				magma_ml_mean,magma_ml_stdev,
				keys_mean,keys_stdev,
				key_all_mean,key_all_stdev, 
				time_all_mean,time_all_stdev,
				mem_mean,mem_stdev)




