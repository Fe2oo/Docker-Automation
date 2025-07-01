from flask import Flask

app2 = Flask(__name__)

@app2.route('/')
def hello():
    return "Hello from the second Docker container!"

if __name__ == '__main__':
    app2.run(host='0.0.0.0', port=5000)
    