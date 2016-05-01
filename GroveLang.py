# OOPL 5 - Grove Parser - Rosenberger Nafziger
# Grove Lang
import importlib

var_table = {}

class Expr:
	def __init__(self, children):
		pass


class Num(Expr):
	def __init__(self, value):
		self.value = value
	
	def eval(self):
		return self.value

class Obj(Expr):
	def __init__(self, value):
		self.value = value
	
	def eval(self):
		return self.value


class Name(Expr):
	def __init__(self, name):
		self.name = name
	
	def getName(self):
		return self.name
		
	def eval(self):
		if self.name in var_table:
			return var_table[self.name]
		else:
			raise GroveError("Undefined variable " + self.name)


class Stmt:
	def __init__(self, name, expr):
		self.name = name
		self.expr = expr
		if not isinstance(self.expr, Expr):
			raise GroveError("Expected expression but received " + str(type(self.expr)))
		if not isinstance(self.name, Name):
			raise GroveError("Expected variable name but received " + str(type(self.name)))
	
	def eval(self):
		if(self.name.getName() == "import"):
			globals()[self.expr.eval()] = importlib.import_module(self.expr.eval())
		else:
			if self.name in var_table:
				var_table[self.name.getName()] = self.expr.eval()


class Addition(Expr):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		if not isinstance(self.a, Expr):
			raise GroveError("Expected expression but received " + str(type(self.a)))
		if not isinstance(self.b, Expr):
			raise GroveError("Expected expression but received " + str(type(self.b)))
			
		# Checks that the numbers being added are the same type
		if type(a) != type(b):
			raise GroveError("Addition expected equal types but received types " + str(type(self.a)) + " + " + str(type(self.b)))
	
	def eval(self):
		return self.a.eval() + self.b.eval()


class StringLiteral(Expr):
	def __init__(self, str):
		self.str = str
<<<<<<< HEAD
		
	def eval(self):
		if containsAny(self.str, string.whitespace):
			raise GroveError("String literal " + self.str + " is not valid. Strings should not contain whitespace.")
		if "\"" in self.str:
			raise GroveError("String literal " + self.str + " is not valid. Strings should not contain double quotes.")
		else:
			return self.str

def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]
=======
		# TODO: Add checking for valid Grove strings
		#I don't think we want to check in here... Name and Num don't have checks
		
	def eval(self):
		return self.str
>>>>>>> 62cf4bf504cae00800c8a64fe66f113ecb7e4269
