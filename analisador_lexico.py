from simula_automato import *

class AnalisadorLexico():
	def __init__(self, caracteres):
		self.caracteres = caracteres
		self.atomos = []
		self.palavras_reservadas = ["if", "else", "while", "print", "call", "get", "int", "bool", "void", "return", "True", "False"]
		self.tabela_de_simbolos = []
								
	def inicia(self):
		i = 0
		while i < len(self.caracteres):
			cadeia = ""
			i_inicial = i
			while i < len(self.caracteres) and self.caracteres[i][0] != ' ' and self.caracteres[i][0] != '\n' and ord(self.caracteres[i][0]) != 9:
				if self.caracteres[i][1] == "letra":
					cadeia += "l"
				elif self.caracteres[i][1] == "digito":
					cadeia += "d"
				else:
					if self.caracteres[i][0] == "=":
						cadeia += "="
					elif self.caracteres[i][0] == "!":
						cadeia += "!"
					elif self.caracteres[i][0] == "/":
						cadeia += "/"
					elif self.caracteres[i][0] == ">":
						cadeia += ">"
					elif self.caracteres[i][0] == "<":
						cadeia += "<"
					else:
						cadeia += "s"
				i += 1

			if cadeia != "":	
				cadeia += "#"
				print(cadeia)
				estado_final, void = simula_automato(cadeia, "txts/pre_categorizador.txt", False, False, False)
				estado_final = estado_final.nome
				if estado_final == "q1":
					cadeia = ""
					for i in range(i_inicial,i):
						cadeia += self.caracteres[i][0]
					self.atomos.append(["NUMERO", cadeia])
				elif estado_final == "q2":
					cadeia = ""
					for i in range(i_inicial,i):
						cadeia += self.caracteres[i][0]
					if cadeia in self.palavras_reservadas:
						self.atomos.append([cadeia, cadeia])
					else:
						if cadeia not in self.tabela_de_simbolos:
							self.tabela_de_simbolos.append({'nome': cadeia, 'definido': False, 'referenciado': False})
						self.atomos.append(["IDENTIFICADOR", cadeia])
				elif estado_final == "q3":
					self.atomos.append(["=", "="])
				elif estado_final == "q4":
					self.atomos.append(["==", "=="])
				elif estado_final == "q5":
					self.atomos.append(["!", "!"])
				elif estado_final == "q6":
					self.atomos.append(["!=", "!="])
				elif estado_final == "q7":
					self.atomos.append(["/", "/"])
				elif estado_final == "q8":
					while self.caracteres[i][0] != '\n':
						i += 1
				elif estado_final == "q9":
					self.atomos.append([">", ">"])
				elif estado_final == "q10":
					self.atomos.append([">=", ">="])
				elif estado_final == "q11":
					self.atomos.append(["<", "<"])
				elif estado_final == "q12":
					self.atomos.append(["<=", "<="])
				elif estado_final == "q13":
					self.atomos.append([self.caracteres[i-1][0], self.caracteres[i-1][0]])

			i += 1

		return [self.atomos, self.tabela_de_simbolos]