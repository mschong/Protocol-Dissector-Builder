import json

class Condition:

	def __init__(self, leftSide, operator, rightSide):
		self.leftSide = leftSide
		self.operator = operator
		self.rightSide = rightSide
		# self.outcomes = ['false': None, 'true': None]

	# def __init__(self, operator, operand):
	# 	self.operator = operator
	# 	self.operand = operand
		# self.outcomes = ['false': None, 'true': None]

	def editProperties(self, leftSide, operator, rightSide):
		self.leftSide = leftSide
		self.operator = operator
		self.rightSide = rightSide

	def editProperties(self, operator, operand):
		self.operator = operator
		self.operand = operand
		
	def addTrue(self, connector):
		self.outcomes['true': connector]

	def addFalse(self, connector):
		self.outcomes['false': connector]

def jdefault(o):
	return o.__dict__

if __name__ == '__main__':

	condition_1 = Condition('a', '>=', 'b')
	print(json.dumps(condition_1, default=jdefault))

	condition_1.editProperties('a', '>', 'b')
	print(json.dumps(condition_1, default=jdefault))

	# condition_2 = Condition('!', 'a')
	# print(json.dumps(condition_2, default=jdefault))

	# condition_2.editProperties('!', 'b')
	# print(json.dumps(condition_2, default=jdefault))

