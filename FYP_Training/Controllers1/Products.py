from flask import request,jsonify
import pandas as pd
from sqlalchemy import text
from FYP_Training.Model1.Products import Products
from FYP_Training.db import db
class ProductControllers:
	@staticmethod
	def product_reg():
		data = pd.read_csv('C:/Users/Faseeh-Ur-Rehman/Downloads/archive/products.csv')
		for i in range(len(data)):
			new_customer = Products(product_ID=int(data['product_ID'].iloc[i]),product_type=str(data['product_type'].iloc[i]),product_name=str(data['product_name'].iloc[i]),size=str(data['size'].iloc[i]),colour=str(data['colour'].iloc[i]),price=int(data['price'].iloc[i]),quantity=int(data['quantity'].iloc[i]), description=str(data['description'].iloc[i]))
			db.session.add(new_customer)
			db.session.commit()
		return jsonify({'msg': 'Data Add Successfully'})