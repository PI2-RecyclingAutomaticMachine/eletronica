function ClienteMqtt (host, port, id)

  local self = {
    id = id,
    host = host,
    port = port,
    data_att = data_att,
    topico_att = topico_att

  }

  function handle_mqtt_error(client, reason) 
    print('falha ao conectar no MQTT... reason: ', reason)
  end


  local mqtt_dados = function  (topico_enviar, topico_receber, mensagem)

    mac_address = wifi.sta.getmac()
    ipAddr = wifi.sta.getip()

    m = mqtt.Client(self.id, 10) -- cliente para enviar/receber
      
      if not ((ipAddr == nil) or (ipAddr == "0.0.0.0")) then
        print('\Conectando no mqtt...');
        
        m:connect(self.host, self.port, 0, 0, function()
          if (topico_enviar and mensagem) then
            
            m:publish(topico_enviar, mensagem, 1, 0)
            print('  mensagem enviada! detalhes', self.host, ':', self.port)
          end

          m:subscribe(topico_receber, 2, function (conn)

        end)
         
          m:on("message", function(conn, topico_receber, data) 
            if data ~= nil then
              print(' mensagem recebida! detalhes', self.host, ':', self.port)
              print(topico_receber .. ":" .. data)
              self.data_att = data
              self.topico_att = topico_receber

            end

          end)

        end,
        handle_mqtt_error)
      end
      
  end
  
  local mqtt_arquivo = function ()
    return self.data_att
  end

  local mqtt_topico = function ()
    return self.topico_att
  end

  local zerar_data_att = function ()
    print('Zerando o data_att com NIL')
    self.data_att = nil
  end

  return {
    mqtt_dados = mqtt_dados,
    mqtt_arquivo = mqtt_arquivo,
    mqtt_topico = mqtt_topico,
    zerar_data_att = zerar_data_att
    }
end