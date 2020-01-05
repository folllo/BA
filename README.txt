How to setup The App to run:
!! I tested it on Ubuntu 16.04  should run on higher versions too though!!

Prequisites:

- git installed:
	sudo apt-get install git

- pip3 installed:
	sudo apt-get install pip3

- flask installed:
	pip3 install flask

- z3 solver installed:
	pip3 install z3-solver

Setup:
- Clone git repository at: https://github.com/folllo/BA

- Everything needed to run the app is located in NPuzzleProject because the rest of the repository is quite a mess 

To run the app:
- open the terminal and go to NPuzzleProject folder

- start virtualenv:
	. venv/bin/activate

- start flask app:
	export FLASK_APP=app.py
	flask run

- open browser and go to "http://127.0.0.1:5000" or "localhost:5000"

- play ;)

