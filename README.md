# dorbit-receiver
Receives and decodes signals sent from a wireless doorbell. 

## Dependencies
The script requires Python 3 to run and uses libraries installed through pip

All dependencies are listed in `requirements.txt`. To install all of them, run:

`pip3 install -r requirements.txt`

You will also need to set some environment variables before you can run the script. 
- `SLACKBOT_SERVER` the base url for the web server to be called when a ring is detected.
- `SERVER_TOKEN` a string used by the web server to verify that this request came from a valid source.
- `DORBIT_SOURCE_ID` a string used by the web server to identify what device a request came from. It is used in debug messages, and can be anything you want.

## Running 

Once all of the dependencies are installed, the script can be started with

`python3 decode_doorbell.py`

The script will loop forever trying to match the input from a GPIO pin with the code and timings specified at the top of `decode_doorbell.py`. You can use `Ctrl+C` to terminate the process.