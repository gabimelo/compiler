from minHeap import *

class MotorDecomposicao():
	def __init__(self, lista_inicial_eventos, texto_fonte):
		self.agora = 0
		self.lista_eventos = lista_inicial_eventos
		self.texto_fonte = texto_fonte
		self.count = 0
		self.caracteres = []
		self.linha = ""
		self.count_linhas = 0
		self.log_linhas = "Linhas: \n"
		self.log_caracteres = "Caracteres: \n"
		self.posicao = 0
								
	def inicia(self):
		# self.rastro_linhas = self.aciona_rastro("Deseja imprimir listagem de linhas? (s/n) ")
		# self.rastro_caracteres = self.aciona_rastro("Deseja imprimir listagem de caracteres? (s/n) ")
		self.rastro_linhas = True
		self.rastro_caracteres = True
		self.arquivo = open(self.texto_fonte)
		fim = False
		while not fim:
			if self.lista_eventos.is_empty():
				fim = True
			else:
				fim = self.processa_evento(self.lista_eventos.serve())
		return self.caracteres

	def processa_evento(self, evento):
		self.count += 1
		self.agora = evento[0]
		tipo_evento = evento[1]

		fim = False

		if tipo_evento == "LE_LINHA":
			self.linha = self.arquivo.readline()
			if self.linha:
				if self.rastro_linhas:
					self.log_linhas += str(self.count_linhas) + ": " + self.linha
				self.count_linhas += 1
				self.lista_eventos.append([self.agora, "LE_CARACTER"])
			else:
				self.lista_eventos.append([self.agora, "FIM_SIMULACAO"])
						
		elif tipo_evento == "LE_CARACTER":
			try:
				caracter = self.linha[self.posicao]
				self.lista_eventos.append([self.agora, "LE_CARACTER"])
				if caracter.isalpha():
					self.caracteres.append([caracter,"letra"])
				elif caracter.isdigit():
					self.caracteres.append([caracter,"digito"])
				else:
					self.caracteres.append([caracter,"outros"])
				if self.rastro_caracteres:
					if caracter.isalpha():
						self.log_caracteres += "letra "
					elif caracter.isdigit():
						self.log_caracteres += "digito "
					else:
						self.log_caracteres += "caracter especial "
					self.log_caracteres += caracter + " - codigo ASCII em hexa: " + str(hex(ord(caracter))) + " - codigo ASCII em decimal: " + str(ord(caracter)) + "\n"
				self.posicao += 1
			except IndexError:
				self.posicao = 0
				self.lista_eventos.append([self.agora, "LE_LINHA"])				

		elif tipo_evento == "FIM_SIMULACAO":
			# self.gera_relatorio()
			print(self.log_linhas)
			print(self.log_caracteres)
			fim = True

		else:
			raise TypeError("Tipo inválido de evento")
		
		return fim
	
	def gera_relatorio(self):
		print("Foram processados " + str(self.count) + " eventos, em " + str(self.agora) + " unidades de tempo.")

	def aciona_rastro(self, prompt): 
		rastro = "?"
		while rastro == "?": 
			rastro = input(prompt)
			if rastro == "s":
				rastro = True
			elif rastro == "n":
				rastro = False
			else:
				print("Opções para rastro: s ou n")
		return rastro		