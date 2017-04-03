from automato import *

class MaquinaDeTuring(Automato):
	def __init__(self):
		super().__init__()

	def inicializa(self, cadeia, rastro):
		super().inicializa(cadeia, rastro)
		self.posicaoCabecote = len(self.fita) - 1
		if rastro:
			self._imprimeConfiguracao()

	def movimentoCabecote(self, rastro):
		if self.direcaoLeitura == "d":
			self.posicaoCabecote += 1
			if self.posicaoCabecote == len(self.fita):
				self.fita = self.fita + "#"
		else:
			self.posicaoCabecote -= 1
			if self.posicaoCabecote == len(self.fita) -2 and self.fita[-1] == "#":
				self.fita = self.fita[:-1]
			if self.posicaoCabecote == -1:
				self.posicaoCabecote = 0
				return "bloqueia"	
		if rastro:
			print("Cabeçote encontra-se na posição " + str(self.posicaoCabecote))
			self._imprimeConfiguracao()
		return ""

	def escreveSimbolo(self, rastro, simbolo):
		self.fita = self.fita[:self.posicaoCabecote] + simbolo + self.fita[self.posicaoCabecote + 1:]
		if rastro:
			print("A máquina escreve o símbolo " + simbolo)
			self._imprimeConfiguracao()

	def leSimbolo(self, rastro):
		simbolo = self.fita[self.posicaoCabecote]
		try:
			novoEstado = self.estadoAtual.transicoes[simbolo]
		except KeyError:
			raise

		if rastro:
			print("A máquina consome o símbolo " + simbolo + " e vai do estado " + self.estadoAtual.nome + " ao estado " + novoEstado[0])

		for estado in self.estados:
			if estado == novoEstado[0]:
				self.estadoAtual = self.estados[estado]

		if novoEstado[0] == "h":
			if novoEstado[1] == "L":
				self.direcaoLeitura = "e"
				return ["mover","fim"]
			elif novoEstado[1] == "R":
				self.direcaoLeitura = "d"
				return ["mover","fim"]
			return ["fim"]

		if novoEstado[1] == "L":
			self.direcaoLeitura = "e"
			return ["mover"]
		elif novoEstado[1] == "R":
			self.direcaoLeitura = "d"
			return ["mover"]
		else:
			return ["escrever", novoEstado[1]]