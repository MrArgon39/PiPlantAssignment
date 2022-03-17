from pyfirmata import Arduino, util
from time import sleep
board = Arduino('/dev/ttyACM0')
led = 13
relay = 7

while True:
    board.digital[led].write(1)
    board.digital[relay].write(0)#Relay is inverted
    sleep(2)
    board.digital[led].write(0)
    board.digital[relay].write(1)
    sleep(2)
    

   