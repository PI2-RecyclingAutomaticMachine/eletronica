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
GPIO.add_event_detect(35, GPIO.RISING)
GPIO.add_event_detect(37, GPIO.RISING)


out1 = 13 #MOTOR
out2 = 11 #MOTOR
out3 = 15 #MOTOR
out4 = 12 #MOTOR

GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)
GPIO.setup(32,GPIO.OUT) #buzzer
GPIO.setup(7,GPIO.OUT)
#saida pro node
garrafa = 0 #
hx = HX711(29, 31) #pinos balança

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

API_ENDPOINT_USER = "http://35.196.52.216/api/user/cpf"
API_ENDPOINT_BOTTLE = "http://35.196.52.216/api/bottle/label"
API_ENDPOINT_OPERATION = "http://35.196.52.216/api/user/"


#Variable global 
estado = 'i' 

#Estados ######################################################################
def EDOi(entrada): 
	global estado
	global mylcd
	print('Estado Inicial')
	mylcd.lcd_clear()
	mylcd.lcd_display_string("Iniciando Maquina...", 1)
	time.sleep(1)
	#Se tiver alguma configuração inicial colocar aqui
	estado = 0 

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
	global mylcd

	print('Estado 0') 

	if flag_usuario_nova_garrafa == 0:
		print ('Novo usuario. Apresente o QRcode.')
		mylcd.lcd_clear()
		mylcd.lcd_display_string(" Novo usuario.", 1)
		mylcd.lcd_display_string("Apresente o QRcode.", 2)
		garrafa_anterior = None
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
		print('%s vai inserir uma nova garrafa.' % (usuario['name']))
		mylcd.lcd_display_string(" %s, insira" %(usuario['name']), 1)
		mylcd.lcd_display_string("uma nova garrafa...", 2)

	if id_qr_code_string == None:
		mylcd.lcd_clear()
		print('ID_QR_CODE_STRING = None -> #ERROR#')
		mylcd.lcd_display_string("ERROR variavel id_qr", 1)
		time.sleep(1)
		mylcd.lcd_clear()
		estado = 0

	else:
		try:
			data_usuario = {"cpf" : id_qr_code_string}
			r = requests.post(url = API_ENDPOINT_USER, data = data_usuario)
			usuario = r.json()

			print('Seja bem vindo %s.' % (usuario['name']))
			mylcd.lcd_display_string(" Seja bem vindo!", 1)
			mylcd.lcd_display_string("Nome: %s" %(usuario['name']), 2)
			time.sleep(1)
			estado = 1

		except:
			mylcd.lcd_clear()
			print('Usuario nao cadastrado. Tente novamente.')
			mylcd.lcd_display_string(" Usuario nao cadas-", 1)
			mylcd.lcd_display_string("trado. Tente de novo", 2)
			time.sleep(1)
			mylcd.lcd_clear()

			estado = 0 
#Leitura do QR code da garrafa ################################################
def EDO1(entrada): 
	global estado
	global garrafa
	global mylcd
	print('Estado 1')
	mylcd.lcd_clear()
	print('Apresente o QRcode da garrafa.')
	mylcd.lcd_display_string(" Apresente o QRcode", 1)
	mylcd.lcd_display_string("da garrafa.", 2)

	qr_code_string = None
	GPIO.output(32, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(32, GPIO.LOW)

	qr_code_string = qr_code()

	GPIO.output(32, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(32, GPIO.LOW)
	mylcd.lcd_clear()
	GPIO.output(7,GPIO.LOW)
	try:
		if qr_code_string == None:
			mylcd.lcd_clear()
			print ("Nao foi possivel ler o QRcode da garrafa.")
			mylcd.lcd_display_string("Nao foi possível ler", 1)
			mylcd.lcd_display_string("o QRcode da garrafa.", 2)
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
		mylcd.lcd_display_string(" Garrafa invalida.", 1)
		mylcd.lcd_display_string("Tente novamente.", 2)
		estado = 1

#verifica se o compartimento ta cheio. ########################################
def EDO2(entrada): 
	global estado
	global mylcd
	print('Estado 2')
	mylcd.lcd_clear()
	print('Verificando se o compartimento de plastico está cheio...')
	mylcd.lcd_display_string(" Verificando se o ", 1)
	mylcd.lcd_display_string("compartimento de ", 2)
	mylcd.lcd_display_string("plastico esta cheio.", 3)  
	time.sleep(0.5)
	mylcd.lcd_clear()

	compartimento_plastico = verifica_compartimento(36)
    
	if compartimento_plastico == '0':
        	time.sleep(0.1)
        	if compartimento_plastico == '0':
            		estado = 15 #limpeza compartimento
			print ("Compartimento do plastico esta cheio. Realizar limpeza.")
			mylcd.lcd_display_string(" Compartimento do ", 1)
			mylcd.lcd_display_string("plastico esta cheio.", 2)
			mylcd.lcd_display_string(" Realizar limpeza.", 3)

	else:
		print ("Compartimento do plastico estavel.")
		mylcd.lcd_display_string(" Compartimento do ", 1)
		mylcd.lcd_display_string("plastico estavel.", 2)
		
		estado = 4

#verifica se o compartimento ta cheio. ########################################
def EDO3(entrada): 
	global estado
	global mylcd
	print ('Estado 3')
	mylcd.lcd_clear()
	print ('Verificando se o compartimento de vidro está cheio...')
	mylcd.lcd_display_string(" Verificando se o ", 1)
	mylcd.lcd_display_string("compartimento de ", 2)
	mylcd.lcd_display_string("vidro esta cheio.", 3)
	time.sleep(0.5)
	mylcd.lcd_clear()

	compartimento_vidro = verifica_compartimento(38)

	if compartimento_vidro == '0':
		time.sleep(0.1)
		if compartimento_vidro == '0':
			estado = 15 #limpeza compartimento
			print ("Compartimento do vidro está cheio. Realizar limpeza.")
			mylcd.lcd_display_string(" Compartimento do", 1)
			mylcd.lcd_display_string("vidro esta cheio.", 2)
			mylcd.lcd_display_string(" Realizar limpeza.", 3)

	else:
		print ("Compartimento do vidro estável.")
		mylcd.lcd_display_string(" Compartimento do ", 1)
		mylcd.lcd_display_string("vidro estavel.", 2)
		estado = 4

#abrindo a porta para inserir a garrafa #######################################
def EDO4(entrada): 
    	global estado
	global garrafa_anterior
	global hx
	global mylcd
    	print ('Estado 4')
	mylcd.lcd_clear()

	print('Realizando a calibração da balança...')
	mylcd.lcd_display_string("Calibrando balanca..", 1)
	time.sleep(0.1)

	hx.set_reading_format("LSB", "MSB")
	hx.set_reference_unit(433) #calibragem
	hx.reset()
	hx.tare()
	mylcd.lcd_clear()
	mylcd.lcd_display_string("Balanca calibrada!", 1)

	print ("Abrindo compartimento para inserir a garrafa.")
	mylcd.lcd_clear()	
	mylcd.lcd_display_string(" Abrindo comparti-", 1)
	mylcd.lcd_display_string("mento para inserir a", 2)
	mylcd.lcd_display_string("garrafa.", 3)
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
	global mylcd
	print ('Estado 5')
	mylcd.lcd_clear()

	print('Insira a Garrafa.')
	mylcd.lcd_display_string("Insira a Garrafa.", 1)
	time.sleep(2)
	peso_balanca = balanca()

	if (peso_balanca >= 10):
		estado = 6
    
	while (peso_balanca < 10):

		print ("Insira a Garrafa.")
		mylcd.lcd_clear()
		mylcd.lcd_display_string("Insira a Garrafa.", 1)
		peso_balanca = balanca()
		time.sleep(1)

	estado = 6
        
    
#Verificando se o usuário está com a mão na porta #############################
def EDO6(entrada): 
	global estado
	global mylcd
	print ('Estado 6')
	mylcd.lcd_clear()
    
	usuario_compartimento = verifica_compartimento(40)
	if usuario_compartimento == '0':
		print ("Retire a mão de dentro do compartimento.")
		mylcd.lcd_display_string(" Retire a mao de ", 1)
		mylcd.lcd_display_string("dentro do comparti-", 2)
		mylcd.lcd_display_string("mento.", 3)
		estado = 6

		while (usuario_compartimento == "0"):
			print ("Retire a mão de dentro do compartimento.")
			mylcd.lcd_clear()
			mylcd.lcd_display_string(" Retire a mao de ", 1)
			mylcd.lcd_display_string("dentro do comparti-", 2)
			mylcd.lcd_display_string("mento.", 3)
			usuario_compartimento = verifica_compartimento(40)

		else:
			mylcd.lcd_clear()
			print ("Usuário retirou a mão do compartimento.")
			mylcd.lcd_display_string(" Usuario retirou a", 1)
			mylcd.lcd_display_string("mao do compartimento", 2)
			estado = 7

	elif usuario_compartimento == '1':
		print ("Compartimento nao obstruido.")
		mylcd.lcd_display_string(" Compartimento nao ", 1)
		mylcd.lcd_display_string("obstruido.", 2)
		estado = 7

#Verificando peso #############################################################
def EDO7(entrada): 
	global estado
	global garrafa
	global mylcd
	print ('Estado 7')
	mylcd.lcd_clear()
    
	peso_balanca = balanca()
	if (peso_balanca >= (garrafa['weight'] - 10)) and (peso_balanca <= (garrafa['weight'] + 10)):
		print ("Peso da garrafa aprovado!")
		mylcd.lcd_display_string(" Peso da garrafa ", 1)
		mylcd.lcd_display_string("aprovado!!", 2)
		time.sleep(0.5)
		estado = 8
	else:
		print ("Problemas com o peso da Garrafa, por gentileza, retire a ÁGUA da garrafa.")
		mylcd.lcd_display_string("Problemas com o peso", 1)
		mylcd.lcd_display_string("da Garrafa, por gen-", 2)
		mylcd.lcd_display_string("tileza,retire a agua", 3)
		mylcd.lcd_display_string("da garrafa.", 4)
		time.sleep(1)
		mylcd.lcd_clear()

		print ("Retire a garrafa e insira corretamente.")

		mylcd.lcd_display_string(" Retire a garrafa e ", 1)
		mylcd.lcd_display_string("insira corretamente.", 2)
		time.sleep(3)
		estado = 12 #criar estado para o cara retirar a garrafa
            
#Verificando capacitivo #######################################################
def EDO8(entrada): 
	global estado
	global mylcd
	print ('Estado 8')
	mylcd.lcd_clear()
    	print ("Realizando a leitura do sensor capacitivo.")
	mylcd.lcd_display_string(" Leitura do sensor", 1)
	mylcd.lcd_display_string("capacitivo.", 2)

	material_garrafa_sensor = verifica_material()

	print('Material da Garrafa: %s' % (material_garrafa_sensor))
	mylcd.lcd_display_string("Material da Garrafa:", 1)
	mylcd.lcd_display_string("%s ." %(material_garrafa_sensor), 2)

	if material_garrafa_sensor == garrafa['material']:
		mylcd.lcd_clear()
		print ('Material da garrafa de acordo com o QRcode.')
		mylcd.lcd_display_string("Aprovado!!", 1)
		estado = 9
	else:
		print ('Conflito entre dados do QRcode (garrafa) e sensor capacitivo.')
		mylcd.lcd_clear()
		mylcd.lcd_display_string("Conflito entre dados", 1)
		mylcd.lcd_display_string("do QRcode (garrafa) ", 2)
		mylcd.lcd_display_string("e sensor capacitivo.", 3)
		estado = 12 #criar estado para o cara retirar a garrafa
             
#Empurrando garrafa pro inferno ###############################################
def EDO9(entrada): 
	global estado 
	global garrafa
	global garrafa_anterior
	global mylcd
	print ('Estado 9')
	mylcd.lcd_clear()
	print ('Direcionando a garrafa para o compartimento correto.')
	mylcd.lcd_display_string(" Direcionando a gar-", 1)
	mylcd.lcd_display_string("rafa para o compar-", 2)
	mylcd.lcd_display_string("timento correto.", 3)
    
	if garrafa['material'] == 'vidro':
		garrafa_anterior = 'vidro'
		motor(-4800)

		estado = 10
	elif garrafa['material'] == 'plastico':
		garrafa_anterior ='plastico'
		GPIO.output(7,GPIO.HIGH)
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
	global mylcd
	print ('Estado 10')
	mylcd.lcd_clear()

	array_garrafas.append(garrafa['id'])
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
	global mylcd
	print ('Estado 11')
	mylcd.lcd_clear()
	#GPIO.cleanup()

	print ("Deseja inserir mais uma garrafa?")
	mylcd.lcd_display_string(" Deseja inserir mais", 1)
	mylcd.lcd_display_string("garrafa? ", 2)
	time.sleep(2)
#	motor(-4800)
	try:
		if (GPIO.event_detected(35) == True) and (GPIO.event_detected(37) == False):
			repetir_id_qr_code_string = id_qr_code_string
			flag_usuario_nova_garrafa = 1
			estado = 1
			mylcd.lcd_clear()
			print('Pontuacao atual: %d . ' % (pontos))
			mylcd.lcd_display_string("Pontuacao atual: %d" %(pontos), 1) 
			time.sleep(0.3)


		elif (GPIO.event_detected(37) == True) and (GPIO.event_detected(35) == False):
			flag_usuario_nova_garrafa = 0
			estado = 0
			data_array_garrafas = {"bottles" : array_garrafas}
			url_operation = API_ENDPOINT_OPERATION + usuario['id'] + "/operation"
			#Se o qr_code_string for uma string ok, se não alterar
			r_operation = requests.post(url = url_operation, data = data_array_garrafas)
			mylcd.lcd_clear()
			print('Pontuação final: %d . ' % (pontos))
			mylcd.lcd_display_string("Pontuacao final: %d" %(pontos), 1)
			pontos = 0
			array_garrafas = []
			time.sleep(15)
		        GPIO.output(7,GPIO.LOW)

		else:
			estado = 11
        except:
		mylcd.lcd_clear()
		print ("Deseja inserir mais uma garrafa? ")
		mylcd.lcd_display_string(" Deseja inserir mais", 1)
		mylcd.lcd_display_string("garrafa? ", 2)
		estado = 11

#Retirar a garrafa, deu ruim ##################################################
def EDO12(entrada): 
	global estado
	global garrafa
	global garrafa_anterior
	global mylcd
	print ('Estado 12')

	mylcd.lcd_clear()
	print('Retire a Garrafa. Apresente o QRcode da garrafa ao Leitor novamente.')
	mylcd.lcd_display_string(" Retire a Garrafa.", 1)
	mylcd.lcd_display_string(" Apresente o QRcode ", 2)
	mylcd.lcd_display_string("da garrafa ao Leitor", 3)
	mylcd.lcd_display_string("novamente.", 4)

	peso_balanca = balanca()
	while (peso_balanca > 10):
		mylcd.lcd_clear()
		print ("Retire a garrafa.")
		mylcd.lcd_display_string("RETIRE A GARRAFA!", 1)
		peso_balanca = balanca()
		time.sleep(0.5)

	usuario_compartimento = verifica_compartimento(40)
	if usuario_compartimento == '0':
		print('Retire a mão do compartimento')
		mylcd.lcd_display_string(" Retire a mao do ", 1)
		mylcd.lcd_display_string("compartimento.", 2)

		while (usuario_compartimento == '0'):
			mylcd.lcd_clear()
			print('Retire a mão do compartimento')
			mylcd.lcd_display_string(" Retire a mao do ", 1)
			mylcd.lcd_display_string("compartimento.", 2)
			usuario_compartimento = verifica_compartimento(40)
			time.sleep(0.8)
		else:
			mylcd.lcd_clear()
			print('Usuário retirou a mão do compartimento')
			mylcd.lcd_display_string(" Usuario retirou a ", 1)
			mylcd.lcd_display_string("mao do comparitmento", 2)
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
	global mylcd
	print ('Estado 15')
	mylcd.lcd_clear()
	print ('Realizar limpeza do compartimento.')
	mylcd.lcd_display_string(" Realizar limpeza do", 1)
	mylcd.lcd_display_string("compartimento", 2)

	compartimento_plastico = verifica_compartimento(36)
    
	if compartimento_plastico == '0':
		time.sleep(1)
		if compartimento_plastico == '0':
			mylcd.lcd_clear()
			print ("Compartimento do plástico está cheio. Realizar limpeza")
			mylcd.lcd_display_string(" Compartimento do ", 1)
			mylcd.lcd_display_string("plastico esta cheio.", 2)
			mylcd.lcd_display_string("Realizar limpeza.", 3)
			estado = 2
	else:
		mylcd.lcd_clear()
		print ("Compartimento do plástico foi esvaziado.")
		mylcd.lcd_display_string(" Compartimento do ", 1)
		mylcd.lcd_display_string("plastico foi esvazi-", 2)
		mylcd.lcd_display_string("ado.", 3)
		time.sleep(0.5)
		mylcd.lcd_clear()
		estado = 4

	compartimento_vidro = verifica_compartimento(38)


	if compartimento_vidro == '0':
		time.sleep(1)
		if compartimento_vidro == '0':
			estado = 3
			mylcd.lcd_clear()
			print ("Compartimento do vidro está cheio. Realizar limpeza")
			mylcd.lcd_display_string(" Compartimento do ", 1)
			mylcd.lcd_display_string("vidro esta cheio.", 2)
			mylcd.lcd_display_string("Realizar limpeza.", 3)

	else:
		mylcd.lcd_clear()
		print ("Compartimento do vidro foi esvaziado.")
		mylcd.lcd_display_string(" Compartimento do ", 1)
		mylcd.lcd_display_string("vidro foi esvaziado.", 2)
		time.sleep(0.5)
		mylcd.lcd_clear()
		estado = 4

def FSM(entrada):
    global repetir_id_qr_code_string
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
