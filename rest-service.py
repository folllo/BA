from flask import Flask
from flask_restful import Api, Resource, reqparse
import solver

app = Flask(__name__)
api = Api(app)


@app.route('/solver', methods=['GET'])
def get():
	return "hello World"




app.run(debug=True)
