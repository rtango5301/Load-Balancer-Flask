from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from Server 1!"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    operation = data.get('operation')
    try:
        result = eval(operation)
        return {"result": result, "server": "Server 1"}
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)