# def stock_portfolio_tracker():
# 	# Hardcoded stock prices
# 	stock_prices = {
# 		"AAPL": 180.50,
# 		"TSLA": 250.75,
# 		"GOOGL": 135.20,
# 		"MSFT": 330.40,
# 		"AMZN": 145.60
# 	}
#
# 	portfolio = {}
# 	total_investment = 0
#
# 	print("📈 Stock Portfolio Tracker")
# 	print("Available stocks:", ", ".join(stock_prices.keys()))
#
# 	while True:
# 		print("\n1. Add stock to portfolio")
# 		print("2. View portfolio")
# 		print("3. Calculate total investment")
# 		print("4. Save portfolio to file")
# 		print("5. Exit")
#
# 		choice = input("Enter your choice (1-5): ")
#
# 		if choice == '1':
# 			stock_name = input("Enter stock symbol: ").upper()
# 			if stock_name not in stock_prices:
# 				print("Invalid stock symbol!")
# 				continue
#
# 			try:
# 				quantity = int(input("Enter quantity: "))
# 				if quantity <= 0:
# 					print("Quantity must be positive!")
# 					continue
#
# 				portfolio[stock_name] = quantity
# 				print(f"Added {quantity} shares of {stock_name}")
#
# 			except ValueError:
# 				print("Please enter a valid number!")
#
# 		elif choice == '2':
# 			if not portfolio:
# 				print("Portfolio is empty!")
# 			else:
# 				print("\nYour Portfolio:")
# 				for stock, quantity in portfolio.items():
# 					price = stock_prices[stock]
# 					value = price * quantity
# 					print(f"{stock}: {quantity} shares @ ${price:.2f} = ${value:.2f}")
#
# 		elif choice == '3':
# 			total_investment = sum(portfolio[stock] * stock_prices[stock] for stock in portfolio)
# 			print(f"\n💰 Total Investment Value: ${total_investment:.2f}")
#
# 		elif choice == '4':
# 			if not portfolio:
# 				print("Portfolio is empty!")
# 				continue
#
# 			filename = input("Enter filename (without extension): ")
# 			filename += ".txt"
#
# 			try:
# 				with open(filename, 'w') as file:
# 					file.write("Stock Portfolio Summary\n")
# 					file.write("=" * 25 + "\n")
# 					for stock, quantity in portfolio.items():
# 						price = stock_prices[stock]
# 						value = price * quantity
# 						file.write(f"{stock}: {quantity} shares @ ${price:.2f} = ${value:.2f}\n")
#
# 					file.write(f"\nTotal Investment: ${total_investment:.2f}\n")
#
# 				print(f"Portfolio saved to {filename}")
#
# 			except Exception as e:
# 				print(f"Error saving file: {e}")
#
# 		elif choice == '5':
# 			print("Thank you for using Stock Portfolio Tracker!")
# 			break
#
# 		else:
# 			print("Invalid choice! Please enter 1-5.")
#
#
# if __name__ == "__main__":
# 	stock_portfolio_tracker()

from werkzeug.security import generate_password_hash

print(generate_password_hash("pass123", method='scrypt'))