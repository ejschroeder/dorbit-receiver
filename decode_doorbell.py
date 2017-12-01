import time
import os
from datetime import datetime
from datetime import timedelta
import RPi.GPIO as GPIO
import notifier

RECEIVE_PIN = 13
NOTIFY_HOST = os.environ['SLACKBOT_SERVER']
SERVER_TOKEN = os.environ['SERVER_TOKEN']
SOURCE_ID = os.environ['DORBIT_SOURCE_ID']

doorbell_code = int('011010110000100000', 2)

one_pw = 0.000329
zero_pw = 0.0010545
code_delay = 0.00755

timings = {
    'one_pw':       lambda x: one_pw - 0.00002 <= x <= one_pw + 0.00002,
    'zero_pw':      lambda x: zero_pw - 0.00005 <= x <= zero_pw + 0.00005,
    'code_delay':   lambda x: code_delay - 0.003 <= x <= code_delay + 0.003
}


def validate_code(code):
    return code == doorbell_code


def decode_delta(delta_time):
    seconds = delta_time.microseconds / 1000000.0

    if timings['zero_pw'](seconds):
        return 0
    elif timings['one_pw'](seconds):
        return 1
    else:
        return None


def get_delta(signal):
    beginning_time = datetime.now()
    delta = timedelta(0)

    while GPIO.input(RECEIVE_PIN) == signal:
        delta = datetime.now() - beginning_time

    return delta


def receive_codes():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    code_word = 0

    while True:
        high_delta = get_delta(GPIO.HIGH)
        bit = decode_delta(high_delta)
        code_word = (code_word << 1) + bit if bit is not None else 0
        low_delta = get_delta(GPIO.LOW)

        if timings['code_delay'](low_delta.microseconds / 1000000.0):
            if validate_code(code_word):
                print("{} Ring-a-ding ding!".format(code_word))
                notifier.notify(NOTIFY_HOST + '/ring', {'source_id': SOURCE_ID, 'token': SERVER_TOKEN})
                time.sleep(4)
            code_word = 0


def main():
    receive_codes()


if __name__ == '__main__':
    main()

