from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Backend Test OK"

if __name__ == '__main__':
    print("Test server starting...")
    app.run(port=5001)
