# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.engine import URL
#
# app = Flask(__name__)
#
# # ✅ Replace the values below with your actual SQL Server configuration
# connection_url = URL.create(
#     drivername="mssql+pyodbc",
#     username="sa",              #
#     password="123",
#     host="DESKTOP-58B8CB8\\VE_SERVER",
#     database="Shop",
# 	query={
# 		"driver": "ODBC Driver 18 for SQL Server",
# 		"Encrypt": "no",  # <== disables encryption
# 		"TrustServerCertificate": "yes"  # <== bypasses certificate trust check
# 	}
# )
#
# app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# Model = db.Model

#########################33
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL

app = Flask(__name__)

connection_url = URL.create(
    drivername="mssql+pyodbc",
    username="sa",
    password="123",
    host="DESKTOP-58B8CB8\\VE_SERVER",
    database="Shop",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Encrypt": "no",
        "TrustServerCertificate": "yes"
    }
)

app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Model = db.Model

###########################
###########################
# #
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.engine import URL
#
# app = Flask(__name__)
#
# connection_url = URL.create(
#     drivername="mssql+pyodbc",
#     username="sa",
#     password="123",
#     host="DESKTOP-58B8CB8\\VE_SERVER",
#     database="Shop",
#     query={
#         "driver": "ODBC Driver 18 for SQL Server",
#         "Encrypt": "no",
#         "TrustServerCertificate": "yes"
#     }
# )
#
# app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# Model = db.Model
