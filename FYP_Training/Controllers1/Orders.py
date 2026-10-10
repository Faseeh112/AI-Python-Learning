from datetime import datetime
from flask import request,jsonify
import pandas as pd
from sqlalchemy import text
from FYP_Training.Model1.Orders import Orders
from FYP_Training.db import db
class OrderControllers:
	@staticmethod
	def order_reg():
		data = pd.read_csv('C:/Users/Faseeh-Ur-Rehman/Downloads/archive/orders.csv')
		for i in range(len(data)):
			new_customer = Orders(order_id=int(data['order_id'].iloc[i]),
								    customer_id=int(data['customer_id'].iloc[i]),
									payment=int(data['payment'].iloc[i]),
								    order_date=data['order_date'].iloc[i],
									delivery_date=data['delivery_date'].iloc[i])

			db.session.add(new_customer)
		db.session.commit()
		return jsonify({'msg': 'Data Add Successfully'})