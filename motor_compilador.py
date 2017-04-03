from minHeap import *
from motor_decomposicao import *
from analisador_lexico import *
from analisador_lexico_wirth import *
from pprint import pprint
from simula_automato import *

class MotorCompilador():
	def __init__(self, rastro, lista_inicial_eventos, texto_fonte, wirth = False, gera_ape = False):
		self.agora = 0
		self.rastro = rastro
		self.lista_eventos = lista_inicial_eventos
		self.codigo = {}
		self.codigo["texto_fonte"] = texto_fonte
		self.count = 0
		self.log = ""
		self.wirth = wirth
		if gera_ape:
			self.gera_ape = {}
			self.gera_ape["arquivo"] = "txts/APEs/saida_ape.txt"
			self.gera_ape["nome_submaquina"] = ""
			self.gera_ape["estado"] = 0
			self.gera_ape["contador"] = 1
			self.gera_ape["pilha"] = []
			self.gera_ape["transicoes"] = []
			self.gera_ape["alfabeto"] = []
			arquivo = open(self.gera_ape["arquivo"], "w")
			arquivo.write("")
			arquivo.close()
		else:
			self.gera_ape = gera_ape
								
	def inicia(self):
		fim = False
		while not fim:
			if self.lista_eventos.is_empty():
				fim = True
			else:
				fim = self.processa_evento(self.lista_eventos.serve())

	def processa_evento(self, evento):
		self.count += 1
		self.agora = evento[0]
		tipo_evento = evento[1]

		fim = False

		if tipo_evento == "DECOMPOSICAO":
			decomposicao_lista_inicial_eventos = MinHeap()
			horario = 0
			decomposicao_lista_inicial_eventos.append([horario, "LE_LINHA"])
			motor_decomposicao = MotorDecomposicao(decomposicao_lista_inicial_eventos, self.codigo["texto_fonte"])
			self.codigo["caracteres"] = motor_decomposicao.inicia()
			resultado = "gerado listagem de caracteres"
			self.log += "instante " + str(self.agora) + " chegada de evento DECOMPOSICAO " + resultado + "\n"

		elif tipo_evento == "ANALISE_LEXICA":
			if not self.wirth:
				analisador_lexico = AnalisadorLexico(self.codigo["caracteres"])
			else:
				analisador_lexico = AnalisadorLexicoWirth(self.codigo["caracteres"])
			resultado = analisador_lexico.inicia()
			self.codigo["atomos"] = resultado[0]
			self.codigo["tabela_de_simbolos"] = resultado[1]
			print(resultado)
			print("atomos")
			print(self.codigo["atomos"])

			resultado = "gerados os atomos"
			self.log += "instante " + str(self.agora) + " chegada de evento ANALISE_LEXICA " + resultado + "\n"

		elif tipo_evento == "ANALISE_SINTATICA":
			cadeia = []
			cadeia_valores = []
			for item in self.codigo["atomos"]:
				cadeia.append(item[0])
				cadeia_valores.append(item[1])
			cadeia.append("#")
			cadeia_valores.append("#")
			# print(cadeia)				
			# print(cadeia_valores)
			
			if self.wirth:
				automato = "txts/APEs/APE_wirth.txt"
				gera_semantica = False
			else:
				# automato = "txts/APEs/saida_ape.txt"
				automato = "txts/APEs/ape_gramatica.txt"
				gera_semantica = True
			estado_final, self.gera_ape = simula_automato(cadeia, automato, self.gera_ape, True, cadeia_valores, gera_semantica, self.codigo["tabela_de_simbolos"])

			if self.gera_ape: 
				resultado = "foi gerado o APE correspondente a gramática"
			else:
				if estado_final.aceitacao:
					resultado = "foi analisada a estrutura sintática do programa e ela foi aceita"
				else:
					resultado = "foi analisada a estrutura sintática do programa porém ela não foi aceita"
			self.log += "instante " + str(self.agora) + " chegada de evento ANALISE_SINTATICA " + resultado + "\n"

		# elif tipo_evento == "ANALISE_SEMANTICA":
		#	pass

		# elif tipo_evento == "GERA_CODIGO_INTERMEDIARIO":
		# 	pass

		# elif tipo_evento == "OTIMIZACAO_CODIGO_INTERMEDIARIO":
		# 	pass

		# elif tipo_evento == "GERA_CODIGO_OBJETO":
		# 	pass

		# elif tipo_evento == "OTIMIZACAO_CODIGO_OBJETO":
		# 	pass

		# elif tipo_evento == "GERA_CODIGO_MAQUINA":
		# 	pass

		# elif tipo_evento == "GERA_CODIGO_EXECUTAVEL":
		#	pass			

		elif tipo_evento == "FIM_SIMULACAO":
			self.gera_relatorio()
			self.gera_log()
			fim = True

		else:
			raise TypeError("Tipo inválido de evento")
		
		return fim
	
	def gera_log(self):
		if self.rastro:
			print(self.log)

	def gera_relatorio(self):
		print("Foram processados " + str(self.count) + " eventos, em " + str(self.agora) + " unidades de tempo.")