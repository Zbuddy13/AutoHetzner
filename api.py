from quart import  Quart, jsonify
from quart import request
import os

port = os.environ.get('port', 2500)

app = Quart(__name__)

data = {"nothing" : "sent"}

@app.post("/recieve")
async def recieve():
    global data
    try:
        data = await request.get_json()  # Attempt to parse JSON
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400  # Handle missing or invalid JSON
        print(f"Received data: {data}")  # Print received data with formatting
        # Process or store the data here (replace with your logic)
        return jsonify({"message": "Data received successfully!"})
    except Exception as e:  # Catch generic exceptions for robustness
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.get("/send")
async def send():
    global data
    return data

def run() -> None:
    app.run(port=port)