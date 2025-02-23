from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Koneksi ke MongoDB Atlas
MONGO_URI = "mongodb+srv://adindaummy05:<UhWQfObXndHnNV2R>@dinda56.5rvzo.mongodb.net/?retryWrites=true&w=majority&appName=dinda56"
client = MongoClient(MONGO_URI)
db = client["sensor_data_SIC6_FutureMakers"]
collection = db["ldr_pir_data"]

@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.json
    if data:
        collection.insert_one(data)
        return jsonify({"message": "Data berhasil disimpan!"}), 200
    return jsonify({"error": "Data kosong"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Server Flask berjalan"}), 200

