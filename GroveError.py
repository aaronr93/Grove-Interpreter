# OOPL 5 - Grove Parser - Rosenberger Nafziger
# GroveError

class GroveError(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
