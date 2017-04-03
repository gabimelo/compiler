from estado import *

class Automato():
	def __init__(self, cadeia = ""):
		self.estados = {}
		self.simbolos = []
		self.direcaoLeitura = "d"
		self.fita = cadeia
		self.posicaoCabecote = 0
		self.estadoAtual = None

	def _imprimeConfiguracao(self):
		print("Dipositivo na configuração M = " + self.estadoAtual.nome, end=" X ") 
		print(self.fita[:self.posicaoCabecote], end=" X ")
		print(self.fita[self.posicaoCabecote], end=" X ")
		print(self.fita[self.posicaoCabecote + 1:], end="\n\n")

	def erroFaltaDeTransicao(self):
		print("Ocorreu um erro de falta de transição")

	def erroFimDaFita(self):
		print("O automato tentou recuar à esquerda do fim da fita, e portanto a máquina ficou bloqueada")

	def adicionaEstado(self, nomeEstado, estado):
		self.estados[nomeEstado] = estado
	
	def adicionaSimbolo(self, simbolo):
		self.simbolos.append(simbolo)

	def adicionaTransicao(self, origem, simbolo, destino):
		self.estados[origem].transicoes[simbolo] = destino

	def inicializa(self, cadeia, rastro):
		for estado in self.estados:
			if self.estados[estado].inicial:
				self.estadoAtual = self.estados[estado]
		self.fita = cadeia

	def movimentoCabecote(self, rastro):
		self.posicaoCabecote += 1
		if rastro:
			print("Cabeçote encontra-se na posição " + str(self.posicaoCabecote))
			self._imprimeConfiguracao()
		return ""

	def fimSimulacao(self, rastro):
		if rastro:
			if self.estadoAtual.aceitacao and self.posicaoCabecote == len(self.fita):
				print("Dispositivo atingiu estado de aceitacao")
			else:
				print("Dispositivo nao atingiu estado de aceitacao")

			self._imprimeConfiguracao()
