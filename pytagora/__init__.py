from flask import Flask, render_template
app = Flask(__name__)

import pytagora.definite_integrals, pytagora.equations

@app.route("/")
def index():
    return """
    <h1>Pytagora</h1>
    <p>A cura di Agnese e Jacopo Sartini</p>
    <a href='/definite_integrals'> Integrali definiti </a>
    <br>
    <a href='/equations'> Equazioni </a>
    <br>
    <a href='/caption'> Sintassi delle funzioni </a>
    """

@app.route("/caption")
def caption():
    return render_template('caption.html')

