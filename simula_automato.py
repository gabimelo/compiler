from motor_automato import *
from automato import *
from minHeap import *
from automato_finito import *
from automato_de_pilha import *
from maquina_de_turing import *
	
def acionaRastro(): 
	rastro = "?"
	while rastro == "?": 
		rastro = input("Deseja acionar a função de rastro? (s/n) ")
		if rastro == "s":
			rastro = True
		elif rastro == "n":
			rastro = False
		else:
			print("Opções para rastro: s ou n")
	return rastro

def leEspecificacaoDispositivo(nome_arquivo_dispositivo):
	arquivoMaquina = open(nome_arquivo_dispositivo)
	inicio = arquivoMaquina.readline().rstrip('\n')
	automatos = []

	while inicio == "##":
		tipoAutomato = arquivoMaquina.readline().rstrip('\n')
		if len(automatos)>0:
			nomeMaquina = arquivoMaquina.readline().rstrip('\n')
			automatos.append(iniciaAutomato(tipoAutomato))
			automatos[0].submaquinas[nomeMaquina] = automatos[-1]
		else:
			automatos.append(iniciaAutomato(tipoAutomato))

		estados = arquivoMaquina.readline().rstrip('\n').split(",")
		for estado in estados:
			automatos[-1].adicionaEstado(estado, Estado(estado))

		simbolos = arquivoMaquina.readline().rstrip('\n').split("@")
		for simbolo in simbolos:
			automatos[-1].adicionaSimbolo(simbolo)

		transicao = arquivoMaquina.readline().rstrip('\n')
		while transicao != "#":
			transicao = transicao.split("@")
			origem = transicao[0]
			simbolo = transicao[1]
			if simbolo not in automatos[-1].simbolos and simbolo != "#" and simbolo != "E":
				raise ValueError("Um símbolo dado não está no alfabeto aceito pela máquina")
			if len(transicao) == 4:
				destino = [transicao[2][1:],transicao[3][:-1]]
			else:
				destino = [transicao[2]]
			automatos[-1].adicionaTransicao(origem, simbolo, destino)
			transicao = arquivoMaquina.readline().rstrip('\n')

		inicial = arquivoMaquina.readline().rstrip('\n')
		automatos[-1].estados[inicial].inicial = True

		final = arquivoMaquina.readline().rstrip('\n')
		final = final.split(",")
		for estado in final:
			automatos[-1].estados[estado].aceitacao = True

		inicio = arquivoMaquina.readline().rstrip('\n')

	return automatos[0]

def iniciaAutomato(tipoAutomato):
	if tipoAutomato == "AF":
		automato = AutomatoFinito();
	elif tipoAutomato == "APE":
		automato = AutomatoDePilha();
	elif tipoAutomato == "MT":
		automato = MaquinaDeTuring();
	else:
		raise TypeError("Tipo inválido de autômato " + tipoAutomato)
	return automato

def leCadeiaEntrada(nome_arquivo_cadeia):
	arquivoCadeia = open(nome_arquivo_cadeia)
	return arquivoCadeia.readline().rstrip('\n')

def agendaEventos(cadeia, automato):
	listaEventos = MinHeap()
	horario = 0
	listaEventos.append([horario, "partidaInicial"])
	horario += 1
	listaEventos.append([horario, "leSimbolo"])
	horario += 1
	for _ in range(len(cadeia) - 1):
		if type(automato) is AutomatoFinito or type(automato) is AutomatoDePilha:
			listaEventos.append([horario, "movimentoCabecote"])
			horario += 1
			listaEventos.append([horario, "leSimbolo"])
			horario += 1
		elif type(automato) is MaquinaDeTuring:
			listaEventos.append([horario, "leSimbolo"])
	return listaEventos

def simula_automato_cadeia_em_arquivo(nome_arquivo_cadeia, nome_arquivo_dispositivo, gera_ape = False, rastro = True, cadeia_valores = False):
	dispositivo = leEspecificacaoDispositivo(nome_arquivo_dispositivo)
	cadeia = leCadeiaEntrada(nome_arquivo_cadeia)

	listaEventos = agendaEventos(cadeia, dispositivo)

	motor = MotorAutomato(rastro, listaEventos, dispositivo, cadeia, gera_ape, cadeia_valores)

	return motor.inicia()

def simula_automato(cadeia, nome_arquivo_dispositivo, gera_ape = False, rastro = True, cadeia_valores = False, gera_semantica = False, tabela_simbolos = []):
	dispositivo = leEspecificacaoDispositivo(nome_arquivo_dispositivo)

	listaEventos = agendaEventos(cadeia, dispositivo)

	motor = MotorAutomato(rastro, listaEventos, dispositivo, cadeia, gera_ape, cadeia_valores, gera_semantica, tabela_simbolos)

	return motor.inicia()

if __name__ == "__main__":
	# simula_automato_cadeia_em_arquivo('txts/cadeia.txt', 'txts/maquinas/ape1.txt')