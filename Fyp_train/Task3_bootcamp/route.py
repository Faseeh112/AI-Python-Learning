from flask import Flask,request,jsonify
from Controllers.Product import Product
app = Flask(__name__)

@app.route('/display')
def dis():
	return Product.show_table()

if __name__=='__main__':
	app.run()