import RPi.GPIO as GPIO
from flask import Flask,request,render_template
from flask_socketio import SocketIO, send, emit
from time import sleep
from threading import Thread, Event
import logging

### Init/setup GPIO interface and turn on logging
BEAM_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
logging.basicConfig(filename='server.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

### Setup Flask + thread for RPi
app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*",logger=True, async_mode=None)
thread = Thread()
thread_stop_event = Event()

def break_beam_task():
    """
    Adding the breakbeam callback to the GPIO event detection;
    This task (and it's callback) should be run in a different thread
    """
    GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=break_beam_callback)
    while True:
        sleep(1) # let's not burn out the CPU...
        pass

def break_beam_callback(channel):
    socketio.emit('beam_state', {'connected': GPIO.input(BEAM_PIN)})

@app.route('/')

#load client
def index():
    return render_template('index.html')

####[ EVENTS ]######

#connect the client; load background task
@socketio.on('connect')
def handle_connect():
    global thread  # need visibility of the global thread object
    app.logger.info('[INFO] Web client connected: {}'.format(request.sid))
    emit('connection_response', {'data': 'Connection Successful'})
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(break_beam_task)

#heartbeat, used to maintain connection
@socketio.on('heartbeat')
def handle_heartbeat(heartbeat):
    print('received heartbeat: ' + str(heartbeat))
    emit('heartbeat', {'heartbeat': "<3"})

#not used, for future use
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

#main
if __name__ == '__main__':
    app.logger.info('======= Starting Server =========')
    socketio.run(app,debug=True)
