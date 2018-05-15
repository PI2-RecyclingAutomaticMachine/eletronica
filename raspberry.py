from time import sleep 
from random import randint 
from sys import argv
import zbar
import sys
import I2C_LCD_driver
import RPi.GPIO as GPIO
import time
import requests
from hx711 import HX711
from time import *

mylcd = I2C_LCD_driver.lcd() 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN) #pino verifica compartimento plastico
GPIO.setup(13, GPIO.IN) #pino verifica compartimento vidro
GPIO.setup(15, GPIO.IN) #pino sensor capacitivo 1
GPIO.setup(19, GPIO.IN) #pino sensor capacitivo 2


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
        print("CUIDADO") 
        data = "0"
    else:
        data = "1"
    return data


#Sensor capacitivo atuando para verificar o material da garrafa.
def verifica_material():
    #pinos 15 e 19
    if GPIO.input(15) == True and GPIO.input(19) == True:
        material = "plastico"

    elif GPIO.input(15) == True and GPIO.input(19) == False:
        material = "vidro"

    else:
        material = "ERRO"
    return material

 

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

def balanca():
    hx = HX711(5, 6)

    hx.set_reading_format("LSB", "MSB")

    hx.set_reference_unit(92) #calibragem

    hx.reset()
    hx.tare()

    while True:
        try:
            val = hx.get_weight(5)
            print val

            hx.power_down()
            hx.power_up()
            time.sleep(0.5)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

    return val


    
def motor(x):

    out1 = 13
    out2 = 11
    out3 = 15
    out4 = 12

    i=0
    positive=0
    negative=0
    y=0



    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(out1,GPIO.OUT)
    GPIO.setup(out2,GPIO.OUT)
    GPIO.setup(out3,GPIO.OUT)
    GPIO.setup(out4,GPIO.OUT)

    print "First calibrate by giving some +ve and -ve values....."


    try:
       while(1):
          GPIO.output(out1,GPIO.LOW)
          GPIO.output(out2,GPIO.LOW)
          GPIO.output(out3,GPIO.LOW)
          GPIO.output(out4,GPIO.LOW)
          x = input()
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
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==1:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==2:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==3:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==4:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==5:
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==6:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==7:    
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  if i==7:
                      i=0
                      continue
                  i=i+1
          
          
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
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==1:
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==2:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==3:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.HIGH)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==4:  
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.LOW)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==5:
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.HIGH)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==6:    
                      GPIO.output(out1,GPIO.LOW)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  elif i==7:    
                      GPIO.output(out1,GPIO.HIGH)
                      GPIO.output(out2,GPIO.LOW)
                      GPIO.output(out3,GPIO.LOW)
                      GPIO.output(out4,GPIO.HIGH)
                      time.sleep(0.0007)
                      #time.sleep(1)
                  if i==0:
                      i=7
                      continue
                  i=i-1 

                  
    except KeyboardInterrupt:
        GPIO.cleanup()


repetir_id_qr_code_string = None 

#Finite State Machine (FSM)    
def FSM(entrada):
    global repetir_id_qr_code_string
    API_ENDPOINT = "URL_GALERA_SOFTWARE_NAO_PASSOU_AINDA"

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
    } 
    func = switch.get(estado, lambda: None) 
    return func(entrada) 

#Programa Principal 
while True:     
 FSM(randint(0,1)) 
 sleep(2)

#Variable global 
estado = 'i' 

#Estados ######################################################################
def EDOi(entrada): 
    global estado 
    print('Estado Inicial') 
    #Se tiver alguma configuração inicial colocar aqui
    estado = 0 

#Leitura do QR code do usuário ################################################
def EDO0(entrada): 
    global estado 
    print('Estado 0') 
    if flag_usuario_nova_garrafa == 0:
        print('Novo usuário, realizar a leitura do QRcode do usuário.')
        id_qr_code_string = None
        id_qr_code_string = qrcode()

    elif flag_usuario_nova_garrafa == 1:
        print('O usuário vai inserir uma nova garrafa.')
        id_qr_code_string = repetir_id_qr_code_string 

    if id_qr_code_string == None:
        estado = 0

    else:
        data_usuario = {'cpf' = id_qr_code_string}
        #Se id_qr_code_string for um string com o CPF separado por ponto e vírgula
        r = requests.post(url = API_ENDPOINT, data = data_usuario)
        usuario = r.json()

        estado = 1
         
#Leitura do QR code da garrafa ################################################
def EDO1(entrada): 
    global estado 
    print('Estado 1')

    qr_code_string = None
    qr_code_string = qrcode()
    #Comunicar com banco de dados
    if qr_code_string == None:
        print("Não foi possível ler o QRcode da garrafa.")
    
    else:
        data_garrafa = {'qr_garrafa' = qr_code_string}
        #Se o qr_code_string for uma string ok, se não alterar
        rg = requests.post(url = API_ENDPOINT, data = data_garrafa)
        garrafa = rg.json()

    if garrafa['material'] == 'plastico': #rever essas variaveis
        estado = 2
    
    elif garrafa['material'] == vidro:
        estado = 3
    else:
		print("Erro na comunicação com a API de software")
        
#verifica se o compartimento ta cheio. ########################################
def EDO2(entrada): 
    global estado 
    print('Estado 2')
    
    compartimento_plastico = verifica_compartimento(pino_compartimento_plastico)
    
	if compartimento_plastico == '0':
        time.sleep(0.1)
        if compartimento_plastico == '0':
            estado = 11 #usuário escolhe se quer inserir outra garrafa
            print("Compartimento do plástico está cheio. Realizar limpeza")

	else:
		print("Limpeza total, vamo nessa!")
		estado = 4
        
#verifica se o compartimento ta cheio. ########################################
def EDO3(entrada): 
    global estado 
    print('Estado 3')
    
	compartimento_vidro = verifica_compartimento(pino_compartimento_vidro)

    
    if compartimento_vidro == '0':
        time.sleep(0.1)
    	if compartimento_vidro == '0':
            estado = 11 #usuário escolhe se quer inserir outra garrafa
            print("Compartimento do Vidro está cheio. Realizar limpeza")
		
	else:
		print("Limpeza total, vamo nessa!")
		estado = 4
        
#abrindo a porta para inserir a garrafa #######################################
def EDO4(entrada): 
    global estado
    print('Estado 4')
    print("Abrindo a porta para o usuário inserir a garrafa.")
    motor(4800)
    estado = 5

#Verificando se a garrafa foi inserida ########################################
def EDO5(entrada): 
    global estado
    print('Estado 5')
    
    peso_balanca = balanca()
    
    if (peso_balanca >= 10):
        estado = 6
    
	while (peso_balanca < 10):
		print("Insira a Garrafa.")
		time.sleep(1)
		peso_balanca = balanca()
        time.sleep(1)
        estado = 5
        
    
#Verificando se o usuário está com a mão na porta #############################
def EDO6(entrada): 
    global estado 
    print('Estado 6')
    
    usuario_compartimento = verifica_compartimento(pino_usuario_compartimento)
		if usuario_compartimento == '0':
			print("Retire a mão dai porra.")
        estado = 6

			while (usuario_compartimento == "0"):
					print("RETIRA A PORRA DA MÃO DAI")
                usuario_compartimento = verifica_compartimento(pino_usuario_compartimento)
                estado = 6
            
			else:
				print("Usuário retirou a mão da máquino, pode seguir em frente.")
             estado = 7

		elif usuario_compartimento == '1':
        print("BORA BORA! LIGA TUDO")
        estado = 7

#Verificando peso #############################################################
def EDO7(entrada): 
    global estado 
    print('Estado 7')
    
    peso_balanca = balanca()
    if peso_balanca >= (garrafa['peso'] - 10) and peso_balanca <= (garrafa['peso'] + 10):
			print("Peso do Garrafa aprovado!")
			estado = 8
    else:
			print("Problemas com o peso da Garrafa, por gentileza, retire a ÁGUA da garrafa.")
			time.sleep(1)
			print("Aguarde 3 segundos")
			time.sleep(3)
            estado = 12 #criar estado para o cara retirar a garrafa
            
#Verificando capacitivo #######################################################
def EDO8(entrada): 
    global estado 
    print('Estado 8')
    
    print("Fazendo a checkagem do sensor capacitivo.")
		material_garrafa_sensor = verifica_material()

		if material_garrafa_sensor == garrafa['material']:
			print('Material da garrafa está OK de acordo com QRcode e S. Capacitivo.')
            estado = 9
        
       else:
			print('temos um problema com material da garrafa.')
            estado = 12 #criar estado para o cara retirar a garrafa
             
#Empurrando garrafa pro inferno ###############################################
def EDO9(entrada): 
    global estado 
    print('Estado 9')
    
    if garrafa['material'] == 'vidro':
		motor(4800)
		time.sleep(0.5)
		motor(-4800)
        estado = 10
	elif garrafa['material'] == 'plastico':
		motor(-4800)
		time.sleep(0.5)
		motor(4800)
        estado = 10
	else:
		print("ERROR")
            
#Pontuar para o usuário #######################################################
def EDO10(entrada):
    global estado 
    print('Estado 10')
    
    estado = 11
            
#Verificando se o usuário que inserir mais garrafas ###########################
def ED11(entrada): 
    global estado 
    print('Estado 11')
    
    print("deseja inserir mais uma garrafa?")
	time.sleep(2)
	motor(-4800)

	if GPIO.input(pino_botao_confirma_nova_garrafa) == True:
		estado = 1
		repetir_id_qr_code_string = id_qr_code_string
	else:
        estado = 0
        
#Retirar a garrafa, deu ruim ##################################################
def EDO12(entrada): 
    global estado 
    print('Estado 12')
    
    peso_balanca = balanca()
    
    if (peso_balanca <= 10):
        estado = 12
    
	while peso_balanca >= (garrafa['peso'] + 20) and peso_balanca <= (garrafa['peso'] - 20):
		print("Retire a Garrafa.")
		time.sleep(1)
		peso_balanca = balanca()
        estado = 12
		time.sleep(1)
    
    else:
        estado = 8

#Verificando se o usuário está com a mão na porta #############################
def EDO13(entrada): 
    global estado 
    print('Estado 13')
    
    usuario_compartimento = verifica_compartimento(pino_usuario_compartimento)
		if usuario_compartimento == '0':
			print("Retire a mão dai porra.")
        estado = 13

			while (usuario_compartimento == "0"):
					print("RETIRA A PORRA DA MÃO DAI")
                imento = verifica_compartimento(pino_usuario_compartimento)
                estado = 13
            
			else:
				print("Usuário retirou a mão da máquino, pode seguir em frente.")
             estado = 14

		elif usuario_compartimento == '1':
        print("Fechar compartimento")
        estado = 14
            
#Fechando a porta #############################################################
def EDO14(entrada): 
    global estado
    print('Estado 14')
    estado = 11 #verificar se o usuário quer inserir mais garrafas
	print("Fechando a porta.")
	motor(-4800)
