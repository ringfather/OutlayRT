from mainapp.models import Expenses, Macros
from datetime import datetime
def decodeExpense(coded, macros, user_name):
	'''
	Parses the user input for expense and stores the data 
	into database
	'''
	result = {}
	# optional name, user can update later
	if not coded[0].isdigit():
		name = macros[coded[0]]
	else:
		name = None
	result['name'] = name
	# get amount
	amount = ""
	i = 1
	while i < len(coded) and (coded[i].isdigit() or coded[i] == '.'):
		amount += coded[i]
		i += 1
	amount = float(amount)
	result['amount'] = amount
	# optional description, user can update later
	description = coded[i:]
	result['description'] = description
	# get date
	date = datetime.now()
	result['date'] = date
	result['username'] = user_name
	return result

def saveExpense(final_form, result):
	final_form.name = result['name']
	final_form.amount = result['amount']
	final_form.date = result['date']
	final_form.description = result['description']
	final_form.username = result['username']

def decodeMacro(user_input, user_name):
	result = {}
	result['key'] = user_input[0]
	result['username'] = user_name
	result['value'] = user_input[1:]
	result['standard'] = False
	return result

def saveMacro(final_form, result):
	final_form.username = result['username']
	final_form.key = result['key']
	final_form.value = result['value']
	final_form.standard = result['standard']

def getMacros(user_name):
	'''
	Returns a dictionary of standard and user set
	macros with user set macros overwriting standard ones
	'''
	macros = {}
	standard_list = Macros.objects.filter(standard=True) # standard list of macros
	macro_list = Macros.objects.filter(username=user_name) # user list of macros
	for item in macro_list:
		macros[item.key] = item.value
	for item in standard_list:
		if item.key not in macros:
			macros[item.key] = item.value
	return macros

def getExpenses(user_name):
	return Expenses.objects.filter(username=user_name)