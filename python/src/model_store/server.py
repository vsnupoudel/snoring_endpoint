import predict 
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
import gridfs

server = Flask(__name__)

mongo_wav = PyMongo(
        server,
        uri= "mongodb://host.minikube.internal:27017/wav"
)

fs_wav = gridfs.GridFS(mongo_wav.db)

@server.route("/predict", methods=["POST"])
def predict():
    if request.method == 'POST':
        f = request.files['file']
        try:
            is_snoring = predict.is_snoring(f)
        except:
            message = "Not a valid file type, try a comma separated file"
            return jsonify({})
        else:
            return jsonify({is_snoring: True})



