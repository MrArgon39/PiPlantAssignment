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
    log = open('/home/pi/Desktop/soil_log.csv', 'a')
    writer = csv.writer(log)
    fudge = [datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), moist]
    writer.writerow(fudge)
    log.close()

while True:
    board.digital[led].write(1)
    sleep(0.25)
    board.digital[led].write(0)
    global moist
    moist=int(board.analog[sensor].read()*1000)
    print(moist)
    makeCSVwork()
    sleep(0.25)
    

   