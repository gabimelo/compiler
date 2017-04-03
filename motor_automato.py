from minHeap import *
from automato import *
from automato_finito import *
from automato_de_pilha import *
from maquina_de_turing import *

class MotorAutomato():
	def __init__(self, rastro, listaEventos, dispositivo, cadeia, gera_ape = False, cadeia_valores = False, gera_semantica = False, tabela_simbolos = []):
		self.agora = 0
		self.rastro = rastro
		self.listaEventos = listaEventos
		self.automato = dispositivo
		self.automato_atual = self.automato
		self.nome_automato_atual = "PROGRAMA"
		self.cadeia = cadeia
		self.count = 0
		self.estado_final = None
		self.gera_ape = gera_ape
		self.cadeia_valores = cadeia_valores
		self.gera_semantica = gera_semantica
		self.pilha_geracao_semantica = []
		self.pilha_operadores = []
		self.pilha_operandos = []
		self.tabela_simbolos = tabela_simbolos
		self.codigo = ""
		self.contador_condicoes = 0
		self.contador_loops = 0
		self.contador_funcoes = 0
		self.codigo_declaracoes_funcoes = ""
								
	def inicia(self):
		fim = False
		while not fim:
			if self.listaEventos.is_empty():
				fim = True
			else:
				fim = self.processaEvento(self.listaEventos.serve())
		return self.estado_final, self.gera_ape


	def processaEvento(self, evento):
		self.count += 1
		self.agora = evento[0]
		tipoEvento = evento[1]

		fim = False
		
		if tipoEvento == "partidaInicial":
			if self.cadeia_valores:
				self.automato_atual.inicializa(self.cadeia, self.rastro, 0, self.cadeia_valores)
			else:
				self.automato_atual.inicializa(self.cadeia, self.rastro)

		elif tipoEvento == "leSimbolo":
			try:
				acao = self.automato_atual.leSimbolo(self.rastro, self.gera_ape)
				if acao[0] == "fim":
					self.listaEventos.append([self.agora, "fimSimulacao"])
					self.estado_final = self.automato_atual.estadoAtual.nome
				elif acao[0] == "mover":
					self.listaEventos.append([self.agora, "movimentoCabecote"])
					if len(acao) > 1:
						if acao[1] == "fim":
							self.listaEventos.append([self.agora, "fimSimulacao"])
							self.estado_final = self.automato_atual.estadoAtual.nome
				elif acao[0] == "escrever":
					self.listaEventos.append([self.agora, "escreveSimbolo", acao[1]])
				elif acao[0] == "empilha":
					self.listaEventos.append([self.agora, "empilha", acao[1], acao[2]])
					if acao[3] == "vazio":
						self.listaEventos.append([self.agora, "movimentoCabecote"])
						self.listaEventos.append([self.agora, "leSimbolo"])
				elif acao[0] == "desempilha":
					self.listaEventos.append([self.agora, "desempilha"])
					if acao[1] == "vazio":
						self.listaEventos.append([self.agora, "movimentoCabecote"])
						self.listaEventos.append([self.agora, "leSimbolo"])
				elif acao[0] == "":
					if len(acao) > 1 and acao[1] == "vazio":
						self.listaEventos.append([self.agora, "movimentoCabecote"])
						self.listaEventos.append([self.agora, "leSimbolo"])

				if self.gera_ape and acao[0] != "fim":
					self.gera_ape = acao[-1]
					print(self.gera_ape)

				self.chamadas_semanticas()

			except KeyError:
				self.listaEventos.append([self.agora, "erroFaltaDeTransicao"])

		elif tipoEvento == "empilha":
			submaquina_destino = evento[3]
			estado_retorno = evento[2]
			if self.rastro:
				print("------------------Chamada da submaquina " + submaquina_destino + "------------------")
			self.automato.pilha.append([estado_retorno, self.automato_atual, self.nome_automato_atual])
			posicao_cabecote = self.automato_atual.posicaoCabecote
			self.automato_atual = self.automato.submaquinas[submaquina_destino]
			self.nome_automato_atual = submaquina_destino
			self.automato_atual.inicializa(self.cadeia, self.rastro, posicao_cabecote, self.cadeia_valores)
			self.chamadas_semanticas()

		elif tipoEvento == "desempilha":
			if len(self.automato.pilha) > 0:
				if self.rastro:
					print("------------------Retorno de submaquina------------------")
				posicao_cabecote = self.automato_atual.posicaoCabecote
				retorno = self.automato.pilha.pop()
				self.automato_atual = retorno[1]
				self.nome_automato_atual = retorno[2]
				self.automato_atual.posicaoCabecote = posicao_cabecote
				nome_novo_estado = retorno[0]
				for estado in self.automato_atual.estados:
					if estado == nome_novo_estado:
						self.automato_atual.estadoAtual = self.automato_atual.estados[estado]

			self.chamadas_semanticas()

		elif tipoEvento == "escreveSimbolo":
			self.automato_atual.escreveSimbolo(self.rastro, evento[2])
			self.listaEventos.append([self.agora, "leSimbolo"])

		elif tipoEvento == "movimentoCabecote":
			bloqueia = self.automato_atual.movimentoCabecote(self.rastro)
			if bloqueia == "bloqueia":
				self.listaEventos.append([self.agora, "erroFimDaFita"])	
			elif type(self.automato) is MaquinaDeTuring:
				self.listaEventos.append([self.agora, "leSimbolo"])

		elif tipoEvento == "erroFaltaDeTransicao":
			self.automato_atual.erroFaltaDeTransicao()
			self.listaEventos.append([self.agora, "fimSimulacao"])
			self.estado_final = self.automato_atual.estadoAtual.nome

		elif tipoEvento == "erroFimDaFita":
			self.automato_atual.erroFimDaFita()
			self.listaEventos.append([self.agora, "fimSimulacao"])
			self.estado_final = self.automato_atual.estadoAtual.nome

		elif tipoEvento == "fimSimulacao":
			if type(self.automato) is AutomatoDePilha:
				self.automato_atual.fimSimulacao(self.rastro, len(self.automato.pilha) == 0)
			else:
				self.automato_atual.fimSimulacao(self.rastro)
			self.estado_final = self.automato_atual.estadoAtual
			self.geraRelatorio()
			fim = True

		else:
			raise TypeError("Tipo inválido de evento")
		
		return fim
	
	def geraRelatorio(self):
		if self.rastro:
			print("Foram processados " + str(self.count) + " eventos, em " + str(self.agora) + " unidades de tempo.")

	def chamadas_semanticas(self):
		valor_atual = self.cadeia_valores[self.automato_atual.posicaoCabecote]
		if (self.nome_automato_atual == "PROGRAMA"): 
			if (self.automato_atual.estadoAtual == "q0"):
				if(len(self.pilha_geracao_semantica) == 0):
					self.inicializa_codigo_MVN()
			elif (self.automato_atual.estadoAtual == "q1"):
				self.pilha_geracao_semantica.append({'comando': 'declaracao_funcao'})
				self.pilha_geracao_semantica[-1]['tipo_funcao'] = valor_atual
			elif (self.automato_atual.estadoAtual == "q2"):
				self.finalizacao_codigo_MVN()
			elif (self.automato_atual.estadoAtual == "q3"):
				self.checa_declaracao_tabela(valor_atual)
				self.pilha_geracao_semantica[-1]['identificador'] = valor_atual
			elif (self.automato_atual.estadoAtual == "q4"):
				self.pilha_geracao_semantica[-1]['parametros'] = []
			elif (self.automato_atual.estadoAtual == "q5"):
				self.pilha_geracao_semantica[-1][parametros].append([{'tipo': valor_atual}])
			elif (self.automato_atual.estadoAtual == "q6"):
				self.declara_funcao()
			elif (self.automato_atual.estadoAtual == "q7"):
				self.checa_referenciacao_tabela(valor_atual)
				self.pilha_geracao_semantica[-1][parametros][-1]['identificador'] = valor_atual
		
		elif (self.nome_automato_atual == "BLOCO"):
			# declaracao de variaveis
			if (self.automato_atual.estadoAtual == "q2"):
				self.pilha_geracao_semantica.append({'comando': 'declaracao'})
				self.pilha_geracao_semantica[-1]['tipo'] = valor_atual
			elif (self.automato_atual.estadoAtual == "q11"):
				self.checa_declaracao_tabela(valor_atual)
				self.pilha_geracao_semantica[-1]['identificador'] = valor_atual
				self.gera_codigo_declaracao()
			elif (self.automato_atual.estadoAtual == "q16"):
				self.pilha_geracao_semantica[-1]['tamanho'] = valor_atual
			elif (self.automato_atual.estadoAtual == "q18"):
				self.pilha_geracao_semantica[-1]['valor'] = valor_atual
				self.checa_referenciacao_tabela(valor_atual)
				self.realiza_atribuicao()

			# atribuicao
			elif (self.automato_atual.estadoAtual == "q3"):
				self.pilha_geracao_semantica.append({'comando': 'atribuicao', 'identificador': valor_atual})
				self.checa_referenciacao_tabela(valor_atual)
			elif (self.automato_atual.estadoAtual == "q26"):
				self.pilha_geracao_semantica[-1]['posicao'] = valor_atual
				self.checa_referenciacao_tabela(valor_atual)
			elif (self.automato_atual.estadoAtual == "q31" and self.pilha_geracao_semantica[-1]['comando'] == 'atribuicao'):
				self.inclui_codigo_expressao()
			elif (self.automato_atual.estadoAtual == "q19" and self.pilha_geracao_semantica[-1]['comando'] == 'atribuicao'):
				self.realiza_atribuicao()

			# chamada de funcao
			elif (self.automato_atual.estadoAtual == "q4"):
				self.pilha_geracao_semantica.append({'comando': 'call'})
			elif (self.automato_atual.estadoAtual == "q34"):
				self.pilha_geracao_semantica[-1]['nome_funcao'] = valor_atual
				self.checa_referenciacao_tabela(valor_atual)
			elif (self.automato_atual.estadoAtual == "q36"):
				try:
					self.pilha_geracao_semantica[-1]['argumentos']
				except KeyError:
					self.pilha_geracao_semantica[-1]['argumentos'] = []
				self.checa_referenciacao_tabela(valor_atual)
				self.pilha_geracao_semantica[-1]['argumentos'].append(valor_atual)
			elif (self.automato_atual.estadoAtual == "q37"):
				try:
					self.pilha_geracao_semantica[-1]['argumentos']
				except KeyError:
					self.pilha_geracao_semantica[-1]['argumentos'] = []
				self.pilha_geracao_semantica[-1]['argumentos'].append(valor_atual)
			elif (self.automato_atual.estadoAtual == "q41"):
				self.pilha_geracao_semantica[-1]['argumentos'][-1] = self.pilha_geracao_semantica[-1]['argumentos'][-1] + "[" + valor_atual + "]"
				self.checa_referenciacao_tabela(valor_atual)
			elif(self.automato_atual.estadoAtual == "q31" and self.pilha_geracao_semantica[-1]['comando'] == 'call'):
				self.realiza_call()

			# input
			elif (self.automato_atual.estadoAtual == "q5"):
				self.realiza_get()

			# return
			elif (self.automato_atual.estadoAtual == "q6"):
				self.pilha_geracao_semantica.append({'comando': 'return'})
			elif (self.automato_atual.estadoAtual == "q38"):
				self.pilha_geracao_semantica[-1]['valor'] = valor_atual
				self.checa_referenciacao_tabela(valor_atual)
			elif (self.automato_atual.estadoAtual == "q43"):
				self.pilha_geracao_semantica[-1]['posicao'] = valor_atual
				self.checa_referenciacao_tabela(valor_atual)
			elif (self.automato_atual.estadoAtual == "q31" and self.pilha_geracao_semantica[-1]['comando'] == 'return'):
				try:
					self.pilha_geracao_semantica[-1]['valor']
				except KeyError:
					self.pilha_geracao_semantica[-1]['valor'] = valor_atual
				self.realiza_return()

			# print
			elif (self.automato_atual.estadoAtual == "q7"):
				self.pilha_geracao_semantica.append({'comando': 'print'})
			elif (self.automato_atual.estadoAtual == "q29"):
				self.pilha_geracao_semantica[-1]['valor'] = valor_atual
				self.checa_referenciacao_tabela(valor_atual)
			elif (self.automato_atual.estadoAtual == "q30"):
				try:
					self.pilha_geracao_semantica[-1]['valor']
				except KeyError:
					self.pilha_geracao_semantica[-1]['valor'] = valor_atual
				self.gera_codigo_print()
			elif (self.automato_atual.estadoAtual == "q33"):
				self.pilha_geracao_semantica[-1]['posicao'] = valor_atual
				self.checa_referenciacao_tabela(valor_atual)

			# if
			elif (self.automato_atual.estadoAtual == "q8"):
				self.pilha_geracao_semantica.append({'comando': 'if'})
				self.prepara_bloco_if()
			elif (self.automato_atual.estadoAtual == "q21"):
				self.inclui_codigo_expressao()
				self.fecha_condicao_if()
			elif (self.automato_atual.estadoAtual == "q23"):
				self.prepara_bloco_else()
			elif (self.automato_atual.estadoAtual == "q17"):
				self.pilha_geracao_semantica[-1]['else'] = 1
			elif (self.automato_atual.estadoAtual == "q19" and self.pilha_geracao_semantica[-1]['comando'] == 'if'):
				self.finaliza_bloco_if()

			# while
			elif (self.automato_atual.estadoAtual == "q9"):
				self.pilha_geracao_semantica.append({'comando': 'while'})
				self.prepara_bloco_while()
			elif (self.automato_atual.estadoAtual == "q15"):
				self.inclui_codigo_expressao()
				self.fecha_condicao_while()
			elif (self.automato_atual.estadoAtual == "q19" and self.pilha_geracao_semantica[-1]['comando'] == 'while'):
				self.finaliza_bloco_while()			

		elif (self.nome_automato_atual == "EXPRESSAO_COMPARACAO"): 
			if (self.automato_atual.estadoAtual == "q0"):
				if(len(pilha_operandos) != 0):
					self.pilha_operadores.append(valor_atual)
			elif (self.automato_atual.estadoAtual == "q2"):
				self.pilha_operadores.append(valor_atual)

		elif (self.nome_automato_atual == "FATOR"): 
			if (self.automato_atual.estadoAtual == "q1"):
				self.gera_codigo_negacao
			elif (self.automato_atual.estadoAtual == "q2"):
				self.pilha_operandos.append(valor_atual)
			elif (self.automato_atual.estadoAtual == "q3"):
				self.pilha_operandos.append(valor_atual)
				self.checa_referenciacao_tabela(valor_atual)
			elif (self.automato_atual.estadoAtual == "q5"):
				self.inclui_codigo_expressao()
			elif (self.automato_atual.estadoAtual == "q7"):
				self.adiciona_posicao(self.pilha_operandos[-1], valor_atual)
				self.checa_referenciacao_tabela(valor_atual)

	def inicializa_codigo_MVN(self):
		self.codigo += "\n		@ 	/0000\nK0 		K 	/0000\nK2 		K 	/0002\nAUX0 	K 	/0000\nKMM 	MM 	/0000\n		JP  IN"

	def finalizacao_codigo_MVN(self):
		self.codigo += self.codigo_declaracoes_funcoes
		self.codigo += "\n		# 	IN"
		arquivo = open("output.asm","w")
		arquivo.write(self.codigo)
		arquivo.close()

	def checa_declaracao_tabela(self, valor_atual):
		for simbolo in self.tabela_simbolos:
			if simbolo["nome"] == valor_atual:
				if simbolo["definido"] == True:
					raise "Erro de dupla definição"
				simbolo["definido"] = True

	def checa_referenciacao_tabela(self, valor_atual):
		for simbolo in self.tabela_simbolos:
			if simbolo["nome"] == valor_atual:
				if simbolo["definido"] == False:
					raise "Erro: Variável " + valor_atual + " sendo referenciada sem ter sido definida."
				simbolo["referenciado"] = True

	def gera_codigo_declaracao(self):
		try:
			self.pilha_geracao_semantica[-1]["tamanho"]
			self.codigo += "\n" + self.pilha_geracao_semantica[-1]["identificador"] + " 		$ 	=" + self.pilha_geracao_semantica[-1]["tamanho"]
		except KeyError:
			try:
				self.pilha_geracao_semantica[-1]["valor"]
				self.codigo += "\n" + self.pilha_geracao_semantica[-1]["identificador"] + " 		K 	=" + self.pilha_geracao_semantica[-1]["valor"]
			except KeyError:
				self.codigo += "\n" + self.pilha_geracao_semantica[-1]["identificador"] + " 		K 	/0000"
		self.pilha_geracao_semantica.pop()

	def realiza_atribuicao(self):
		self.codigo += "\n		MM 	" + self.pilha_geracao_semantica[-1]["identificador"]
		self.pilha_geracao_semantica.pop()

	def realiza_call(self):
		for item in self.pilha_geracao_semantica[-1]['argumentos']:
			self.codigo += "\n    LD  " + item
			self.codigo += "\n    SC  Push"
		self.codigo += "\n    SC  "	+ self.pilha_geracao_semantica[-1]['nome_funcao']
		self.pilha_geracao_semantica.pop()

	def realiza_get(self):
		self.codigo += "\n    SC  Read"
		self.pilha_geracao_semantica.pop()

	def realiza_return(self):
		self.codigo += "\n		LD  res\n		RS  " + self.pilha_geracao_semantica[-2]['nome_funcao']
		self.pilha_geracao_semantica.pop()

	def gera_codigo_print(self):
		self.codigo += "\n    SC  Print"
		self.pilha_geracao_semantica.pop()

	def declara_funcao(self):
		for par in self.pilha_geracao_semantica[-1]['parametros']:
			self.codigo_declaracoes_funcoes += "\n" + par
			for _ in range(len(par),8):
				self.codigo_declaracoes_funcoes += " "
			self.codigo_declaracoes_funcoes += "K   /0000"
		nome = self.pilha_geracao_semantica[-1]['nome_funcao']
		self.codigo_declaracoes_funcoes += "\n" + nome
		for _ in range(len(nome),8):
				self.codigo += " "
		self.codigo_declaracoes_funcoes += "K   /0000"
		self.codigo_declaracoes_funcoes += "\n          JP  F" + self.contador_funcoes
		self.codigo_declaracoes_funcoes += "\nres" + self.contador_funcoes + "    K   /0000" + self.contador_funcoes
		self.codigo_declaracoes_funcoes += "\nF" + self.contador_funcoes + "       +   K0"
		for par in self.pilha_geracao_semantica[-1]['parametros']:
			self.codigo_declaracoes_funcoes += "\n         SC  Pop"
			self.codigo_declaracoes_funcoes += "\n         MM  " + par
		self.contador_funcoes += 1
		self.pilha_geracao_semantica.pop()

	def prepara_bloco_if(self):
		self.codigo += "\nIF" + self.contador_condicoes + "     +   K0"

	def fecha_condicao_if(self):
		self.codigo += "\n        JZ  IF" + self.contador_condicoes + "1"
		self.codigo += "\n        JP  ELSE" + self.contador_condicoes
		self.codigo += "\n IF" + self.contador_condicoes + "1    +   K0"		

	def prepara_bloco_else(self):
		self.codigo += "\nELSE" + self.contador_condicoes + " 	+ 	K0"

	def finaliza_bloco_if(self):
		self.contador_condicoes += 1
		self.pilha_geracao_semantica.pop()

	def prepara_bloco_while(self):
		self.codigo += "\nLOOP" + self.contador_loops + "   +   K0"
	
	def fecha_condicao_while(self):
		self.codigo += "\n        JZ  L" + self.contador_loops + "AUX0"
		self.codigo += "\n        JP  L" + self.contador_loops + "END"
		self.codigo += "\nL" + self.contador_loops + "AUX0  +   K0"

	def finaliza_bloco_while(self):
		self.codigo += "\n        	JP 	LOOP" + self.contador_loops
		self.codigo += "\nL"+ self.contador_loops + "END        	+  	K0" + self.contador_loops
		self.contador_loops += 1
		self.pilha_geracao_semantica.pop()