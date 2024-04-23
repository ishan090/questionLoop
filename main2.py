"""
This program takes in a table and asks question based on the table

It takes in three fields: (work in progress)
-unique field
-group field
-special field

Anyways, there are certain types that can be mentioned in the data files for this program.
The following are the accepted types: Num for a number, Str for a string

"""

# Imports
import csv
import json
import random


# Setting up some Global variables
modules = {"1":"months.csv", "2":"rutina.csv", "3": "verbs.csv", "4": "colours.csv", "5": "face.csv", "6": "medios_de_transporte.csv", "7": "cosas_cotidianas.csv", "8": "los_lugares_de_trabajo.csv"}
module_names = {"1":"Meses del año en español", "2":"Rutina días", "3": "Verbos Regulares", "4": "Los Colores", "5": "Partes de la cara", "6": "Medios De Transporte", "7": "Cosas Cotidianas", "8": "Los Lugares De Trabajo"}
# var_defs = {"#N": float, "#M"}


def loadConfig(filename):
	with open(filename, 'r') as file:
		config = json.load(file)
	return config

def parse_vars(header=None, variables_raw=None, vars_names=None, refs=None):
	if variables_raw is not None:
		vars_names = variables_raw[header[0]].split(";")
		refs = variables_raw[header[1]].split(";")
	else:
		vars_names = vars_names.split(";")
		refs = refs.split(";")
	assert len(vars_names) == len(refs)
	variables = {vars_names[i]:refs[i] for i in range(len(vars_names))}
	return variables

def loadData(filename):
	data = []
	with open(filename, 'r') as file:
		reader = csv.DictReader(file)
		# Get the row that corresponds to variables are parse the terms to get the final variables
		# variables_raw = next(reader)
		# header = [i for i in variables_raw.keys()] # header
		# variables = parse_vars(header, variables_raw) # variables
		vars_n_refs = json_conf["vars"]
		variables = parse_vars(vars_names=vars_n_refs[0], refs=vars_n_refs[1])

		# Get the configuration (second row)
		field_guide = next(reader)
		header = [i for i in field_guide.keys()] # header

		columns = {}  # arrange data column-wise

		# And now, the rest of the data
		for line in reader:
			data.append(line)
			row_vals = list(line.values())
			for i in range(len(row_vals)):
				if line["Type"] != "s":
					continue
				columns[i] = columns.get(i, []) + [row_vals[i]]

	print(columns)
	return header, data, field_guide, variables, columns

# ~~** Question Types **~~
# Simple
def QuesSimple(row):
	# unique = {i:row[i] for i in row if conf[i] == "unique"}
	row = row.copy()
	if None in row.keys():
		del row[None]
	# del row["Type"]

	ques_types, ans_types = [], []
	# print("row", row)
	# print("fields", field_guide)
	for i in row.keys():
		if field_guide[i] == "ques":
			ques_types.append(i)
		elif field_guide[i] == "ans":
			ans_types.append(i)

	print("ques and ans types", ques_types, ans_types)

	# To clarify, the ques_type field is the field the value that is given belongs to and the ans_type represents the field that the value to be entered belongs to
	field1 = random.choice(ques_types)
	val1 = row[field1]

	field2 = random.choice(ans_types)
	val2 = row[field2]
	if random.randint(0,3) == 0:
		field1, field2, val1, val2 = field2, field1, val2, val1

	en_espanol = {"English": "inglés", "Spanish": "español"}
	ques = json_conf["simple"].format(val2, en_espanol[field1])
	ans = val1
	return ques, ans

# More Responsive Type Questions
def QuesComplex(row):
	ques = row[header[0]]
	ans = row[header[1]]
	ans_format = {}
	for i,j in enumerate(ans.split()):
		if j[0] == "<":
			ans_format[i] = variables[j[1:]]
	return ques, ans, ans_format


def trimAns(a):
	return a.capitalize()

def selectModule(modules):
	while True:
		print("You can choose from the following modules:")
		for i in module_names.keys():
			print(i, "->", module_names[i])
		try:
			x = str(input("Select Module:\n--> "))
			module = modules[x]
			break
		except KeyError:
			print("-"*25+"ENTER A VALID NUMBER!"+"-"*25)
	return module

def complexQuesTypeCheck(value, expected):
	expected_res = expected  # same thing, my bad
	if expected_res.isnumeric():
		return value in columns[int(expected_res)]
	elif expected_res == "Num":
		return value.isnumeric()
	return False

def complexAnsCheck(ans, a, ans_format):
	okay = "Nice! You got it!"
	nok = "Hmm not quite but Keep Going!"
	split_ans = ans.split()
	special_types = ans_format.keys()
	check = True
	print("enumerating over all the values")
	print("indexes of type placeholders", special_types, ans_format.values())
	for i, j in enumerate(a):
		print("enum", i, j)
		print("checking if placeholder index...", i in special_types)
		if i in special_types:
			print("checking if placeholder type matches...", complexQuesTypeCheck(split_ans[i], ans_format[i]))
		if i in special_types:
			if not complexQuesTypeCheck(split_ans[i], ans_format[i]):
				print("special type check doesn't match", split_ans[i], ans_format[i])
				check = False
				break
		elif not j.lower() == split_ans[i].lower():
			print("word doesn't match", j, split_ans[i])
			check = False
			break
	if check:
		print(okay)
	else:
		print("No no! Think think!\n")
		print("Your Answer:", ans)
		print("Actual Answer", a)


def main():
	"""
	this is the main loop of the function which goes through the data
	"""

	print("Welcome to this quiz program")

	# Select module
	module = selectModule(modules)

	global json_conf
	json_conf = loadConfig("config.json")

	# Load Data
	global header, data, variables, field_guide, columns
	header, data, field_guide, variables, columns = loadData(module)
	print(variables)


	# Start Asking Questions
	questions = {"s": QuesSimple, "c": QuesComplex}
	rand_row = random.choice(data)
	# rand_row = data[-1]
	print(rand_row)
	if not rand_row["Type"] in questions.keys():
		raise TypeError("Unknown Type of question found. Please refer to the manual for the acceptable question types.")
	question_infos = questions[rand_row["Type"]](rand_row)
	q, a = question_infos[0], question_infos[1]
	ans = input(q+"\n--> ").strip()

	while ans != "quit" and ans != "q":  # Ask Questions till user doesn't want to stop
		if rand_row["Type"] == "s":  # if it's a simple question
			if ans.lower() == a.lower():  # Answer is corrent
				print("nice! keep going\n")
			else:   # Ans not correct
				print("Your Answer:", ans)
				print("Actual Answer", a)
				print("No no! Think think!\n")
		elif rand_row["Type"] == "c":  # but on the off chance it's not~
			split_a = a.split()  # split real ans to compare every word
			ans_format = question_infos[2]
			complexAnsCheck(ans, split_a, ans_format)  # check if the answer is correct


		print()
		rand_row = random.choice(data)  # ask the question again
		if not rand_row["Type"] in questions.keys():
			raise TypeError("Unknown Type of question found. Please refer to the manual for the acceptable question types.")
		question_infos = questions[rand_row["Type"]](rand_row)
		q, a = question_infos[0], question_infos[1]
		ans = str(input(q+"\n--> "))

	# If user stops, give closing statement
	print("-"*25+"\nThank you for using this tool hope you liked it :)\n")			


if __name__ == '__main__':  # don't run if this is just an import
	# Call the function
	main()

