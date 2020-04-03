import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_svg import FigureCanvasSVG
import io
from pytagora.parser import Parser
from flask import Flask, Response, request, render_template
from pytagora import app

import numexpr as ne

@app.route("/equations")
def equations():
    f = str(request.args.get("f", 'x*2'))
    g = str(request.args.get("g", 'x'))
    return render_template('equations.html',  f=f, g=g)


@app.route("/equations/f=<string:f>&g=<string:g>.svg")
def equations_plot_svg(f, g):
    print(f, g)
    x = np.linspace(-10, 10, 1000000)
    y1 = ne.evaluate(f)
    y2 = ne.evaluate(g)

    chart, curve = plt.subplots()
    # Disegno la curva
    curve.plot(x, y1, 'blue', linewidth=2)
    curve.plot(x, y2, 'green', linewidth=2)

    intersetions_points = []
    idx = np.argwhere(np.diff(np.sign(y1 - y2))).flatten()

    for i in idx:
        print(y2[i])
        if not np.isnan(y1[i]) and not np.isnan(y2[i]):
            intersetions_points.append(np.around(x[i], decimals=2))
            plt.plot(x[i], y1[i], 'ro')

    intesetion_point = '; '.join([str(elem) for elem in intersetions_points])
    chart.text(.1, .9, f'Risultato: {intesetion_point}')
    output = io.BytesIO()
    FigureCanvasSVG(chart).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")
