wlan = dofile('wlan.lua')
mqtt = dofile('mqtt.lua')
motor = dofile('motor.lua')

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

    print('Entrando no loop principal...');
    timer_principal:register(7000, tmr.ALARM_AUTO, function()
      wlan.status_wifi();

      topico_receber = "#"
      topico_base_publicacao = "raspberry"
      cliente_mqtt.mqtt_dados(topico_base_publicacao, topico_receber, dados);
      topico = cliente_mqtt.mqtt_topico
      conteudo = cliente_mqtt.mqtt_arquivo
      peso = tonumber(conteudo)


      sensor_capacitivo_vidro = gpio.read(3)
      sensor_capacitivo_plastico = gpio.read(4)
      sensor_capacitivo_verificar = gpio.read(5)
      --hx711.init(clk, data)
      hx711.init(6, 1)
      read_hx711 = hx711.read(0)

      if topico == "vidro" then
        print("Topico: ", topico)
        print("Garrafa de vidro entrou na Máquina! peso: ", conteudo)

        dados = {}

        if read_hx711 == peso then
          print('Peso confere!')
          dados[0] = nil
        else
          print('Peso não confere')
          dados[0] = 'peso'
        end  

        if sensor_capacitivo_vidro == 1 then
          print('Sensor capacitivo verificou que é vidro')
          dados[1] = nil
        else
          print('Sensor capacitivo para o vidro não acionou')
          dados[1] = 'VidroF'

        end 

        if sensor_capacitivo_plastico == 0 then
          print('Sensor capacitivo verificou que não é plástico')
          dados[2] = nil     
        else
          print('Sensor capacitivo de plástico acionou')
          dados[2] ='PlasticoV'

        end

        if sensor_capacitivo_verificar == 0  then
          print('Sensor capacitivo de verificação não acionou')
          dados[3] = nil
        else
          print('Sensor capacitivo de verificação acionou')
          dados[3] ='VerificarV'
        end

        if dados ~= nil then
          topico_base_publicacao = topico_base_publicacao .. '/vidro'
          cliente_mqtt.mqtt_dados(topico_base_publicacao, topico_receber, dados);

        else
          motor.rotacionar_motor("esquerda") 
        end


      elseif topico == "plastico" then
        print("Topico: ", topico)
        print("Garrafa de plástico entrou na Máquina! peso: ", conteudo)

      end

    end)
    timer_principal:start()
  end
end
  
function start()
  print(node.bootreason())

  print('\n\n=== Rodando');
  
  wlan = WLan("Matheus", "batatafrita123", IP, NETMASK, GW)
  wlan.status_wifi();
  motor = MotorPasso(8,7,6,5)

  cliente_mqtt = ClienteMqtt("192.168.0.13", 1883, 'id') --função MQTT


  modo_operacao = MODOS_OPERACAO.NORMAL
  local timer_principal = tmr.create()
  loop_principal(timer_principal);
  
end
