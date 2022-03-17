from pyfirmata import Arduino, util
from time import sleep
import csv
from datetime import datetime
board = Arduino('/dev/ttyACM0')
led = 13
sensor = 0

it = util.Iterator(board)
it.start()
board.analog[sensor].enable_reporting()

def makeCSVwork():
    log = open('/home/pi/Desktop/PiPlantAssignment/Component Test Code/soil_log2.csv', 'a')
    writer = csv.writer(log)
    fudge = [datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), moist]
    writer.writerow(fudge)
    log.close()

while True:
    sleep(0.01)
    global moist
    moist=int(board.analog[sensor].read()*1000)
    print(moist)
    makeCSVwork()
    if moist < 200:
        board.digital[7].write(0)
    else:
        board.digital[7].write(1)
    sleep(0.49)
    

   