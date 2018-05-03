from sys import argv
import zbar
import sys
import I2C_LCD_driver
import RPi.GPIO as GPIO
import time
from hx711 import HX711
from time import *

mylcd = I2C_LCD_driver.lcd() 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN) #pino verifica compartimento plastico
GPIO.setup(13, GPIO.IN) #pino verifica compartimento vidro
GPIO.setup(15, GPIO.IN) #pino sensor capacitivo 1
GPIO.setup(19, GPIO.IN) #pino sensor capacitivo 2
GPIO.setup(21, GPIO.OUT) #pino rele triturador

#Leitura do QRcode do usuário para identificação do usuário. O usuário vai ter um ID.

#Leitura do QRcode da garrafa, associar um ID para o material e peso da garrafa.
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

#Verificar se o compartimento das garrafas de vidro/plástico estão lotados.
#Verifica se o usuário está com a mão dentro do compartimento.
def verifica_compartimento(pino):
	if GPIO.input(pino) == True:
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

 



#Balança faz a checkagem do peso do garrafa, com margem de erro.

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


#Acionamento do motor de passo.

#Abrir compartimento para o usuário inserir a garrafa.

#Se a garrafa for de plástico acionar o triturador.
#pino 21
def acionamento_triturador():
	GPIO.output(21, GPIO.HIGH)

#Retorno da posição do motor de passo.
def main():




#chamada do main
def main():

if __name__ == '__main__':
    main()