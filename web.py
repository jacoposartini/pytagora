""" Shows how to use flask and matplotlib together.
Shows SVG, and png.
The SVG is easier to style with CSS, and hook JS events to in browser.
python3 -m venv venv
. ./venv/bin/activate
pip install flask matplotlib
python flask_matplotlib.py
"""
import io
import random
from flask import Flask, Response, request, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
import numpy as np
import matplotlib.pyplot as plt

from parser import Parser



app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h1>Pytagora</h1>
    <p>A cura di Agnese e Jacopo Sartini</p>
    <a href='/definite_integrals'> Integrali definiti </a>
    <br>
    <a href='/caption'> Sintassi delle funzioni </a>
    """

@app.route("/caption")
def caption():
    return render_template('caption.html' )

@app.route("/definite_integrals")
def definite_integrals():
    a = int(request.args.get("a", 2))
    b = int(request.args.get("b", 8))
    fx = str(request.args.get("fx", 'sin(x)'))
    return render_template('definite_integrals.html', fx=fx, a=a, b=b )

@app.route("/definite_integrals/fx=<string:fx>&a=<string:a>&b=<string:b>.svg")
def plot_svg(fx, a, b):
    a, b = int(a), int(b)
    PRECISION =  (b - a) * 20
    x = np.linspace( a, b, PRECISION)
    y = [Parser(fx,  { 'x' : val }).getValue() for val in x]

    chart, curve = plt.subplots()
    # Disegno la curva
    curve.plot(x, y, 'red', linewidth=2)
    underlying_area = 0
    for index in range(0, len(x)-1):
        deltax = x[index+1] - x[index]
        # Calcolo l'area del rettangolo piccolo
        rectangle_min = plt.Rectangle((x[index], 0), deltax, y[index], alpha=.2, fc='green',ec="black")
        area_min = rectangle_min.get_height() * rectangle_min.get_width()
        # Calcolo l'area del rettangolo grande
        rectangle_max = plt.Rectangle((x[index], 0), deltax, y[index+1], alpha=.1, fc='blue',ec="black")
        area_max = rectangle_max.get_height() * rectangle_max.get_width()
        # Disegno i due rettangoli sul grafico
        curve.add_patch(rectangle_min)
        curve.add_patch(rectangle_max)
        # Aggiungo la media dei due rettangoli all'area totale
        underlying_area += np.mean([area_min, area_max])
    # Mostro il grafico e stampo il risultato
    chart.text(.1, .9, f'Risultato: {underlying_area}')
    output = io.BytesIO()
    FigureCanvasSVG(chart).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
