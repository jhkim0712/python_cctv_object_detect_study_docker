from flask import Flask, send_file, Response
import os
import time

app = Flask(__name__)

OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/output')

@app.route('/')
def index():
  text = '''
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>CCTV Object Detection Image Stream</title>
  </head>
  <body>
      <h1>CCTV Object Detection Image Stream</h1>
      <h2>흠좀무....</h2>
      <img src="/stream" alt="CCTV Stream" />
  </body>
  </html>
  '''
  return text

@app.route('/stream')
def stream():
    def generate():
        last_file = None
        while True:
            files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.jpg')])
            if files:
                latest = files[-1]
                if latest != last_file:
                    last_file = latest
                    with open(os.path.join(OUTPUT_DIR, latest), 'rb') as f:
                        img = f.read()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            time.sleep(0.2)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
