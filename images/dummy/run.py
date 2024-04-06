from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status":"ok"})

@app.route("/inference", methods=['POST'])
def inference():
    return jsonify(request.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)