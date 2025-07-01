from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from a Docker container!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
#FROM python:3.9-slim
#COPY . /app
#WORKDIR /app
#CMD ["python", "app2.py"]

