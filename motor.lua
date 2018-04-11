function MotorPasso (wire1, wire2, wire3, wire4)

  local self = {
    wire1 = wire1,
    wire2 = wire2,
    wire3 = wire3,
    wire4 = wire4,
  }
direction_all = nil;

_delay = 50000 --delay in between two steps. minimum delay more the rotational speed

gpio.mode(wire1, gpio.OUTPUT)--set four wires as output
gpio.mode(wire2, gpio.OUTPUT)
gpio.mode(wire3, gpio.OUTPUT)
gpio.mode(wire4, gpio.OUTPUT)


  local sequence = function (a, b, c, d)--four step sequence to stepper motor
      gpio.write(wire1, a)
      gpio.write(wire2, b)
      gpio.write(wire3, c)
      gpio.write(wire4, d)
      tmr.delay(_delay)
  end

  local rotacionar_motor = function (direction)
  
    while true do
      if direction == 'esquerda' then
        for i = 1 ,12 do --Rotation in one direction
            sequence(gpio.HIGH, gpio.LOW, gpio.LOW, gpio.LOW)
            sequence(gpio.HIGH, gpio.HIGH, gpio.LOW, gpio.LOW)
            sequence(gpio.LOW, gpio.HIGH, gpio.LOW, gpio.LOW)
            sequence(gpio.LOW, gpio.HIGH, gpio.HIGH, gpio.LOW)
            sequence(gpio.LOW, gpio.LOW, gpio.HIGH, gpio.LOW)
            sequence(gpio.LOW, gpio.LOW, gpio.HIGH, gpio.HIGH)
            sequence(gpio.LOW, gpio.LOW, gpio.LOW, gpio.HIGH)
            sequence(gpio.HIGH, gpio.LOW, gpio.LOW, gpio.HIGH)
        end
      end

      elseif direction == 'direita' then
        sequence(gpio.HIGH, gpio.LOW, gpio.LOW, gpio.LOW)
        for i = 1 ,12 do --Rotation in opposite direction
            sequence(gpio.LOW, gpio.LOW, gpio.LOW, gpio.HIGH)
            sequence(gpio.LOW, gpio.LOW, gpio.HIGH, gpio.HIGH)
            sequence(gpio.LOW, gpio.LOW, gpio.HIGH, gpio.LOW)
            sequence(gpio.LOW, gpio.HIGH, gpio.HIGH, gpio.LOW)
            sequence(gpio.LOW, gpio.HIGH, gpio.LOW, gpio.LOW)
            sequence(gpio.HIGH, gpio.HIGH, gpio.LOW, gpio.LOW)
            sequence(gpio.HIGH, gpio.LOW, gpio.LOW, gpio.LOW)
            sequence(gpio.HIGH, gpio.LOW, gpio.LOW, gpio.HIGH)
        end
        sequence(gpio.LOW, gpio.LOW, gpio.LOW, gpio.HIGH)
      end
    end

    return {
      rotacionar_motor = rotacionar_motor
    }
end 