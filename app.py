from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import os

app = Flask(__name__)
CORS(app)

# 'database' is the DNS name we will give to the Redis container in the network
db = redis.Redis(host='database', port=6379, decode_responses=True)

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        note = request.json.get('note')
        if note:
            db.lpush('notes_list', note)
            # This path must be mounted via a Volume/Bind Mount
            log_file = '/app/data/audit.log'
            with open(log_file, 'a') as f:
                f.write(f"New note added: {note}\n")
            return jsonify({"status": "success"}), 201
    
    return jsonify(db.lrange('notes_list', 0, -1))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)