var mqtt = require('mqtt')  
var Backbone = require('backbone');
var fs = require('fs');


var Gateway = Backbone.Model.extend({
  defaults:{
    mac: '',
    id: '',
    options_config_local: {port: 1883,
               host: 'localhost',
               keepalive: 60,
               reconnectPeriod: 1000,
               protocolId: 'MQTT',
               protocolVersion: 4,
               clean: true},
     mqtt_client_local: null
  },

  initialize: function(){

    var that = this

    this.set('mqtt_client_local', mqtt.connect(this.get('options_config_local')));
    this.get('mqtt_client_local').subscribe('out_topic');
    this.get('mqtt_client_local').on('message', function(topic, payload){
      that.parse_evento(topic, payload, that.get('mqtt_client_local'))
    });
},

  forward_message: function(topic, payload, client) {

    client.publish(topic, payload)
    console.log('\n porta: ' + client.options.port + ', destinatário: ' + client.options.host)
    console.log(' ENVIOU MENSAGEM '  + topic + ' - ' + payload)
  },

  parse_evento: function(topic, payload, client){

    if (client == this.get('mqtt_client_local')){
          console.log('Recebendo mensagem...')
          // delay = setTimeout(this.forward_message, 300, topic, payload, this.get('mqtt_client_local'));
          console.log ('Mensagem recebida: ' + topic + ' - '  + 'mensagem: ' + payload)
      }
  }

});

module.exports = {Gateway};

function main(){
  gateway = new Gateway()
  
}

main()
