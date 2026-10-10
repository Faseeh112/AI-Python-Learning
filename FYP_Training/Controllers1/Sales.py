from datetime import datetime
from sqlalchemy import func
from flask import request,jsonify
import pandas as pd
from sqlalchemy import text

from FYP_Training.Model1.Sales import Sales
from FYP_Training.db import db
class SalesControllers:
	@staticmethod
	def sale_reg():
		data = pd.read_csv('C:/Users/Faseeh-Ur-Rehman/Downloads/archive/sales.csv')
		for i in range(len(data)):
			new_customer = Sales(sales_id=int(data['sales_id'].iloc[i]),order_id=int(data['order_id'].iloc[i]),product_id=int(data['product_id'].iloc[i]),price_per_unit=int(data['price_per_unit'].iloc[i]),quantity = int(data['quantity'].iloc[i]),total_price=int(data['total_price'].iloc[i]))
			db.session.add(new_customer)
		db.session.commit()
		return jsonify({'msg': 'Data Add Successfully'})


