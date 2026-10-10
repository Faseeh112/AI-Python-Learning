from flask import request,render_template
class Product:
	@staticmethod
	def show_table():
		data = request.get_json()
		product_list = list(data.values())
		return render_template("index.html", data=product_list)