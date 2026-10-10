from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from sqlalchemy.sql.operators import endswith_op
from sqlalchemy.testing import startswith_

# from sklearn.preprocessing import

data=pd.read_csv("unilever_pakistan_fake_sales.csv")
X=data.iloc[:,[0,1]].values
Y= data.iloc[:,[2]].values
Y=np.ndarray.flatten(Y)
print(X)
print(Y)

p_d=[]
p_y=[]
for i in range(len(X)):
	if ((X[i][1].startswith('May') or X[i][1].startswith('June') or X[i][1].startswith('July') or X[i][1].startswith('Aug')) and (X[i][1].endswith('24') or X[i][1].endswith('25'))):
		p_d.append(X[i])
		p_y.append(Y[i])