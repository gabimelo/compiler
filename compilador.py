from motor_compilador import *
from minHeap import *
	
def aciona_rastro(): 
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

def agenda_eventos():
	lista_eventos = MinHeap()
	horario = 0
	lista_eventos.append([horario, "DECOMPOSICAO"])
	horario += 1
	lista_eventos.append([horario, "ANALISE_LEXICA"])
	horario += 1
	lista_eventos.append([horario, "ANALISE_SINTATICA"])
	# horario += 1
	# lista_eventos.append([horario, "ANALISE_SEMANTICA"])
	# horario += 1
	# lista_eventos.append([horario, "GERA_CODIGO_INTERMEDIARIO"])
	# horario += 1
	# lista_eventos.append([horario, "OTIMIZACAO_CODIGO_INTERMEDIARIO"])
	# horario += 1
	# lista_eventos.append([horario, "GERA_CODIGO_OBJETO"])
	# horario += 1
	# lista_eventos.append([horario, "OTIMIZACAO_CODIGO_OBJETO"])
	# horario += 1
	# lista_eventos.append([horario, "GERA_CODIGO_MAQUINA"])
	# horario += 1
	# lista_eventos.append([horario, "GERA_CODIGO_EXECUTAVEL"])
	horario += 1
	lista_eventos.append([horario, "FIM_SIMULACAO"])
	return lista_eventos

def main(arquivo, wirth = False, gera_ape = False):
	arquivo_entrada = arquivo
	lista_eventos = agenda_eventos()
	# motor = MotorCompilador(aciona_rastro(), lista_eventos, arquivo_entrada)
	motor = MotorCompilador(True, lista_eventos, arquivo_entrada, wirth, gera_ape)
	motor.inicia()

if __name__ == "__main__":
	main('txts/texto_fonte.txt')
	# main('txts/texto_fonte2.txt')
	# main('txts/texto_fonte3.txt')
	# main('txts/texto_fonte4.txt')