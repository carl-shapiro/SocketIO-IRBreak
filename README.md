# SocketIO-IRBreak
A simple POC using Flask + Socket IO server to send information from a Raspberry PI GPIO to a browser.


## Dependencies
This project requires the following Python 3 packages:

- RPi.GPIO
- flask
- flask_socketio


## Installation
SSH to the Raspberry Pi

Clone this repo to the Raspberry Pi

Install any missing dependencies. For Python 3, the following should work:

```sh
pip3 install RPi
pip3 install flask
pip3 install flask_socketio
```

Export the FLASK_APP variable via the command line. "/path/to/project" below is
the absolute path to where this repository was cloned to on the Raspberry Pi.

```sh
export FLASK_APP=[/path/to/project]/server/server.py
```

## Usage
Upload an mp3 alarm file to [/path/to/project/]**server/static/** on the Raspberry Pi

Define the name of the alarm file within the
[/path/to/project/]**server/templates/index.html** file to
the **alarmSound** variable

Start the Flask service within an SSH session to the Raspberry Pi:

```sh
flask run --host=0.0.0.0
```

On a browser within the network the Raspberry Pi is connected to,  
navigate to http://[YOUR_RASPBERRYPI_HOSTNAME]:5000

Click the "Arm" button to enable the alarm.
Click the "Disarm" button to disable the alarm.
