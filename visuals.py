from flask import Flask, jsonify, request, render_template, redirect, url_for

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import json

from buses import buses
from coulomb import coulomb

app = Flask(__name__)

b = buses(10)
k = coulomb()

@app.route("/")
def visuals(name=None):
    return render_template('visuals.html', name=name)

@app.route("/Dyson.html")
def Dyson(name=None):

    return render_template('Dyson.html', name=name, N=b.N, sigma=b.sigma, C=b.C, universality_class=b.beta_closed/b.sigma/b.sigma)

@app.route("/Coulomb.html")
def Coulomb(name=None):

    return render_template('Coulomb.html', name=name, N=k.N, sigma=k.sigma, C=k.C)

@app.route('/bus_sim', methods=['GET', 'POST'])
def bus_sim():
    # GET request
    if request.method == 'GET':
        b.update_closed(0.05, 10)
        message = {
            'positions': b.positions.tolist(),
            'N': b.N, 

        }
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        data = request.get_json()
        b.reinit(N=int(data['N']),sigma=float(data['sigma']), C=float(data['C']))
        # return data, 200
        return "Success", 200

@app.route('/koala_sim', methods=['GET', 'POST'])
def koala_sim():
    # GET request
    if request.method == 'GET':
        k.update_closed(0.05, 10)

        if k.circumcircles:
            [radii, x_center, y_center] = k.get_circumcircles(0)
            num_circles = len(radii)

            message = {
                'x_positions': k.positions[:, 0].tolist(),
                'y_positions': k.positions[:, 1].tolist(),
                'N': k.N, 
                'radii': radii,
                'x_center': x_center,
                'y_center': y_center,
                'num_circles': num_circles,
                'circumcircles': k.circumcircles
            }
        else:
            message = {
                'x_positions': k.positions[:, 0].tolist(),
                'y_positions': k.positions[:, 1].tolist(),
                'N': k.N, 
                'circumcircles': k.circumcircles
            }
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        data = request.get_json()
        k.reinit(int(data['N']),sigma=float(data['sigma']), C=float(data['C']))
        k.circumcircles = data['circumcircles']
        # return data, 200
        return "Success", 200