from automato import *

class AutomatoFinito(Automato):
	def __init__(self):
		super().__init__()
		self.direcaoLeitura = "d"

	def inicializa(self, cadeia, rastro):
		super().inicializa(cadeia, rastro)
		self.posicaoCabecote = 0
		if rastro:
			self._imprimeConfiguracao()

	def leSimbolo(self, rastro, gera_ape = False):
		simbolo = self.fita[self.posicaoCabecote]
		if simbolo == "#":
			return ['fim']
		else:
			try:
				nomeNovoEstado = self.estadoAtual.transicoes[simbolo][0]
			except KeyError:
				raise
			
			if rastro:
				print("A máquina consome o símbolo " + simbolo, end ="")
				print(" e vai do estado " + self.estadoAtual.nome, end="")
				print(" ao estado " + nomeNovoEstado)

			for estado in self.estados:
				if estado == nomeNovoEstado:
					self.estadoAtual = self.estados[estado]

			return [""]
