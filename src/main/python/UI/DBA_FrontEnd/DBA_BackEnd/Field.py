import json

class FieldBackEnd:

	def __init__(self, fieldLength, fieldName, fieldDescription):
		self.length = fieldLength
		self.name = fieldName
		self.description = fieldDescription

	def editProperties(self, fieldName, fieldDescription):
		self.name = fieldName
		self.description = fieldDescription


def jdefault(o):
	return o.__dict__

if __name__ == '__main__':
	
	field = FieldBackEnd("test", "t", "This is a test")
	print(json.dumps(field, default=jdefault))

	field.editProperties("test", "Editted description")
	print(json.dumps(field, default=jdefault))