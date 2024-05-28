#Main Flask App

from flask import Flask, render_template, jsonify
from flask import request
from flask_cors import CORS
from chat import get_response


app = Flask(__name__, template_folder='./templates')

#To run separately:
# app = Flask(__name__)  #no need for getting a template just integrate it to a React component for example
# CORS(app)


@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug = True)
    


""" RUN:
~ mac/chatbot % python3 app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with watchdog (fsevents)

"""