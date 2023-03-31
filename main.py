

import csv
import random

"""
This program takes in a table and asks question based on the table
usefullness: ****
productivity: **
level of boredom: *******

It takes in three fields:
-unique field
-group field
-special field


[
{row1},
{row2}
]





"""


def loadData(file):
	data = []
	with open(file, 'r') as filename:
		reader = csv.DictReader(filename)
		conf = next(reader)
		for line in reader:
			data.append(line)
	header = [i for i in data[0].keys()]
	return header, data, conf



def QuesUnique(row):
	unique = {i:row[i] for i in row if conf[i] == "unique"}
	print(unique)
	field1 = random.choice(list(unique.keys()))
	val1 = unique[field1]
	del unique[field1]
	field2 = random.choice(list(unique.keys()))
	val2 = unique[field2]
	ques = "Give the {} where the {} is {}".format(field1, field2, val2)
	ans = val1
	return ques, ans



def trimAns(a):
	return a.capitalize()

def selectModule(modules):
	while True:
		print("You can choose from the following modules:")
		print("Periodic Table (1)")
		try:
			x = str(input("Select Module:\n--> "))
			module = modules[x]
			break
		except KeyError:
			print("-"*25+"ENTER A NUMBER ONLY!"+"-"*25)
	return module


def main():
	"""
	this is the main loop of the function which goes through the data
	"""
	modules = {"1":"data.csv", "2": "data2.csv"}
	print("Welcome to this quiz program")

	# Select module
	module = selectModule(modules)

	# Load Data
	global header, data, conf
	header, data, conf = loadData(module)

	# Start Asking Questions
	questions = [QuesUnique]
	ques = random.choice(questions)
	q, a = ques(random.choice(data))
	ans = str(input(q+"\n--> "))

	while ans != "quit":  # Ask Questions till user doesn't want to stop
		if ans == trimAns(a):  # Answer is corrent
			print("nice! keep going\n")
		else:   # Ans not correct
			print("Your Answer:", ans)
			print("Actual Answer", a)
			print("No no! Think think!\n")
		ques = random.choice(questions)    # Ask questions again
		q, a = ques(random.choice(data))
		ans = str(input(q+"\n--> "))

	# If user stops, give closing statement
	print("-"*25+"\nThank you for using this tool hope you liked it :)\n")			


if __name__ == '__main__':
	main()

