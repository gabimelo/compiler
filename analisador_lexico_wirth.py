from simula_automato import *

class AnalisadorLexicoWirth():
	def __init__(self, caracteres):
		self.caracteres = caracteres
		self.atomos = []
		self.tabela_de_simbolos = []
								
	def inicia(self):
		i = 0
		while i < len(self.caracteres):
			if self.caracteres[i][0] == "=":
				self.atomos.append(["=", "="])
			elif self.caracteres[i][0] == "|":
				self.atomos.append(["|", "|"])
			elif self.caracteres[i][0] == ".":
				self.atomos.append([".", "."])
			elif self.caracteres[i][0] == "(":
				self.atomos.append(["(", "("])
			elif self.caracteres[i][0] == ")":
				self.atomos.append([")", ")"])
			elif self.caracteres[i][0] == "[":
				self.atomos.append(["[", "["])
			elif self.caracteres[i][0] == "]":
				self.atomos.append(["]", "]"])
			elif self.caracteres[i][0] == "{":
				self.atomos.append(["{", "{"])
			elif self.caracteres[i][0] == "}":
				self.atomos.append(["}", "}"])
			elif self.caracteres[i][0] == '"':
				cadeia = ""
				i += 1
				while self.caracteres[i][0] != '"':
					cadeia += self.caracteres[i][0]
					i += 1
				print(cadeia)
				self.atomos.append(["T", cadeia])
			elif self.caracteres[i][1] == "letra":
				cadeia = ""
				while self.caracteres[i][0] != ' ':
					cadeia += self.caracteres[i][0]
					i += 1
				if cadeia == "IDENTIFICADOR" or cadeia == "NUMERO":
					self.atomos.append(["T", cadeia])
				else:
					self.atomos.append(["N", cadeia])
			# else:
			# 	self.atomos.append([" ", " "])
			i += 1

		return [self.atomos, self.tabela_de_simbolos]