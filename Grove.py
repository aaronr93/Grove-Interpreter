# OOPL 5 - Grove Parser - Rosenberger Nafziger
# Grove Parser Main
import sys

exec(open("GroveLang.py").read())
exec(open("GroveError.py").read())

# Utility methods for handling parse errors
def check(condition, message = "Unexpected end of expression"):
	""" Checks if condition is true, raising a ValueError otherwise """
	if not condition:
		raise GroveError("" + message)
		
		
def expect(token, expected):
	""" Checks that token matches expected
		If not, throws a ValueError with explanatory message """
	if token != expected:
		check(False, "Expected '" + expected + "' but found '" + token + "'")


def is_expr(x):
	if not isinstance(x, Expr):
		check(False, "Expected expression but found " + str(type(x)))	 
		

def is_int(s):
	""" Takes a string and returns True if in can be converted to an integer """
	try:
		int(s)
		return True
	except ValueError:
		return False



def parse(s):
	""" Return an object representing a parsed command
		Throws ValueError for improper syntax """
	(root, remaining_tokens) = parse_tokens(s.split())
	
	# The parse call should have used all the tokens
	check(len(remaining_tokens) == 0, "Expected end of command but found '" + " ".join(remaining_tokens) + "'")
		
	return root
		
		
def parse_tokens(tokens):
	""" Returns a tuple:
		(an object representing the next part of the expression,
		 the remaining tokens)
	"""
	check(len(tokens) > 0)
	start = tokens[0]
	
	if is_int(start):
		return (Num(int(start)), tokens[1:])
	elif start[0] == "\"":
		#StringLiteral
		expect(start[-1], "\"")
		check(" " not in start[1:-1] and "\"" not in start[1:-1], "StringLiterals cannot contain whitespace or quotes")
		return (StringLiteral(start[1:-1]), tokens[1:])

	elif start == "call":
		expect(tokens[1], "(")
		(name, tokens) = parse_tokens(tokens[2:])
		check(len(tokens) > 1)
		#make sure the object exists
		try:
			test = var_table[name.getName()]
		except:
			raise GroveError("Undefined variable " + name.getName())
		(methodName, tokens) = parse_tokens(tokens)
		#check(len(tokens) > 1)
		try:
			callable(getattr(var_table[name.getName()], methodName.getName()))
		except:
		 	raise GroveError("Object " + name.getName() + " does not have method " + methodName.getName())

	elif start == "+":
		expect(tokens[1], "(")
		(child1, tokens) = parse_tokens(tokens[2:])
		check(len(tokens) > 1)
		expect(tokens[0], ")")
		expect(tokens[1], "(")
		(child2, tokens) = parse_tokens(tokens[2:])
		check(len(tokens) > 0)
		expect(tokens[0], ")")
		return (Addition(child1, child2), tokens[1:])
			
	elif start == "set":
		(varname, tokens) = parse_tokens(tokens[1:])
		expect(tokens[0], "=")
		ret = 0
		if tokens[1] == "new":
			class_name = tokens[2]
			if "." in class_name:
				parts = class_name.split(".")
				module = globals()[parts[0]]
				cls = getattr(module, parts[1])
				obj = cls()
				ret = obj
			else:
				try: 
					obj = globals()[class_name]()
					ret = obj
				except:
					cls = getattr(globals()["__builtins__"], class_name)
					obj = cls()
					ret = obj
			return(Stmt(varname,Obj(ret)), tokens[3:])
		else:
			(child, tokens) = parse_tokens(tokens[1:])
			return (Stmt(varname, child), tokens)
		
	elif start == "quit":
		sys.exit()
		
	elif start == "exit":
		sys.exit()
	
	elif start == "import":
		return(Stmt(Name("import"), Obj(tokens[1])), tokens[2:])
		
	else:
		""" Variable name """		
		check(start[0].replace("_", "a").isalpha() and (start[1:].replace("_", "a").isalnum() or start[1:] == ""), "Variable names must be alphanumeric and begin with an alphabetic character.")
		remaining = tokens[1:]
		return (Name(start), remaining)
		

if __name__ == "__main__":

	while True:
		userInput = input("Grove>> ") #.strip()
		if len(userInput) == 0:
			break
		
		try:
			root = parse(userInput)
			result = root.eval()
			if not result is None:
				print(result)
		except ValueError as error:
			print(error)
		except GroveError as error:
			print("GROVE: " + str(error))

			