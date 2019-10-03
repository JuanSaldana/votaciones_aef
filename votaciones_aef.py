import csv
import codecs
#from pprint import pprint

#Carga de los votos a grossomodo a través del CSV    
def load_data(infile):
	#csv_reader = Latin1ToUnicodeDictReader(infile)
	csv_reader = csv.DictReader(infile,delimiter = ',')
	votos_raw = []
	for row in csv_reader:
		votos_raw.append(dict(row))
	return votos_raw

#Cargando matrículas
def Normalizar_matriculas(diccionario):
	formas_matricula = ['Mat.','Matricula','Matrícula','matricula','matrícula','mat.','Mat','mat']
	normal_key = 'matricula'
	for linea in diccionario:
		for key in list(linea.keys()):
			if key in formas_matricula:
				linea[normal_key] = linea.pop(key)
	return diccionario

#Toda la lista de matrículas válidas
def valid_mat(students):
	matriculas_validas = []
	for student in students:
		matriculas_validas.append(student['matricula'])
	return matriculas_validas 

#Aquí se eliminan aquellos votos que estén repetidos o no estén en la lista de estudiantes
def validate_votes(votos_raw,students):
	#Primero eliminemos aquellos que no estén en la lista
	#print(votos_raw)
	new_votos_raw = [] 
	for voto in votos_raw:
		#print(voto['matricula'])
		if str(voto['matricula']) in students:
			#print('cool')
			new_votos_raw.append(voto)

	return new_votos_raw

#Extracción de los puestos
def puestos(votos_raw):
	puestos = list(votos_raw[0].keys())
	nopuestos = ['Marca temporal','matricula']
	for nopuesto in nopuestos:
		if nopuesto in puestos: puestos.remove(nopuesto)
	return puestos

#Limpiar los votos, como output: Diccionario puesto:[votos]
def clean_votes(votos_raw,puestos):
	votos = {}
	for puesto in puestos:
		votos.update({puesto:[]})
		for voto in votos_raw:
			votos[puesto].append(voto[puesto])
	return votos

#Conteo de los votos
def contar_votos(votos,puestos):
	for puesto in puestos:
		candidatos = set(votos[puesto])
		for candidato in candidatos:
			votos_a_favor = votos[puesto].count(candidato)
			formatito = f"El candidato {candidato} para el puesto de {puesto}\ntiene {votos_a_favor} votos a favor\n"
			print(formatito)
	return

#Regresa una lista de los ganadores en base al candidato "más votado"
def ganadores(votos,puestos):
	ganadores = []
	for puesto in puestos:
		ganador = most_frequent(votos[puesto])
		ganadores.append({puesto:ganador})
	print(ganadores)
	return ganadores

def most_frequent(List): 
    return max(set(List), key = List.count)


#----FLUJO MATRICULAS------
# 1. Se cargan el archivo de alumnos
# 2. Se normaliza el key de matrículas
# 3. Se limpia la data para solo obtener las matrículas

students_file = codecs.open('INSCRITOS_EN_FISICA_AGO_DIC_2019.csv', mode = 'r',encoding = 'ISO-8859-1', errors = 'ignore')
students = load_data(students_file)
students = Normalizar_matriculas(students)
students = valid_mat(students)


#----FLUJO VOTOS------
# 1. Se cargan los votos
# 2. Se limpian para tener solo aquellos votos que son válidos
# 3. Se obtienen los puestos
# 4. Se limpian los votos y se clasifican por puesto
# 5. Se cuentan los votos
# 6. Se entrega la lista de ganadores
#

votos_file = codecs.open('votaciones_aef.csv', mode = 'r',encoding = 'ISO-8859-1', errors = 'ignore')
votos_raw = load_data(votos_file)
votos_raw = Normalizar_matriculas(votos_raw)
votos_raw = validate_votes(votos_raw,students)
puestos = puestos(votos_raw)
votos = clean_votes(votos_raw,puestos)
contar_votos(votos,puestos)
ganadores = ganadores(votos,puestos)