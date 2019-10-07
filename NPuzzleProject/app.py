from flask import Flask, render_template, request
from static import solver

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("SP/index.html")

@app.route('/hint')
def hint():
	state = request.args.get('state')
	stateArray = state.split(',')
	return str(solver.getHint(stateArray, 5));
	
