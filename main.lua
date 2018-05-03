MODOS_OPERACAO = {NORMAL = 'normal', ATUALIZACAO = 'atualizacao'}

function loop_principal(timer_principal)

  gpio.trig(3, 'up', function()
    if (modo_operacao == MODOS_OPERACAO.NORMAL) then
      print('\nSaindo do loop principal...');
      modo_operacao = MODOS_OPERACAO.ATUALIZACAO
      timer_principal:stop()
    else
      print('\nEntrando no loop principal...');
      modo_operacao = MODOS_OPERACAO.NORMAL
      timer_principal:start()
    end
  end)

  if (modo_operacao == MODOS_OPERACAO.NORMAL) then
 
	  gpio.mode(2, gpio.INPUT) -- SENSOR PROXIMO AO TRITURADOR
	  gpio.mode(3, gpio.INPUT) -- SENSOR MAIS DISTANTE DO TRITURADOR
	  gpio.mode(1, gpio.OUTPUT) -- RELE PARA ACIONAR TRITURADOR
		gpio.mode(4, gpio.OUTPUT) -- RELE PARA ACIONAR O FREIO
    
    print('Entrando no loop principal...');
    timer_principal:register(2500, tmr.ALARM_AUTO, function()

	  	if ( gpio.read(2) == 0 and gpio.read(3) == 0 ) then
	  		print("Funil do triturador está vazio.")	
	  		tmr.delay(1000000)
	  		if ( gpio.read(2) == 0 and gpio.read(3) == 0 ) then
		  		gpio.write(1, gpio.LOW)
		  		gpio.write(4, gpio.HIGH)
		  		tmr.delay(5000000) -- ENERGIA CONTROLA
		  		gpio.write(4, gpio.LOW)

		  	else
		  		print("Movimento de garrafas no triturador.")
		  	end

	  	elseif ( gpio.read(2) == 1 and gpio.read(3) == 0 ) then
	  		print("Poucas garrafas no triturador.")
	  		gpio.write(4, gpio.LOW)
	  		gpio.write(1, gpio.HIGH)

	  	elseif ( gpio.read(2) == 1 and gpio.read(3) == 1 ) then
	  		print("Muitas garrafas no triturador.")
	  		gpio.write(1, gpio.HIGH)

	  	end

    end)
    timer_principal:start()
  end
end
  
function start()
  print(node.bootreason())
  print('\n\n=== Rodando');
  
  modo_operacao = MODOS_OPERACAO.NORMAL
  local timer_principal = tmr.create()
  loop_principal(timer_principal);
  
end
