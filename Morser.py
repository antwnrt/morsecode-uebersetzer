#!/usr/bin/env python3

from i2clcd import i2clcd
import RPi.GPIO as GPIO
from time import sleep


BtnPin = 18
BeepPin = 17

# Dictionary
morse_codes = {
    '.-'  :'A',
    '-...':'B',
    '-.-.':'C',
    '-..' :'D',
    '.'   :'E',
    '..-.':'F',
    '--.' :'G',
    '....':'H',
    '..'  :'I',
    '.---':'J',
    '-.-' :'K',
    '.-..':'L',
    '--'  :'M',
    '-.'  :'N',
    '---' :'O',
    '.--.':'P',
    '--.-':'Q',
    '.-.' :'R',
    '...' :'S',
    '-'   :'T',
    '..-' :'U',
    '...-':'V',
    '.--' :'W',
    '-..-':'X',
    '-.--':'Y',
    '--..':'Z',
    '.-.-':'Ä',
    '---.':'Ö',
    '..--':'Ü',

    '.----':'1',
    '..---':'2',
    '...--':'3',
    '....-':'4',
    '.....':'5',
    '-....':'6',
    '--...':'7',
    '---..':'8',
    '----.':'9',
    '-----':'0',

    '.-.-.-':'.',
    '..--..':'?',
    '..-..' :',',
    #unerkannt:Zeile71
}

# input = '...'
# return = 'S'
#
# input = '---'
# return = 'O'
def translator(input):
    if input in morse_codes:
        buchstabe = morse_codes[input]
        return buchstabe
    else:
        return '_'


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BtnPin, GPIO.IN)
    GPIO.setup(BeepPin, GPIO.OUT, initial=GPIO.HIGH)
    lcd = i2clcd(i2c_bus= 1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    return lcd


def cleanup(lcd):
    GPIO.output(BeepPin, GPIO.HIGH)
    lcd.clear()
    GPIO.cleanup()


def main(lcd):
    counter_pressed = 0
    counter_released = 0
    last_inputs = ''
    while True:
        input = GPIO.input(BtnPin)
        if input == 0:
            GPIO.output(BeepPin, GPIO.LOW)
            counter_pressed += 1
            if counter_released > 0:
                counter_released = 0
        else:
            GPIO.output(BeepPin, GPIO.HIGH)
            counter_released += 1
            if counter_pressed > 0:
                if counter_pressed > 15:
                    last_inputs += '-'
                else:
                    last_inputs += '.'
                counter_pressed = 0
            if counter_released > 70 and last_inputs:
                lcd.print(translator(last_inputs))
                last_inputs = ''
        sleep(0.01)


if __name__ == '__main__':
    lcd = setup()
    try:
        main(lcd)
    except KeyboardInterrupt:
        cleanup(lcd)
