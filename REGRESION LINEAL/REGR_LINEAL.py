import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# INPORTANDO ARCHIVO
url = 'data/BuildingData.csv'
df = pd.read_csv(url)

# SE HACE ESO POR QUE AL QUERER SABER LA COLUMNA CON MEJOR COORELACION TIENE QUE SER NUMERICAS
mapeo = {'yes': 1, 'no': 0, 'unfurnished': 0, 'semi-furnished': 1, 'furnished': 2}
df = df.replace(mapeo)
# print(df.head(3))

# SABIENDO COLUMNA CON MEJOR COORELACION
coorelacion = df.corr()['stories'].drop('stories')
mejor = coorelacion.idxmax()
# print(f'\nCOORELACION:\n\n{coorelacion}')
# COLUNMA CON MEJOR COORELACION CON EL NUMERO DE PISOS
print('\nCOLUMNA CON MEJOR COORELACION')
print(f'MEJOR: {mejor}\n')

plt.scatter(df.stories,df.height, color='cornflowerblue')

X = df.stories.values
X= X.reshape(-1,1)
y = df.height.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 50)

regresion = LinearRegression()
regresion.fit(X_train, y_train)

y_pred = regresion.predict(X_test)

data = [Line2D([0], [0], color = 'slateblue', lw = 3, label = 'predict'),
        Line2D([0], [0], marker = 'o', color = 'cornflowerblue', label = 'default', markerfacecolor = None, markersize = 8),
        Line2D([0], [0], marker = 'o', color = 'indianred', label = 'train', markersize = 8)]

plt.scatter(X_train, y_train, color = 'indianred')
plt.plot(X_train,regresion.predict(X_train), color = 'slateblue', linewidth = 2)
plt.legend(handles = data)

plt.title ('EDIFICIO')
plt.xlabel ('stories')
plt.ylabel ('height')
plt.show()

mse = mean_squared_error(y_true = y_test, y_pred = y_pred)
rmse = np.sqrt(mse)

print(f'ERROR CUADRATICO MEDIO (MSE): {str(mse)}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO (RMSE): {str(rmse)}')
print(f'R2_SCORE: {r2_score(y_test,y_pred)}\n')