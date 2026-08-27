from flask import Flask, jsonify
import time, random

app = Flask(__name__)

@app.get("/item/<int:n>")
def item(n):
    time.sleep(random.uniform(0.3, 0.6))  # 네트워크 대기를 흉내 냄
    return jsonify({"id": n, "name": f"item-{n}"})

if __name__ == "__main__":
    app.run(port=5000, threaded=True)