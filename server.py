from flask import Flask, render_template
import waitress


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

server = waitress.create_server(app, host="localhost", port=8080)
server.run()
