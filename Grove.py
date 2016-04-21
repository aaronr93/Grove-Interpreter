# OOPL 5 - Grove Parser - Rosenberger Nafziger Kibler
# MAIN

if __name__ == "__main__":

	while True:
		userInput = input("Grove>>") #.strip()
		
		if len(userInput) == 0:
			break
		
		try:
			parse(userInput)
		except GroveError:
			print("Invalid command")

			
def parse(str):
	