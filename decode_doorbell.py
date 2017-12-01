import time
import sys
import os
from datetime import datetime
from datetime import timedelta
import RPi.GPIO as GPIO
import asyncio
import aiohttp
import notifier

RECEIVE_PIN = 13
NOTIFY_HOST = os.environ['SLACKBOT_SERVER']
SERVER_TOKEN = os.environ['SERVER_TOKEN']
SOURCE_ID = os.environ['DORBIT_SOURCE_ID']

doorbell_code = '011010110000100000'

one_pw = 0.000329
zero_pw = 0.0010545
zero_one = 0.00113
one_one = 0.001138
one_zero = 0.000377
zero_zero = 0.000413
code_delay = 0.00755

timings = {
    'one_pw':       lambda x: one_pw - 0.00002 <= x <= one_pw + 0.00002,
    'zero_pw':      lambda x: zero_pw - 0.00005 <= x <= zero_pw + 0.00005,
    'code_delay':   lambda x: code_delay - 0.003 <= x <= code_delay + 0.003,
    '00':           lambda x: zero_zero - 0.0001 <= x <= zero_zero + 0.0001,
    '01':           lambda x: zero_one - 0.0001 <= x <= zero_one + 0.0001,
    '10':           lambda x: one_zero - 0.0001 <= x <= one_zero + 0.0001,
    '11':           lambda x: one_one - 0.0001 <= x <= one_one + 0.0001
}

def validate_code(code):
    return code == doorbell_code

def decode_delta(delta_time):
    seconds = delta_time.microseconds / 1000000.0

    if timings['zero_pw'](seconds):
        return '0'
    elif timings['one_pw'](seconds):
        return '1'
    else:
        return ''

def receive_codes():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    signal = GPIO.input(RECEIVE_PIN)
    low_delta = timedelta(0)
    high_delta = timedelta(0)
    code_word = ''
    while True:
        
        beginning_time = datetime.now()
        while signal == 1:
            high_delta = datetime.now() - beginning_time
            signal = GPIO.input(RECEIVE_PIN)

        bit = decode_delta(high_delta)

        if len(code_word) > 0:
            previous_bit = code_word[-1]
            
            if bit:
                code_word += bit
            else:
                low_delay = timedelta(0)
                code_word = ''
                continue
        else:
            code_word += bit
        
        beginning_time = datetime.now()
        while signal == 0:
            low_delta = datetime.now() - beginning_time
            signal = GPIO.input(RECEIVE_PIN)


        if timings['code_delay'](low_delta.microseconds / 1000000.0):
            if validate_code(code_word):
                print(code_word + " Ring-a-ding ding!")
                notifier.notify(NOTIFY_HOST + '/ring', { 'source_id': 0, 'token': SERVER_TOKEN })
                time.sleep(2)
            code_word = ''
            high_delta = timedelta(0)
            low_delta = timedelta(0)

if __name__ == '__main__':
    exec('receive_codes()')
