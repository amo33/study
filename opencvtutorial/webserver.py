import base64
import os
from flask import Flask, render_template, Response , url_for , redirect
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
socketio = SocketIO(app)
outputFrame = None
def generate():
    while True: # 계속 들어오기 때문에 계속 yield 해준다. 
        frame = base64.b64decode(outputFrame) # 넘겨줄때 이걸 꼭 해야하는지 체크해보자.
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_frame')
def video_frame():
    return Response(generate(), mimetype= "multipart/x-mixed-replace; boundary=frame")

@socketio.on('streaming') # streaming 이라는 이벤트가 client로부터 emit 되면 이 함수를 실행 
def connect(framedata):
    global outputFrame
    outputFrame = framedata # global 변수에 넣어줌으로써 video_frame과 generate 함수에서 값 접근이 가능하다.
    return redirect(url_for('video_frame'))
    
if __name__ == '__main__':
    socketio.run(app, debug=True)