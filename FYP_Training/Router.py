from flask import request, jsonify
from FYP_Training.Controllers1.Customers import CustomerControllers
from FYP_Training.Controllers1.Products import ProductControllers
from FYP_Training.Controllers1.Orders import OrderControllers
from FYP_Training.Controllers1.Sales import SalesControllers
# from FYP_Training.Controllers1.Products import ProductController
from FYP_Training.db import db, app

# @app.route('/showcart/<id>')
# def show_product(id):
# 	return ProductController.showcart(id)
#
# @app.route('/count3')
# def count3():
# 	return ProductController.count3()
#
# @app.route('/viewcart/<id>')
# def show_prod(id):
# 	return ProductController.viewcart(id)
#
# @app.route('/findname/<id>')
# def cart_all(id):
# 	return ProductController.cart_all(id)

@app.route('/register', methods=['POST'])
def register_customer():
	return CustomerControllers.register()
	# return jsonify({'message': 'Register a new customer'})

@app.route('/product_reg', methods=['POST'])
def register_Product():
	return ProductControllers.product_reg()

@app.route('/oder_reg', methods=['POST'])
def register_order():
	return OrderControllers.order_reg()

@app.route('/sale_reg', methods=['POST'])
def register_sale():
	return SalesControllers.sale_reg()

@app.route('/avg_cus')
def cus_avg():
	return CustomerControllers.final()

# @app.route('/profile', methods=['GET'])
# def view_profile():
# 	return CustomerController.get_profile()
#
# @app.route('/profile', methods=['PUT'])
# def update_profile():
#     return jsonify({'message': 'Update customer profile'})
#
# @app.route('/profile/password', methods=['PUT'])
# def change_password():
#     return jsonify({'message': 'Change password'})
#
# @app.route('/account', methods=['DELETE'])
# def delete_account():
#     return jsonify({'message': 'Delete account'})
#
# @app.route('/products', methods=['GET'])
# def list_products():
#     return jsonify({'message': 'List all products'})
#
# @app.route('/products/<int:product_id>', methods=['GET'])
# def view_product(product_id):
#     return jsonify({'message': f'View product {product_id}'})
#
# @app.route('/products', methods=['POST'])
# def add_product():
#     return jsonify({'message': 'Add new product (admin)'})
#
# @app.route('/products/<int:product_id>', methods=['PUT'])
# def update_product(product_id):
#     return jsonify({'message': f'Update product {product_id} (admin)'})
#
# @app.route('/products/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     return jsonify({'message': f'Delete product {product_id} (admin)'})
#
# @app.route('/products/search/<term>', methods=['GET'])
# def search_products(term):
#     return jsonify({'message': f'Search products by term: {term}'})
#
# @app.route('/products/category/<cat>', methods=['GET'])
# def filter_by_category(cat):
#     return jsonify({'message': f'Filter products by category: {cat}'})
#
# # ------------------ Cart Routes ------------------
#
# @app.route('/cart/add', methods=['POST'])
# def add_to_cart():
#     return jsonify({'message': 'Add item to cart'})
#
# @app.route('/cart', methods=['GET'])
# def view_cart():
#     return jsonify({'message': 'View cart'})
#
# @app.route('/cart/update/<int:item_id>', methods=['PUT'])
# def update_cart_item(item_id):
#     return jsonify({'message': f'Update item {item_id} quantity in cart'})
#
# @app.route('/cart/remove/<int:item_id>', methods=['DELETE'])
# def remove_cart_item(item_id):
#     return jsonify({'message': f'Remove item {item_id} from cart'})
#
# @app.route('/cart/clear', methods=['DELETE'])
# def clear_cart():
#     return jsonify({'message': 'Clear cart'})
#
#
# @app.route('/checkout', methods=['POST'])
# def checkout():
#     return jsonify({'message': 'Place order from cart'})
#
# @app.route('/orders', methods=['GET'])
# def view_orders():
#     return jsonify({'message': 'View all orders'})
#
# @app.route('/orders/<int:order_id>', methods=['GET'])
# def view_order(order_id):
#     return jsonify({'message': f'View order {order_id}'})
#
# @app.route('/orders/<int:order_id>', methods=['DELETE'])
# def cancel_order(order_id):
#     return jsonify({'message': f'Cancel order {order_id}'})



if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy import text
# from FYP_Training.Model.Customer import Customer
# from FYP_Training.Model.Cart import Cart
# from FYP_Training.Model.CartItem import CartItem
# from FYP_Training.Model.Product import Product
# from FYP_Training.Model.Order import Order
# from FYP_Training.Model.OrderItem import OrderItem

# if __name__ == '__main__':
#     with app.app_context():
#         try:
#             db.session.execute(text('SELECT 1'))
#             print("✅ Database connection established successfully.")
#         except SQLAlchemyError as e:
#             print("❌ Database connection failed:", e)
#         db.create_all()
#         print("✅ Tables created successfully (or already exist).")
#     app.run(debug=True)