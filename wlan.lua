function WLan (ssid, pwd, IP, netmask, gw)

  local self = {
    ssid = ssid,
    pwd = pwd,
    IP = IP,
    netmask = netmask,
    gw = gw
  }

  local conectar_na_wifi = function ()
    station_cfg={}
      station_cfg.ssid = self.ssid
      station_cfg.pwd = self.pwd
      station_cfg.save = true

    wifi.setmode(wifi.STATION)
    wifi.sta.config(station_cfg)
    wifi.sta.connect()

    if wifi.sta.getip() == nil then
      print("Conectando no Wi-Fi...", self.ssid)

    else
      print("ESP8266 mode is: " .. wifi.getmode())
      self.mac_address = wifi.sta.getmac()
      print("Endereço MAC (sta) é: " .. self.mac_address)
      print("Conectado! o IP é: ".. wifi.sta.getip())
    end
    --ip_cfg = {}
    --  ip_cfg.ip = self.IP
    --  if (not self.netmask == nil) then ip_cfg.netmask = self.netmask end
    --  if (not self.gw == nil) then ip_cfg.gateway = self.gw end
    --wifi.sta.setip(ip_cfg)  

  end

  local status_wifi = function ()
    
    ipAddr = wifi.sta.getip()
    if ((ipAddr == nil) or (ipAddr == "0.0.0.0")) then
      conectar_na_wifi()
    else
      print('\n\n=== Status Wifi');
      print('    IP..........: ', wifi.sta.getip());
    end
  end

  return {
    conectar_na_wifi = conectar_na_wifi,
    status_wifi = status_wifi
  }

end
