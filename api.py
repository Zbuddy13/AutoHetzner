from flask import Flask, jsonify, request
import subprocess
import settings
import logging
import json

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True

@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'date': result.strip()})

@app.route('/returnjson', methods = ['GET']) 
def ReturnJSON(): 
    var = "hello"
    if(request.method == 'GET'): 
        data = { 
            "Modules" : var, 
            "Subject" : "Data Structures and Algorithms", 
        }
        #print(json.dumps(data, indent=4))
        return json.dumps(data) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3200)