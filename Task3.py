import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

data = pd.read_csv('prices_hist.txt', header=None) # считываем данные из файла
data.columns = ['Price']
data.index = pd.DatetimeIndex(freq='d', start='2000-01-01', periods=1000)
ts = data['Price']
#print(ts.head())
#plt.plot(ts)

ts_diff = ts - ts.shift() # вычисляется первая разность
ts_diff.dropna(inplace=True) # удаляются нулевые элементы
#plt.plot(ts_diff)

#Тест Дики-Фуллера для проверки на стационарность
from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
#test_stationarity(ts)
#test_stationarity(ts_diff)

'''
# построение графиков автокорреляций и частичных автокорреляций
plt.figure(1)
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(ts_diff, lags=100, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(ts_diff, lags=100, ax=ax2)
'''

model = sm.tsa.ARIMA(ts, order=(2,1,0)) # построение модели
fit = model.fit(method="mle")
print(fit.summary()) # вывод характеристик построенной модели
#sm.qqplot(fit.resid, line='q')
#sm.graphics.tsa.plot_acf(fit.resid)

insample_predict = fit.predict(typ='levels') # прогноз 
ospredict = fit.predict(start=1000, end=1400, typ='levels') # прогноз на будущее

plt.plot(ts) # исходный ряд
plt.plot(insample_predict) # прогноз
plt.plot(ospredict) # прогноз на будущее

# M[Price_end]=313.46121 (T=1400)
# Low=246.26121 (T=1400) 95%
# high=445.46121 (T=1400) 95%

