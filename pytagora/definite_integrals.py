import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_svg import FigureCanvasSVG
import io
from pytagora.parser import Parser
from flask import Flask, Response, request, render_template
from pytagora import app
import numexpr as ne


@app.route("/definite_integrals")
def definite_integrals():
    a = int(request.args.get("a", 2))
    b = int(request.args.get("b", 8))
    fx = str(request.args.get("fx", 'sin(x)'))
    return render_template('definite_integrals.html', fx=fx, a=a, b=b)


@app.route("/definite_integrals/fx=<string:fx>&a=<string:a>&b=<string:b>.svg")
def definite_intergrals_plot_svg(fx, a, b):
    a, b = int(a), int(b)
    PRECISION = (b - a) * 20
    x = np.linspace(a, b, PRECISION)
    y = ne.evaluate(fx)

    chart, curve = plt.subplots()
    # Disegno la curva
    curve.plot(x, y, 'red', linewidth=2)
    underlying_area = 0
    for index in range(0, len(x)-1):
        deltax = x[index+1] - x[index]
        # Calcolo l'area del rettangolo piccolo
        if not np.isnan(y[index]) and not np.isnan(y[index + 1]):
            rectangle_min = plt.Rectangle(
                (x[index], 0), deltax, y[index], alpha=.2, fc='green', ec="black")
            area_min = rectangle_min.get_height() * rectangle_min.get_width()
            # Calcolo l'area del rettangolo grande
            rectangle_max = plt.Rectangle(
                (x[index], 0), deltax, y[index+1], alpha=.1, fc='blue', ec="black")
            area_max = rectangle_max.get_height() * rectangle_max.get_width()
            # Disegno i due rettangoli sul grafico
            curve.add_patch(rectangle_min)
            curve.add_patch(rectangle_max)
            # Aggiungo la media dei due rettangoli all'area totale
            underlying_area += np.mean([area_min, area_max])

    # Mostro il grafico e stampo il risultato
    chart.text(.1, .9, f'Risultato: {np.around(underlying_area, decimals=2)}')
    output = io.BytesIO()
    FigureCanvasSVG(chart).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")
