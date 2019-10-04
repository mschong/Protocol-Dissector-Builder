import json

class StartFieldBackEnd:

	def __init__(self, protocolName, protocolDescription):
		self.name = protocolName
		self.description = protocolDescription

	def editProperties(self, protocolName, protocolDescription):
		self.name = protocolName
		self.description = protocolDescription

def jdefault(o):
	return o.__dict__

if __name__ == '__main__':

	root = StartFieldBackEnd("MYDNS", "This is a sample MYDNS start field.")
	print(json.dumps(root, default=jdefault))

	root.editProperties("MYDNS", "Editted the description.")
	print(json.dumps(root, default=jdefault))