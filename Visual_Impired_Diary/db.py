from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL

app = Flask(__name__)

connection_url = URL.create(
    drivername="mssql+pyodbc",
    username="sa",
    password="123",
    host="DESKTOP-58B8CB8\\VE_SERVER",
    database="test_virtualimpired",
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