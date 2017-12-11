# dorbit-receiver
Receives and decodes signals sent from a wireless doorbell. 

## Dependencies
The script requires Python 3 to run and uses libraries installed through pip

All dependencies are listed in `requirements.txt`. To install all of them, run:

`pip3 install -r requirements.txt`

Once all of the dependencies are installed, the script can be started with

`python3 decode_doorbell.py`

The script will loop forever trying to match the input from a GPIO pin with the code and timings specified at the top of `decode_doorbell.py`. You can use `Ctrl+C` to terminate the process.