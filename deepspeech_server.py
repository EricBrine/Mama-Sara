from flask import Flask
from flask import jsonify
from flask import request
from scipy.io.wavfile import read as wavread
from scipy.io.wavfile import write as wavwrite
import numpy as np
import wave
import cgi
import contextlib
import base64
import soundfile as sf
from flask_cors import CORS, cross_origin
import subprocess

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['POST'])
@cross_origin()
def post():
    with open("file.wav", "wb") as vid:
        vid.write(request.data)

    proc = subprocess.Popen(
        "deepspeech --model models/output_graph.pbmm --lm models/lm.binary --trie models/trie --audio file.wav",
        shell=True, stdout=subprocess.PIPE, )
    output = proc.communicate()[0].decode('ascii')
    print(output)

    return jsonify(
        message=output
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8341,debug=True)