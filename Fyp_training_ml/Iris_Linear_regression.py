from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,mean_squared_error

from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
# from sklearn.preprocessing import OrdinalEncoder

data=pd.read_csv("iris.csv")
X=data.iloc[:,[2,3,4]].values
Y= data.iloc[:,[1]].values

# order = ['Iris-setosa','Iris-versicolor',"Iris-virginica"]
# ordinal_encoder = OrdinalEncoder(categories=[order])
#
# Y = ordinal_encoder.fit_transform(Y)
Y=np.ndarray.flatten(Y)
# print(Y)

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=42)

lr = LinearRegression()
lr.fit(X_train,Y_train)
pre=lr.predict(X_test)

print(mean_squared_error(Y_test,pre))



