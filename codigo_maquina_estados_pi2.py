#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from sys import argv
import zbar

from time import *
from time import sleep 
from random import randint 
import sys
import lcddriver
import RPi.GPIO as GPIO
import time
import requests
from hx711 import HX711

mylcd = lcddriver.lcd()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(36, GPIO.IN) #PLASTICO
GPIO.setup(38, GPIO.IN) #VIDRO
GPIO.setup(40, GPIO.IN) #MÃO
GPIO.setup(16, GPIO.IN) #CAPACITIVO1
GPIO.setup(18, GPIO.IN) #CAPACITIVO2
GPIO.setup(35, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #botao sim
GPIO.setup(37, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #botao nao
#GPIO.add_event_detect(35, GPIO.RISING)
#GPIO.add_event_detect(37, GPIO.RISING)

out1 = 13 #MOTOR
out2 = 11 #MOTOR
out3 = 15 #MOTOR
out4 = 12 #MOTOR

GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)
GPIO.setup(32,GPIO.OUT) #buzzer
GPIO.setup(19,GPIO.OUT) #ligar motor
GPIO.setup(21,GPIO.OUT) #ligar motor
GPIO.setup(22,GPIO.OUT) #desligar motor
GPIO.setup(24,GPIO.OUT) #desligar motor
#saida pro node
garrafa = 0 #
hx = HX711(29, 31) #pinos balança

def remover_evento(pino1, pino2):
	GPIO.remove_event_detect(pino1)
	time.sleep(1)
	GPIO.remove_event_detect(pino2)
	

def qr_code():
    #sys.stdout = open ("data.txt", "a")
    # create a Processor
    proc = zbar.Processor()

    # configure the Processor
    proc.parse_config('enable')

    # initialize the Processor
    device = '/dev/video0'
    if len(argv) > 1:
        device = argv[1]
    proc.init(device)

    # enable the preview window
    proc.visible = True

    # read at least one barcode (or until window closed)
    proc.process_one()

    # hide the preview window
    proc.visible = False
    # extract results

    for symbol in proc.results:
        # do something useful with results
        # print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        # print ('%s' % symbol.data)
        #mylcd.lcd_display_string("%s %%" % symbol.data)

        data = symbol.data 
    
    if data is not None:
        return data 
    else:
        print('QRcode não existe')

def verifica_compartimento(pino):
    if GPIO.input(pino) == False:
        print("Compartimento obstruído") 
        data = "0"
    else:
        data = "1"
    return data


#Sensor capacitivo atuando para verificar o material da garrafa.
def verifica_material():
	#pinos 16 e 18
	if (GPIO.input(16) == False) or (GPIO.input(18) == False):
		material = "vidro"

	else:
		material = "plastico"

	return material


def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

def balanca():
    global hx

    contador = 0
    while (contador <= 1):
        try:
            contador +=1
            val = hx.get_weight(5)
            print (val)

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

    return val


    
def motor(x):

    global out1 #= 13
    global out2 #= 11
    global out3 #= 15
    global out4 #= 12

    i=0
    positive=0
    negative=0
    y=0

    #print ("First calibrate by giving some +ve and -ve values.....")


    try:
         # GPIO.output(out1,GPIO.LOW)
         # GPIO.output(out2,GPIO.LOW)
         # GPIO.output(out3,GPIO.LOW)
         # GPIO.output(out4,GPIO.LOW)
          if x>0 and x<=10000:
              for y in range(x,0,-1):
                  if negative==1:
                      if i==7:
                          i=0
                      else:
                          i=i+1
                      y=y+2
                      negative=0
                  positive=1
                  #print((x+1)-y)
                  if i==0:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==1:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==2:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==3:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==4:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==5:
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==6:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==7:    
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  if i==7:
                      i=0
                      continue
                  i=i+1
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              return None

          elif x<0 and x>=-10000:
              x=x*-1
              for y in range(x,0,-1):
                  if positive==1:
                      if i==0:
                          i=7
                      else:
                          i=i-1
                      y=y+3
                      positive=0
                  negative=1
                  #print((x+1)-y) 
                  if i==0:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==1:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==2:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==3:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==4:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==5:
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==6:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  elif i==7:    
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0005)
                      #time.sleep(1)
                  if i==0:
                      i=7
                      continue
                  i=i-1 
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              return None

                  
    except KeyboardInterrupt:
        GPIO.cleanup()


repetir_id_qr_code_string = None 
flag_usuario_nova_garrafa = 0
id_qr_code_string = None
usuario = None
pontos = 0
garrafa_anterior = None
array_garrafas = []
flag_desligar_motor = 1

API_ENDPOINT_USER = "http://35.196.52.216/api/user/cpf"
API_ENDPOINT_BOTTLE = "http://35.196.52.216/api/bottle/label"
API_ENDPOINT_OPERATION = "http://35.196.52.216/api/user/"


#Variable global 
estado = 'i' 

#Estados ######################################################################
def EDOi(entrada):
	GPIO.output(19,GPIO.HIGH)
	GPIO.output(21,GPIO.HIGH)
	GPIO.output(22,GPIO.HIGH)
	GPIO.output(24,GPIO.HIGH) 
	global estado
	#global mylcd
	print('Estado Inicial')
	mylcd.lcd_clear()
	time.sleep(0.5)
	mylcd.lcd_display_string("Iniciando...",1)
	time.sleep(1)
	#Se tiver alguma configuração inicial colocar aqui
	estado = 0 
	garrafa_anterior = None

#Leitura do QR code do usuário ################################################
def EDO0(entrada): 
	global estado 
	global repetir_id_qr_code_string
	global flag_usuario_nova_garrafa
	global usuario
	global pontos
	global garrafa_anterior
	global id_qr_code_string
	global array_garrafas
	#global mylcd

	print('Estado 0') 

	if flag_usuario_nova_garrafa == 0:
		print ('Novo usuario. Apresente o QRcode.')

		mylcd.lcd_clear()
		time.sleep(0.5)
		mylcd.lcd_display_string("Novo usuario.",1)

		time.sleep(1)
		mylcd.lcd_clear()
		time.sleep(0.5)

		mylcd.lcd_display_string("Insira o QRcode",1)
		mylcd.lcd_display_string("do usuario.",2)
		pontos = 0

		array_garrafas = []

		id_qr_code_string = None
		GPIO.output(32, GPIO.HIGH)
		time.sleep(0.5)
                GPIO.output(32, GPIO.LOW)

		id_qr_code_string = qr_code()

                GPIO.output(32, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(32, GPIO.LOW)
		mylcd.lcd_clear()

	elif flag_usuario_nova_garrafa == 1:
		id_qr_code_string = repetir_id_qr_code_string
		mylcd.lcd_clear()
		time.sleep(0.5)
		print('%s vai inserir uma nova garrafa.' % (usuario['name']))
		mylcd.lcd_display_string("%s," %(usuario['name']),1)
		mylcd.lcd_display_string("insira garrafa..",2)

	if id_qr_code_string == None:
		print('ID_QR_CODE_STRING = None -> #ERROR#')
		estado = 0


	else:
		try:
			data_usuario = {"cpf" : id_qr_code_string}
			r = requests.post(url = API_ENDPOINT_USER, data = data_usuario)
			usuario = r.json()
			mylcd.lcd_clear()
			time.sleep(0.5)
			print('Seja bem vindo %s.' % (usuario['name']))
			mylcd.lcd_display_string("Seja bem vindo!",1)
			mylcd.lcd_display_string("Nome: %s" %(usuario['name']),2)
			time.sleep(1)
			estado = 1

		except:
			mylcd.lcd_clear()
			time.sleep(0.5)
			print('Usuario nao cadastrado. Tente novamente.')
			mylcd.lcd_display_string("Usuario nao",1)
			mylcd.lcd_display_string("cadastrado.",2)
			time.sleep(1)

			estado = 0 
#Leitura do QR code da garrafa ################################################
def EDO1(entrada): 
	global estado
	global garrafa
	global flag_desligar_motor
	global garrafa_anterior
	#global mylcd
	print('Estado 1')

	mylcd.lcd_clear()
	time.sleep(0.5)
	print('Apresente o QRcode da garrafa.')
	mylcd.lcd_display_string("Insira o QRcode",1)
	mylcd.lcd_display_string("da garrafa.",2)

	qr_code_string = None
	GPIO.output(32, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(32, GPIO.LOW)

	qr_code_string = qr_code()

	GPIO.output(32, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(32, GPIO.LOW)
	mylcd.lcd_clear()

	if flag_desligar_motor == 0:
		if garrafa_anterior == 'plastico':
			GPIO.output(19,GPIO.HIGH) #rotina para desligar motor e acionar freio.
			GPIO.output(21,GPIO.HIGH) #desligar motor
			time.sleep(0.2)
			GPIO.output(22,GPIO.LOW) #freio
			GPIO.output(24,GPIO.LOW)
			time.sleep(1)
			GPIO.output(22,GPIO.HIGH)
			GPIO.output(24,GPIO.HIGH)

	try:
		if qr_code_string == None:
			print ("Nao foi possivel ler o QRcode da garrafa.")
			mylcd.lcd_display_string("Erro na leitura",1)
			mylcd.lcd_display_string("QRcode garrafa.",2)
			time.sleep(0.5)
			estado = 1
		else:
			data_garrafa = {"label" : qr_code_string}
			#Se o qr_code_string for uma string ok, se não alterar
			rg = requests.post(url = API_ENDPOINT_BOTTLE, data = data_garrafa)
			garrafa = rg.json()

			if garrafa['material'] == 'plastico':
        			estado = 2
    
			elif garrafa['material'] == 'vidro':
        			estado = 3

	except:
		print('Garrafa invalida. Tente novamente.')
		time.sleep(0.5)
		mylcd.lcd_display_string("Garrafa invalida",1)
		mylcd.lcd_display_string("Tente novamente.",2)
		estado = 1

#verifica se o compartimento ta cheio. ########################################
def EDO2(entrada): 
	global estado
	#global mylcd
	print('Estado 2')
	mylcd.lcd_clear()
	print('Verificando se o compartimento de plastico está cheio...')
	time.sleep(0.5)
	mylcd.lcd_display_string("Aguarde...",1)


	compartimento_plastico = verifica_compartimento(36)
    
	if compartimento_plastico == '0':
        	time.sleep(0.1)
        	if compartimento_plastico == '0':
            		estado = 15 #limpeza compartimento
			print ("Compartimento do plastico esta cheio. Realizar limpeza.")
			mylcd.lcd_clear()
			time.sleep(0.5)
			mylcd.lcd_display_string("Limpar compart.",1)
			mylcd.lcd_display_string("de plastico.",2)

	else:
		print ("Compartimento do plastico estavel.")
		
		estado = 4

#verifica se o compartimento ta cheio. ########################################
def EDO3(entrada): 
	global estado
	#global mylcd
	print ('Estado 3')
	mylcd.lcd_clear()
	time.sleep(0.5)
	print ('Verificando se o compartimento de vidro está cheio...')
	mylcd.lcd_display_string("Aguarde...",1)


	compartimento_vidro = verifica_compartimento(38)

	if compartimento_vidro == '0':
		time.sleep(0.1)
		if compartimento_vidro == '0':
			estado = 15 #limpeza compartimento
			mylcd.lcd_clear()
			time.sleep(0.5)
			print ("Compartimento do vidro está cheio. Realizar limpeza.")
			mylcd.lcd_display_string("Limpar compart.",1)
			mylcd.lcd_display_string("de vidro.",2)


	else:
		print ("Compartimento do vidro estável.")

		estado = 4

#abrindo a porta para inserir a garrafa #######################################
def EDO4(entrada): 
    	global estado
	global garrafa_anterior
	global hx
	#global mylcd
    	print ('Estado 4')
	mylcd.lcd_clear()
	time.sleep(0.5)

	print('Realizando a calibração da balança...')
	mylcd.lcd_display_string("Aguarde..",1)

	hx.set_reading_format("LSB", "MSB")
	hx.set_reference_unit(435) #calibragem(anterior433)
	hx.reset()
	hx.tare()

	print ("Abrindo compartimento para inserir a garrafa.")

	time.sleep(0.5)	
	if garrafa_anterior == 'plastico':
		motor(-4800)
	elif garrafa_anterior == 'vidro':
		motor(4800)
	else:
		motor(-4800)
	estado = 5

#Verificando se a garrafa foi inserida ########################################
def EDO5(entrada): 
	global estado
	#global mylcd
	print ('Estado 5')
	mylcd.lcd_clear()
	time.sleep(0.5)
	print('Insira a Garrafa.')
	mylcd.lcd_display_string("Insira a Garrafa.", 1)
	time.sleep(2)
	peso_balanca = balanca()

	if (peso_balanca >= 10):
		estado = 6
    
	while (peso_balanca < 10):

		print ("Insira a Garrafa.")
		peso_balanca = balanca()
		time.sleep(1)

	estado = 6
        
    
#Verificando se o usuário está com a mão na porta #############################
def EDO6(entrada): 
	global estado
	#global mylcd
	print ('Estado 6')
	mylcd.lcd_clear()
    
	usuario_compartimento = verifica_compartimento(40)
	if usuario_compartimento == '0':
		print ("Retire a mão de dentro do compartimento.")
		time.sleep(0.5)
		mylcd.lcd_display_string("Retire a mao do ",1)
		mylcd.lcd_display_string("compartimento.",2)

		estado = 6

		while (usuario_compartimento == "0"):
			print ("Retire a mão de dentro do compartimento.")
			time.sleep(0.5)
			usuario_compartimento = verifica_compartimento(40)

		else:
			mylcd.lcd_clear()
			time.sleep(0.5)
			print ("Usuário retirou a mão do compartimento.")
			mylcd.lcd_display_string("Aguarde...",1)

			estado = 7

	elif usuario_compartimento == '1':
		print ("Compartimento nao obstruido.")
		mylcd.lcd_display_string("Aguarde...",1)

		estado = 7

#Verificando peso #############################################################
def EDO7(entrada): 
	global estado
	global garrafa
	#global mylcd
	print ('Estado 7')
	mylcd.lcd_clear()
    
	peso_balanca = balanca()
	if (peso_balanca >= (garrafa['weight'] - 10)) and (peso_balanca <= (garrafa['weight'] + 10)):
		print ("Peso da garrafa aprovado!")
		time.sleep(0.5)
		mylcd.lcd_display_string("Peso da garrafa",1)
		mylcd.lcd_display_string("aprovado!!",2)
		estado = 8
	else:
		print ("Problemas com o peso da Garrafa, por gentileza, retire a ÁGUA da garrafa.")
		time.sleep(0.5)
		mylcd.lcd_display_string("Problemas com o",1)
		mylcd.lcd_display_string("peso da Garrafa.",2)

		time.sleep(1)
		mylcd.lcd_clear()
		time.sleep(0.5)

		print ("Retire a garrafa e insira corretamente.")

		mylcd.lcd_display_string("Retire a garrafa",1)
		mylcd.lcd_display_string("e insira de novo",2)
		time.sleep(3)
		estado = 12 #criar estado para o cara retirar a garrafa
            
#Verificando capacitivo #######################################################
def EDO8(entrada): 
	global estado
	#global mylcd
	print ('Estado 8')
	mylcd.lcd_clear()
	time.sleep(0.5)
    	print ("Realizando a leitura do sensor capacitivo.")
	mylcd.lcd_display_string("Validando o ",1)
	mylcd.lcd_display_string("material garrafa",2)
	time.sleep(0.5)
	mylcd.lcd_clear()
	time.sleep(0.5)
	material_garrafa_sensor = verifica_material()

	print('Material da Garrafa: %s' % (material_garrafa_sensor))
	mylcd.lcd_display_string("Material garrafa:",1)
	mylcd.lcd_display_string("%s ." %(material_garrafa_sensor),2)

	if material_garrafa_sensor == garrafa['material']:
		mylcd.lcd_clear()
		time.sleep(0.5)
		print ('Material da garrafa de acordo com o QRcode.')
		mylcd.lcd_display_string("Aprovado!!",1)
		estado = 9
	else:
		print ('Conflito entre dados do QRcode (garrafa) e sensor capacitivo.')
		mylcd.lcd_clear()
		time.sleep(0.5)
		mylcd.lcd_display_string("Problemas com",1)
		mylcd.lcd_display_string("material garrafa",2)

		estado = 12 #criar estado para o cara retirar a garrafa
             
#Empurrando garrafa pro inferno ###############################################
def EDO9(entrada): 
	global estado 
	global garrafa
	global garrafa_anterior
	#global mylcd
	print ('Estado 9')
	mylcd.lcd_clear()
	time.sleep(0.5)
	print ('Direcionando a garrafa para o compartimento correto.')
	mylcd.lcd_display_string("Direcionando",1)
	mylcd.lcd_display_string("garrafa...",2)

    
	if garrafa['material'] == 'vidro':
		garrafa_anterior = 'vidro'
		motor(-4800)

		estado = 10
	elif garrafa['material'] == 'plastico':
		garrafa_anterior = 'plastico'
		GPIO.output(19,GPIO.LOW)
		GPIO.output(21,GPIO.LOW)
		motor(4800)
		estado = 10
	else:
		print ("ERROR")

#Pontuar para o usuário #######################################################
def EDO10(entrada):
	global estado 
	global pontos
	global garrafa
	global array_garrafas
	#global mylcd
	print ('Estado 10')
	time.sleep(0.2)
	mylcd.lcd_clear()
	
	#GPIO.add_event_detect(35, GPIO.RISING, bouncetime=200)
	#time.sleep(1)
	#GPIO.add_event_detect(37, GPIO.RISING, bouncetime=200)

	array_garrafas.append(str(garrafa['id']))
	print(array_garrafas)
	if garrafa['material'] == 'vidro': 
		pontos = pontos + 2
	if garrafa['material'] == 'plastico':
		pontos = pontos + 1
    
	estado = 11
            
#Verificando se o usuário que inserir mais garrafas ###########################
def EDO11(entrada): 
	global estado 
	global repetir_id_qr_code_string
	global id_qr_code_string
	global flag_usuario_nova_garrafa
	global pontos
	global array_garrafas
	global usuario
	global garrafa
	global flag_desligar_motor
	#global mylcd

	print ('Estado 11')
	mylcd.lcd_clear()
	time.sleep(0.5)
	print ("Deseja inserir mais uma garrafa?")
	mylcd.lcd_display_string("Deseja inserir",1)
	mylcd.lcd_display_string("nova garrafa?",2)

	try:
		if GPIO.input(35) == 1:
			repetir_id_qr_code_string = id_qr_code_string
			flag_usuario_nova_garrafa = 1
			estado = 1
			mylcd.lcd_clear()
			time.sleep(0.5)
			print('Pontuacao atual: %d . ' % (pontos))
			mylcd.lcd_display_string("Pontuacao atual:",1) 
			mylcd.lcd_display_string("%d" %(pontos),2)
			time.sleep(0.3)
			flag_desligar_motor = 0
			#remover_evento(35, 37)

		elif GPIO.input(37) == True:
			flag_usuario_nova_garrafa = 0
			estado = 0
			data_array_garrafas = {"bottles" : array_garrafas}
			url_operation = API_ENDPOINT_OPERATION + usuario['id'] + "/operation"
			#Se o qr_code_string for uma string ok, se não alterar
			print(url_operation)
			r_operation = requests.post(url = url_operation, data = data_array_garrafas)
			mylcd.lcd_clear()
			time.sleep(0.5)
			print('Pontuação final: %d . ' % (pontos))
			mylcd.lcd_display_string("Pontuacao final:",1)
			mylcd.lcd_display_string("%d" %(pontos),2)
			pontos = 0
			array_garrafas = []
			if garrafa['material'] == 'plastico':
				flag_desligar_motor = 1
				time.sleep(15)
				GPIO.output(19,GPIO.HIGH)
				GPIO.output(21,GPIO.HIGH)
				time.sleep(0.2)
				GPIO.output(22,GPIO.LOW)
				GPIO.output(24,GPIO.LOW)
				time.sleep(1)
				GPIO.output(22,GPIO.HIGH)
				GPIO.output(24,GPIO.HIGH)
				#remover_evento(35, 37)
			else:
				print('Garrrafa de vidro. Não precisa desligar o triturador.')

		else:
			estado = 11
        except:

		estado = 11

#Retirar a garrafa, deu ruim ##################################################
def EDO12(entrada): 
	global estado
	global garrafa
	global garrafa_anterior
	#global mylcd
	global garrafa_anterior
	print ('Estado 12')

	mylcd.lcd_clear()
	time.sleep(0.5)
	print('Retire a Garrafa. Apresente o QRcode da garrafa ao Leitor novamente.')
	mylcd.lcd_display_string("Retire a Garrafa", 1)
	garrafa_anterior = 'plastico'

	peso_balanca = balanca()
	while (peso_balanca > 10):
		print ("Retire a garrafa.")
		peso_balanca = balanca()
		time.sleep(0.5)


	usuario_compartimento = verifica_compartimento(40)
	if usuario_compartimento == '0':
		print('Retire a mão do compartimento')
		mylcd.lcd_clear()
		time.sleep(0.5)
		mylcd.lcd_display_string("Retire a mao do",1)
		mylcd.lcd_display_string("compartimento.",2)

		while (usuario_compartimento == '0'):
			print('Retire a mão do compartimento')
			usuario_compartimento = verifica_compartimento(40)
			time.sleep(0.8)
		else:
			mylcd.lcd_clear()
			time.sleep(0.5)
			print('Usuário retirou a mão do compartimento')
			mylcd.lcd_display_string("Usuario retirou",1)
			mylcd.lcd_display_string("a mao do comp.",2)
			estado = 1
			motor(4800)
	else:
		estado = 1 
		motor(4800)

#Verificando se o usuário está com a mão na porta #############################
def EDO13(entrada): 
	global estado 
	print ('Estado 13')
    
	usuario_compartimento = verifica_compartimento(40)
	if usuario_compartimento == '0':
		print ("Retire a mao dai porra.")
		estado = 13

		while (usuario_compartimento == "0"):
			print ("Retire a mao do compartimento, por gentileza.")
			usuario_compartimento = verifica_compartimento(40)
			estado = 13

		else:
			print ("Usuário retirou a mão do compartimento, pode seguir em frente.")
			estado = 14

	elif usuario_compartimento == '1':
		print ("Fechar compartimento.")
		estado = 14
            
#Fechando a porta #############################################################
def EDO14(entrada): 
	global estado
	print ('Estado 14')
	estado = 11 #verificar se o usuário quer inserir mais garrafas
	print ("Não vai cair aqui.")
#	motor(-4800)

def EDO15(entrada): 
	global estado
	#global mylcd
	print ('Estado 15')
	mylcd.lcd_clear()
	time.sleep(0.5)
	print ('Realizar limpeza do compartimento.')
	mylcd.lcd_display_string("Realizar limpeza",1)
	mylcd.lcd_display_string("do compartimento",2)

	compartimento_plastico = verifica_compartimento(36)
    
	if compartimento_plastico == '0':
		time.sleep(1)
		if compartimento_plastico == '0':
			mylcd.lcd_clear()
			time.sleep(0.5)
			print ("Compartimento do plástico está cheio. Realizar limpeza")
			mylcd.lcd_display_string("Limpar compart.",1)
			mylcd.lcd_display_string("do plastico,",2)

			estado = 2
	else:
		mylcd.lcd_clear()
		time.sleep(0.5)
		print ("Compartimento do plástico foi esvaziado.")
		mylcd.lcd_display_string("Aguarde...",1)

		estado = 4

	compartimento_vidro = verifica_compartimento(38)


	if compartimento_vidro == '0':
		time.sleep(1)
		if compartimento_vidro == '0':
			estado = 3
			mylcd.lcd_clear()
			time.sleep(0.5)
			print ("Compartimento do vidro está cheio. Realizar limpeza")
			mylcd.lcd_display_string("Limpar compart.",1)
			mylcd.lcd_display_string("do vidro.",2)


	else:
		mylcd.lcd_clear()
		time.sleep(0.5)
		print ("Compartimento do vidro foi esvaziado.")
		mylcd.lcd_display_string("Aguarde...",1)

		estado = 4

def FSM(entrada):

    API_ENDPOINT_USER = "http://35.196.52.216/api/user/cpf"
    API_ENDPOINT_BOTTLE = "http://35.196.52.216/api/bottle/label"


    global estado 
    switch = { 
       'i':EDOi, 
        0 :EDO0, 
        1 :EDO1, 
        2 :EDO2,
        3 :EDO3, 
        4 :EDO4, 
        5 :EDO5,
        6 :EDO6, 
        7 :EDO7, 
        8 :EDO8,
        9 :EDO9, 
        10 :EDO10,
        11 :EDO11,
        12 :EDO12,
        13 :EDO13,
        14 :EDO14,
        15 :EDO15
    } 
    func = switch.get(estado, lambda: None) 
    return func(entrada) 

#Programa Principal 
while True:     
 FSM(randint(0,1)) 
 sleep(2)
