import time
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

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


while True:
    # date and time
    lcd_line_1 = datetime.now().strftime('%d/%m  %H:%M:%S\n')
    
    DHT_read()
    
    lcd_line_2 = "Tmp {}\337C Hmd {}%".format(temp, humid)
    
    lcd.message = lcd_line_1 + lcd_line_2

    time.sleep(1)
    