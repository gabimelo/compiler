from automato import *

class AutomatoDePilha(Automato):
	def __init__(self):
		super().__init__()
		self.direcaoLeitura = "d"
		self.pilha = []
		self.submaquinas = {}

	def inicializa(self, cadeia, rastro, posicaoCabecote = 0, cadeia_valores = False):
		super().inicializa(cadeia, rastro)
		self.posicaoCabecote = posicaoCabecote
		self.cadeia_valores = cadeia_valores
		self.maquinaAtual = self
		if rastro:
			self._imprimeConfiguracao()

	def fimSimulacao(self, rastro, pilha_vazia = True):
		if rastro:
			if self.maquinaAtual.estadoAtual.aceitacao and self.posicaoCabecote == len(self.fita) and pilha_vazia:
				print("Dispositivo atingiu estado de aceitacao")
			if (self.posicaoCabecote == len(self.fita) and pilha_vazia):
				while not (self.maquinaAtual.estadoAtual.aceitacao):
					try:
						simbolo = 'E'
						nomeNovoEstado = self.maquinaAtual.estadoAtual.transicoes[simbolo][0]
						for estado in self.maquinaAtual.estados:
							if estado == nomeNovoEstado:
								self.maquinaAtual.estadoAtual = self.maquinaAtual.estados[estado]
						self._imprimeConfiguracao()
						if self.maquinaAtual.estadoAtual.aceitacao:
							print("Dispositivo atingiu estado de aceitacao")
					except Exception:
						print("Dispositivo nao atingiu estado de aceitacao")
						break

			self._imprimeConfiguracao()

	def leSimbolo(self, rastro, gera_ape = False):
		simbolo = self.fita[self.posicaoCabecote]
		if simbolo == "#":
			return ['fim']
		else:
			array_retorno = []
			try:
				nomeNovoEstado = self.maquinaAtual.estadoAtual.transicoes[simbolo][0]
				array_retorno.append("nao_vazio")
			except KeyError:
				self.posicaoCabecote -= 1
				array_retorno.append("vazio")
				try:
					simbolo = 'E'
					nomeNovoEstado = self.maquinaAtual.estadoAtual.transicoes[simbolo][0]
				except Exception:
					array_retorno.insert(0, "desempilha")
					return array_retorno
			
			if "$" not in nomeNovoEstado:
				if rastro:
					if simbolo != "E":
						print("A máquina consome o símbolo " + simbolo, end ="")
					else:
						print("A máquina faz transição em vazio", end ="")		
					print(" e vai do estado " + self.maquinaAtual.estadoAtual.nome, end="")
					print(" ao estado " + nomeNovoEstado)

				for estado in self.maquinaAtual.estados:
					if estado == nomeNovoEstado:
						self.maquinaAtual.estadoAtual = self.maquinaAtual.estados[estado]

				if self.maquinaAtual.estadoAtual.aceitacao:
					try:
						self.maquinaAtual.estadoAtual.transicoes[self.fita[self.posicaoCabecote+1]][0]
						array_retorno.insert(0, "")
					except Exception:
						array_retorno.insert(0, "desempilha")

			else:
				nomeNovoEstado = nomeNovoEstado.split("$")
				submaquina = nomeNovoEstado[0]
				nomeNovoEstado = nomeNovoEstado[1]

				if rastro:
					if simbolo != "E":
						print("A máquina consome o símbolo " + simbolo, end ="")
					else:
						print("A máquina faz transição em vazio", end ="")		
					print(" e vai à máquina " + submaquina, end="")
					print(" empilhando o estado " + nomeNovoEstado)

				array_retorno.insert(0, "empilha")
				array_retorno.insert(1, nomeNovoEstado)
				array_retorno.insert(2, submaquina)
			if (gera_ape):
				array_retorno.append(self.geracao_ape(simbolo, gera_ape))
			return array_retorno

	def geracao_ape(self, simbolo, gera_ape):
		if simbolo == "N":
			nao_terminal = self.cadeia_valores[self.posicaoCabecote]
			if not gera_ape["pilha"]:
				gera_ape["nome_submaquina"] = nao_terminal
			else:
				gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@"+nao_terminal+"$q"+str(gera_ape["contador"]))
				gera_ape["estado"] = gera_ape["contador"]
				gera_ape["contador"] += 1

		elif simbolo == "T":
			terminal = self.cadeia_valores[self.posicaoCabecote]
			if terminal not in gera_ape["alfabeto"]:
				gera_ape["alfabeto"].append(terminal)
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@" + terminal + "@q"+str(gera_ape["contador"]))
			gera_ape["estado"] = gera_ape["contador"]
			gera_ape["contador"] += 1			

		elif simbolo == "=":
			gera_ape["pilha"].append([gera_ape["estado"], gera_ape["contador"]])
			gera_ape["contador"] += 1

		elif simbolo == ".":
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@q"+str(gera_ape["pilha"][-1][1]))
			gera_ape = self.gera_arquivo_ape(gera_ape)
			gera_ape["nome_submaquina"] = ""
			gera_ape["estado"] = 0
			gera_ape["contador"] = 1
			gera_ape["pilha"] = []
			gera_ape["transicoes"] = []
			gera_ape["alfabeto"] = []

		elif simbolo == "(":
			gera_ape["pilha"].append([gera_ape["estado"], gera_ape["contador"]])
			gera_ape["contador"] += 1

		elif simbolo == ")":
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@q"+str(gera_ape["pilha"][-1][1]))
			gera_ape["estado"] = gera_ape["pilha"][-1][1]
			gera_ape["pilha"].pop()

		elif simbolo == "[":
			gera_ape["pilha"].append([gera_ape["estado"], gera_ape["contador"]])
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@q"+str(gera_ape["pilha"][-1][1]))
			gera_ape["contador"] += 1

		elif simbolo == "]":
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@q"+str(gera_ape["pilha"][-1][1]))
			gera_ape["estado"] = gera_ape["pilha"][-1][1]
			gera_ape["pilha"].pop()

		elif simbolo == "{":
			gera_ape["pilha"].append([gera_ape["contador"], gera_ape["contador"]])
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@q"+str(gera_ape["pilha"][-1][1]))
			gera_ape["estado"] = gera_ape["contador"]
			gera_ape["contador"] += 1

		elif simbolo == "}":
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@q"+str(gera_ape["pilha"][-1][1]))
			gera_ape["estado"] = gera_ape["pilha"][-1][1]
			gera_ape["pilha"].pop()

		elif simbolo == "|":
			gera_ape["transicoes"].append("q"+str(gera_ape["estado"])+"@E@q"+str(gera_ape["pilha"][-1][1]))
			gera_ape["estado"] = gera_ape["pilha"][-1][0]

		return gera_ape

	def gera_arquivo_ape(self, gera_ape):
		arquivo = open(gera_ape["arquivo"],"r")
		primeira_linha = arquivo.readline()
		arquivo.close()
		
		arquivo = open(gera_ape["arquivo"],"a")
		texto_para_escrita = ""
		if primeira_linha == "":
			texto_para_escrita += "##\nAPE\n"
		else:
			texto_para_escrita += "##\nAPE\n"+ gera_ape["nome_submaquina"] + "\n"
		
		for i in range(gera_ape["contador"]):
			texto_para_escrita += "q" + str(i) + ","
		texto_para_escrita += "q" + str(i+1) + "\n"
		
		for simbolo in gera_ape["alfabeto"]:
			texto_para_escrita += simbolo + "@"
		texto_para_escrita = texto_para_escrita[:-1]
		texto_para_escrita+= "\n"
		
		for item in gera_ape["transicoes"]:
			texto_para_escrita += str(item) + "\n"
			texto_para_escrita += "q1@E@q" + str(i+1) + "\n"
		texto_para_escrita += "#\nq0\nq"+str(i+1)+"\n"
		arquivo.write(texto_para_escrita)
		arquivo.close()
		return gera_ape
