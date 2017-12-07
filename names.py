import subprocess
import os


def buscar(line):
	old_name = ' '.join(line.split()[8:]) 
	first = False
	res = ''
	for caracter in old_name:
		if caracter.isdigit() and not first:
			res+=caracter
			first = True

		elif first and caracter == "x": res+=caracter
		elif caracter.isdigit(): res+=caracter
		elif first and not caracter.isdigit(): break

	assert len(res) == 4 or len(res) == 3, "error al identificar temporada y capitulo"
	if len(res) == 4: return res
	if len(res) == 3: return "{}x{}".format(res[0], res[1:]) 

def formato(line):
	old_name = ' '.join(line.split()[8:])
	return "."+old_name.split('.')[-1]
			

process = subprocess.Popen('ls -l', stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=None, shell=True)
output = process.communicate()

name = input("Nombre de la serie: ")
name = name.replace(" ", "\ ")

dic = {}
dir_to_move = []
for line in output[0].decode().split('\n'):
	if(len(line) > 0 and line[0] == '-'):  #Es archivo
		copy_name = name
		if(' '.join(line.split()[8:]) == "nombres.py"): continue
		tempycap = buscar(line)
		copy_name += "\ "+tempycap
		copy_name += formato(line)
		dic[' '.join(line.split()[8:])] = copy_name

	elif len(line)>0 and line[0] == 'd':  dir_to_move.append(' '.join(line.split()[8:]))

for i in set(dir_to_move):
	directory = i.replace(" ", "\ ")
	directory = directory.replace("[", "\[")
	directory = directory.replace("]", "\]")
	process = subprocess.Popen('ls -l {}'.format(directory), stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=None, shell=True)
	output = process.communicate()

	for line in output[0].decode().split('\n'):
		if(len(line) > 0 and line[0] == '-'):  #Es archivo
			copy_name = directory
			copy_name += '/'
			copy_name += name
			if(' '.join(line.split()[8:]) == "nombres.py"): continue
			tempycap = buscar(line)
			copy_name += "\ "+tempycap
			copy_name += formato(line)
			dic[' '.join(line.split()[8:])] = copy_name

res = []
for i in dic.keys():
	res.append("{} <-- {}".format(dic[i], i))

for i in sorted(res): print(i)

ok = input("continuar[y/n]")

if(ok.lower() == 'y'):
	for i in dic.keys():
		os.system('mv {} {}'.format(i, dic[i]))
else: print("operacion cancelada")
