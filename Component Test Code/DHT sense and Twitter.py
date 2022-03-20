import time
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_dht
import csv
import tweepy
from picamera import PiCamera
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

egg=40

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
    )
twitter = tweepy.API(auth)
camera = PiCamera()
camera.rotation = 180

lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, 16, 2)
lcd.clear()

def tweet(message):
    twitter.update_status(status=message)

def tweetMedia():
    picture_title = datetime.now().strftime('%d|%m_%H:%M:%S')
    camera.start_preview()
    time.sleep(3)
    camera.capture('/home/pi/Desktop/PiPlantAssignment/Photos/%s.jpg' % picture_title)
    camera.stop_preview()
    image = twitter.media_upload(filename = '/home/pi/Desktop/PiPlantAssignment/Photos/%s.jpg' %picture_title)
    message = "This image was taken at {0}, the Temperature is {1}, and the Humidity is {2}".format(picture_title, temp, humid)
    twitter.update_status(status=message, media_ids=[image.media_id])
    print(message)


def DHT_read():
    for x in range(1):
        try:
            # Print the values to the serial port
            global temp
            global humid
            temp = dhtDevice.temperature
            humid = dhtDevice.humidity
        
        except RuntimeError as error:
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

def makeCSVwork():
    log = open('/home/pi/Desktop/Tweepy/dhtAndTwitterTest.csv', 'a')
    writer = csv.writer(log)
    fudge = [datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), temp, humid]
    writer.writerow(fudge)
    log.close()
    #fudge = 2
    
while True:
    # date and time
    lcd_line_1 = datetime.now().strftime('%d/%m  %H:%M:%S\n')
    
    DHT_read()
    
    lcd_line_2 = "Tmp {}\337C Hmd {}%".format(temp, humid)
    
    lcd.message = lcd_line_1 + lcd_line_2
    print(egg)
    if egg == 45: #Apparently 45 iterations equals a minute, seems legit
        makeCSVwork()
        tweetMedia()
        egg=0
    else:
        egg=egg+1

    time.sleep(1)    