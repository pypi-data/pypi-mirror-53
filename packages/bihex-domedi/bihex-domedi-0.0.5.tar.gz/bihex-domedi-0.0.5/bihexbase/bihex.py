class Bihex:
	def __init__(self, number):
		self.number = 0
		if number[0] == "d":
			exec("self.number = int(" + "0" + "number[1:])")
			self.base = "dec"
		if number[0] == "b":
			exec("self.number = int(" + "0b" + "number[1:])")
			self.base = "bin"
		if number[0] == "x":
			exec("self.number = int(" + "0x" + "number[1:])")
			self.base = "hex"
		if number[0] == "o":
			exec("self.number = int(" + "0o" + "number[1:])")
			self.base = "oct"

	def returnnum(self, base):
		if base == "d":
			return str(self.number)
		if base == "b":
			return bin(self.number)
		if base == "x":
			return hex(self.number)
		if base == "o":
			return oct(self.number)

	def returnbase(self):
		return self.base