#!/bin/bash

iniciar_gateway() {
  cd /home/pi/Documents/mqtt-node
  node raspberry.js
}

echo "iniciando gateway..."
iniciar_gateway &
echo "gateway iniciado!"
