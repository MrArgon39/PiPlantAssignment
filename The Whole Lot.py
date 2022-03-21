import time #Import all the things
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_dht
import csv
import tweepy
from picamera import PiCamera
from pyfirmata import Arduino, util
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

#Note, when running this code, sometimes it will give an error saying that temp is undefined, run the code again and it will fix itself
#No idea why this happens

Uno = Arduino('/dev/ttyACM0')#Setup the arduino, and make sure that an analogue reading doesn't flood the port.
sensor = 0
it = util.Iterator(Uno)
it.start()
Uno.analog[sensor].enable_reporting()

bacon = 0
egg=0

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False) #Init the DHT

auth = tweepy.OAuth1UserHandler( #Import the access keys for the Twitter API
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
    )
twitter = tweepy.API(auth)

camera = PiCamera()
camera.rotation = 180 #Can be change to match the camera orientation

lcd_rs = digitalio.DigitalInOut(board.D22)#Init the LCD pins
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, 16, 2)
lcd.clear()

def tweet(message):#This is intended for sending a text tweet
    twitter.update_status(status=message)

def tweetMedia(enable):#This is for taking an image, uploading it to twitter, and adding a message to it.
    picture_title = datetime.now().strftime('%d|%m_%H:%M:%S')
    camera.start_preview()
    time.sleep(3)
    camera.capture('/home/pi/Desktop/PiPlantAssignment/Photos/%s.jpg' % picture_title)
    camera.stop_preview()
    if enable == 1:#I am lazy and didn't want to write a second image function, so I stopped the twitter bit.
        image = twitter.media_upload(filename = '/home/pi/Desktop/PiPlantAssignment/Photos/%s.jpg' %picture_title)
        message = "This image was taken at {0}, the Temperature is {1}, and the Humidity is {2}".format(picture_title, temp, humid)
        twitter.update_status(status=message, media_ids=[image.media_id])
        print(message)


def DHT_read():#Do I need to explain what this does?
    for x in range(1):
        try:
            global temp
            global humid
            temp = dhtDevice.temperature
            humid = dhtDevice.humidity
        
        except RuntimeError as error:
            continue #Error checking removed as to have more reliable readings
        except Exception as error:
            dhtDevice.exit()
            raise error

def makeCSVwork():
    log = open('/home/pi/Desktop/PiPlantAssignment/CompleteLog.csv', 'a')
    writer = csv.writer(log)
    fudge = [datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), temp, humid, moist]#This exists becuase when I tried doing it directly, it just broke.
    writer.writerow(fudge)
    log.close()
    #fudge = 2
    
def soilAndwater():
    time.sleep(0.01)#If this isn't here, my Pi loses the ability to math
    global moist
    global bacon
    moist=int(Uno.analog[sensor].read()*1000)#Weird fudge math as the pyfirmata make the read analog value into a float between 0.0-1.000
    print(bacon)
    if moist < 500:#Will need to be tuned for the individual plant.
        Uno.digital[7].write(0)
        bacon = 10
    elif bacon == 0:
        Uno.digital[7].write(1)
    else:
        bacon=bacon - 1
        

while True:
    #About every second, we refresh the data being sent to the lcd, and if we need to give the plant water.
    lcd_line_1 = datetime.now().strftime('%d/%m  %H:%M:%S\n')
    
    DHT_read()
    
    lcd_line_2 = "Tmp {}\337C Hmd {}%".format(temp, humid)#The \337 is the index for the degree symbol, an ascii version doesn't register.
    
    lcd.message = lcd_line_1 + lcd_line_2
    #print(egg)
    soilAndwater()
    if egg == 46: #Apparently 46 iterations equals a minute, seems legit
        makeCSVwork()
        egg=0
        if datetime.now().strftime('%H:%M') == '12:20':#takes a photo once at the time stated
            tweetMedia(0) #The tweeting functionality has been disabled until the the plant is being montiored, so that I am not just showing a photo of drit.
            #print('photo')
    else:
        egg=egg+1#The most important variable in the code, after bacon

    time.sleep(1)    #ZZZZZZzzzzzz