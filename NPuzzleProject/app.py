from flask import Flask, render_template, request, jsonify
from static import solver

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("SP/index.html")

@app.route('/hint')
def hint():
	state = request.args.get('state')
	stateArray = state.split(',')
	return str(solver.getHint(stateArray, 1));
	
@app.route('/solve')
def solve():
	state = request.args.get('state')
	stateArray = state.split(',')
	solutionSequence = solver.getSolutionSequence(stateArray, 25);
	return jsonify(sequence=solutionSequence)
