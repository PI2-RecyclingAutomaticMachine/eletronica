function loop_principal(timer_principal)

	  while true do
	  	if (gpio.read(2)==1) then
	  		if (gpio.read(7)==1) then
	  			print("fazer nada, motor ja ta ligado")
	  		else 
	  			print("ligar motor")
	  			gpio.write(7, gpio.HIGH)
	  			flag_freio = 0
	  		end

	  	else
	  		if (flag_freio == 0) then
		  		gpio.write(7, gpio.LOW)
		  		print("desligar motor e ligar freio")
		  		tmr.delay(500000)
		  		gpio.write(8, gpio.HIGH)
		  		tmr.delay(1500000)
		  		gpio.write(8, gpio.LOW)

		  		flag_freio = 1
		  	else 
		  		print("fazer nada, freio ja foi acionado, ligar somente o freio quando o motor ligar antes")
		  	end
	  	end

	  	tmr.delay(500000)
	  end

end
  
function start()
  print(node.bootreason())
  print('\n\n=== Rodando');
  pin_rpi_ler = 2
  pin_ligar_motor = 7
  pin_ligar_freio = 8

  gpio.mode(pin_rpi_ler,gpio.INPUT)
  gpio.mode(pin_ligar_motor,gpio.OUTPUT)
  gpio.mode(pin_ligar_freio, gpio.OUTPUT)	

  local timer_principal = tmr.create()
  loop_principal(timer_principal);
