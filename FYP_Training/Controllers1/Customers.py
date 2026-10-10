import numpy as np
from flask import request,jsonify
from datetime import datetime
import pandas as pd
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy import case
from FYP_Training.Model1.Customers import Customers
from FYP_Training.Model1.Products import Products
from FYP_Training.Model1.Sales import Sales
from FYP_Training.Model1.Orders import Orders
from FYP_Training.db import db

class CustomerControllers:
	@staticmethod
	def register():
		# data = request.get_json()
		# print('name=', data['name'], 'email=', data['email'], 'password=', data['password'])
		data=pd.read_csv('C:/Users/Faseeh-Ur-Rehman/Downloads/archive/customers.csv')
		# print(df['customer_name'][0])
		for i in range(len(data)):
			new_customer = Customers(customer_id=int(data['customer_id'].iloc[i]),customer_name=str(data['customer_name'].iloc[i]),
									 gender=str(data['gender'].iloc[i]), age=int(data['age'].iloc[i]),
									 home_address=str(data['home_address'].iloc[i]),zip_code=int(data['zip_code'].iloc[i]),
									 city=str(data['city'].iloc[i]),state=str(data['state'].iloc[i]),country=str(data['country'].iloc[i]))
			db.session.add(new_customer)
			db.session.commit()
		return jsonify({'msg': 'Data Add Successfully'})
### Avg cart item price
	@staticmethod
	def avg():
		# sub = db.session.query(Sales.order_id, func.sum(Sales.total_price).label('sum')).group_by(Sales.order_id).subquery()
		# data = db.session.query(sub.c.order_id, sub.c.sum).all()
		data = (db.session.query(Customers.customer_id.label('id'),func.avg(Sales.total_price).label('avg')).outerjoin(Orders,Orders.customer_id==Customers.customer_id).join(Sales,Sales.order_id==Orders.order_id).group_by(Customers.customer_id).order_by(Customers.customer_id).all())#.filter(Orders.order_date.between(datetime(2021,7,30),datetime(2021,8,30))).all())
		# data=(db.session.query(sub.c.id.label('id'), func.avg(sub.c.sum).label('avg')).join(Customers,Customers.customer_id==sub.c.id).group_by(sub.c.id).all())
		print(len(data))
		# data = (db.session.query(Customers.customer_id.label('id'),func.avg(Orders.payment).label('avg')).join(Orders,Orders.customer_id==Customers.customer_id).group_by(Customers.customer_id).filter(Orders.order_date.between(datetime(2021,7,30),datetime(2021,8,30))).all())
## order or cart bth because order payment is not a bill
		# return jsonify({'msg': 'Data Add Successfully'})
		df = pd.DataFrame(data, columns=['id', 'Avg'])
		df.to_csv('Item_Price.csv')
		return jsonify([{"id":r.id,"avg":r.avg} for r in data])

	@staticmethod
	def lavish():
		lvsish = []
		data = Products.query.all()
		for i in data:
			if i.price >= 115 and i.price <= 119:
				lvsish.append(i.product_ID)
		# data=(db.session.query(Customers.customer_id.label('id'),func.count(Sales.product_id).label('total'),func.count(Sales.product_id.in_(lvsish)).label("lavish")).join(Orders,Orders.customer_id==Customers.customer_id).join(Sales,Sales.order_id==Orders.order_id).group_by(Customers.customer_id).all())
		data=(db.session.query(Customers.customer_id.label('id'),func.count(Sales.product_id).label('total'),func.sum(
			case(
				(Sales.product_id.in_(lvsish), 1),
                else_=0
            )).label("lavish"))
			  .outerjoin(Orders,Orders.customer_id==Customers.customer_id)
			  .outerjoin(Sales,Sales.order_id==Orders.order_id).group_by(Customers.customer_id).order_by(Customers.customer_id).all())
		df = pd.DataFrame(data, columns=['id', 'total_Product', 'lavish_Product'])
		df.to_csv('lavish.csv')
		return jsonify([{"id":r.id,"total":r.total,"lavish":r.lavish} for r in data])


## avg cart price
	@staticmethod
	def avg_oder():
		sub = (db.session.query(Orders.order_id.label('id'),func.sum(Sales.total_price).label('sum')).join(Sales,Sales.order_id==Orders.order_id).group_by(Orders.order_id).subquery())
		data=(db.session.query(Customers.customer_id.label('id') ,func.avg(sub.c.sum).label('avg')).outerjoin(Orders,Customers.customer_id==Orders.customer_id).join(sub,Orders.order_id==sub.c.id).group_by(Customers.customer_id).order_by(Customers.customer_id).all())
		print(data)
		df = pd.DataFrame(data, columns=['id', 'Avg'])
		df.to_csv('Cart_Avg.csv')
		return jsonify([{"id":r.id,"avg":r.avg} for r in data])

##### Csv make final
	# @staticmethod
	# def final():
	# 	c_a=pd.read_csv('C:/Users/Faseeh-Ur-Rehman/PycharmProjects/PythonProject/FYP_Training/Cart_Avg.csv')
	# 	i_p=pd.read_csv("C:/Users/Faseeh-Ur-Rehman/PycharmProjects/PythonProject/FYP_Training/Item_Price.csv")
	# 	lavish= pd.read_csv("C:/Users/Faseeh-Ur-Rehman/PycharmProjects/PythonProject/FYP_Training/lavish.csv")
	# 	df = pd.DataFrame(columns=["id","Item_order", "Avg_cart", "Avg_Item"])
	# 	for i in range(len(lavish)):
	# 		avg_cart=c_a.index[c_a['id'] == lavish['id'][i]]
	# 		avg_cart = avg_cart[0] if len(avg_cart) > 0 else -1
	# 		if avg_cart==-1:
	# 			avg_cart=0
	# 		else:
	# 			avg_cart=c_a["Avg"][avg_cart]
	# 		avg_item = i_p.index[i_p['id'] == lavish['id'][i]]
	# 		avg_item = avg_item[0] if len(avg_item) > 0 else -1
	# 		if avg_item==-1:
	# 			avg_item=0
	# 		else:
	# 			avg_item=i_p["Avg"][avg_cart]
	# 		l_v = np.divide(lavish['lavish_Product'][i], lavish['total_Product'][i] or np.nan)
	#
	# 		# l_v=lavish['lavish_Product'][i]/lavish['total_Product'][i]
	# 		df.loc[len(df)] = [lavish['id'][i], l_v, avg_cart, avg_item]
	# 	# df.append({"id": lavish['id'][i], "Item_order":l_v,"Avg_cart": avg_cart,"Avg_Item": avg_item}, ignore_index=True)
	# 	df.to_csv('Customer.csv')
	# 	return jsonify({'msg': 'Data Add Successfully'})

	@staticmethod
	def final():
		# Read CSV files
		c_a = pd.read_csv('C:/Users/Faseeh-Ur-Rehman/PycharmProjects/PythonProject/FYP_Training/Cart_Avg.csv')
		i_p = pd.read_csv("C:/Users/Faseeh-Ur-Rehman/PycharmProjects/PythonProject/FYP_Training/Item_Price.csv")
		lavish = pd.read_csv("C:/Users/Faseeh-Ur-Rehman/PycharmProjects/PythonProject/FYP_Training/lavish.csv")
		# Empty dataframe with column names
		df = pd.DataFrame(columns=["id", "Item_order", "Avg_cart", "Avg_Item"])
		for i in range(len(lavish)):
			# Get avg_cart
			cart_idx = c_a.index[c_a['id'] == lavish['id'][i]]
			avg_cart = c_a["Avg"].iloc[cart_idx[0]] if len(cart_idx) > 0 else 0
			# Get avg_item
			item_idx = i_p.index[i_p['id'] == lavish['id'][i]]
			avg_item = i_p["Avg"].iloc[item_idx[0]] if len(item_idx) > 0 else 0
			# Calculate lavish ratio (avoid division by zero)
			total_products = lavish['total_Product'][i]
			l_v = np.divide(
				lavish['lavish_Product'][i],
				total_products if total_products != 0 else np.nan
			)
			# Add row
			df.loc[len(df)] = [lavish['id'][i], l_v, avg_cart, avg_item]
		# Save to CSV
		df.to_csv('Customer.csv', index=False)
		return jsonify({'msg': 'Data Add Successfully'})