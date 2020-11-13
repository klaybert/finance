#librerias a importar
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pandas_datareader import data
import seaborn as sns


start = "2010-1-1"
end = "2020-7-7"

# Buscamos la data del SPY y del SKEW
data_skew = yf.download("^SKEW", start=start, end=end, group_by="ticker")
data_spy = yf.download("SPY", start=start, end=end, group_by="ticker")

# Los colocamos en un dataframe unido
df = pd.DataFrame(index=data_spy.index)
df['spy']=data_spy['Close']
df['skew']=data_skew['Close']




#################################################
# Graficamos en dos partes la relacion
df[['spy','skew']].plot(subplots=True, figsize=(12,6))
plt.grid(True)
plt.show()

# Otro método de graficar, donde podemos c2docar label2
#definimos el size del plot con 12,6
fig, ax = plt.subplots(figsize=(12,6))

	#Trabajamos por el 1er plot, 211
ax = plt.subplot(211)
plt.plot(df['spy'],label='spy')
plt.grid(True)
plt.legend(loc=0)
	#Trabajamos por el 2do plot, 212
ax = plt.subplot(212)
plt.plot(df['skew'],label='CBOE skew',color='g')
plt.grid(True)
plt.legend(loc=0)
plt.show()


####################################################
#Seteamos la col date como index, y lo llamamo Date
data_skew = data_skew.reset_index()
data_skew.index = data_skew['Date']
skew_close = data_skew['Close']
skew_close = skew_close.round(2)
skew_close.tail()

#Hagamos el plot del Close del Skew
data_skew['Close'].plot(figsize = (12,6), fontsize = 12)
plt.grid(True)
plt.show()

##############################################################
# Calculando el moving average SPY, 
df['MovAvg20'] = data_spy['Close'].rolling(20).mean()
df['MovAvg50'] = data_spy['Close'].rolling(50).mean()
df['MovAvg200'] = data_spy['Close'].rolling(200).mean()
df['MovAvg300'] = data_spy['Close'].rolling(300).mean()

##############################################################
# Calculando el moving average SKEW, 
df['skew_SMA_10'] = data_skew['Close'].rolling(10).mean()
df['skew_SMA_20'] = data_skew['Close'].rolling(20).mean()
df['skew_SMA_50'] = data_skew['Close'].rolling(50).mean()
df['skew_SMA_200'] = data_skew['Close'].rolling(200).mean()


##############################################################
# Porcentaje de diferencia entre el SPY y el 200day SMA
df['diff_200sma_price'] = ((df['spy'] / df['MovAvg200'])-1 )*100

# Grafico de la dif entre 200sma vs spy
#Otro metodo de graficar, donde podemos colocar labels
fig, ax = plt.subplots(figsize=(12,6))

ax = plt.subplot(211)
plt.plot(df['spy'],label='spy')
plt.plot(df['MovAvg200'], label='200D-sma')
# plt.xlim("2020-1-1","2020-7-1")
set_xlim("2020-1-1","2020-7-1")
plt.grid(True)
plt.legend(loc=0)

ax = plt.subplot(212)
plt.plot(df['diff_200sma_price'],label='Porcentaje de separacion del 200 d-sma del spy',color='g')
plt.legend(loc=0)
# plt.xlim("2020-1-1",end)
plt.axhline(y=0, color='r', linestyle='-')
plt.grid(True)
plt.show()

###############################################################
##############################################################
# Porcentaje de diferencia entre el SPY y el 50day SMA
df['diff_50sma_price'] = ((df['spy'] / df['MovAvg50'])-1 )*100

# Grafico de la dif entre 200sma vs spy
#Otro metodo de graficar, donde podemos colocar labels
fig, ax = plt.subplots(figsize=(12,6))
ax = plt.subplot(211)
plt.plot(df['spy'],label='spy')
plt.plot(df['MovAvg50'], label='50D-sma')
plt.grid(True)
plt.legend(loc=0)

ax = plt.subplot(212)
plt.plot(df['diff_50sma_price'],label='Porcentaje de separacion del 50 d-sma del spy',color='g')
plt.legend(loc=0)
plt.axhline(y=0, color='r', linestyle='-')
plt.grid(True)
plt.show()

##############################################################
# Porcentaje de diferencia entre el SPY y el 300day SMA
df['diff_300sma_price'] = ((df['spy'] / df['MovAvg300'])-1 )*100

# Grafico de la dif entre 200sma vs spy
#Otro metodo de graficar, donde podemos colocar labels
fig, ax = plt.subplots(figsize=(12,6))
ax = plt.subplot(211)
plt.plot(df['spy'],label='spy')
plt.plot(df['MovAvg300'], label='300D-sma')
plt.grid(True)
plt.legend(loc=0)

ax = plt.subplot(212)
plt.plot(df['diff_300sma_price'],label='Porcentaje de separacion del 300 d-sma del spy',color='g')
plt.legend(loc=0)
plt.axhline(y=0, color='r', linestyle='-')
plt.grid(True)
plt.show()

#Correlacion de -X dias de los valores, muestra los ultimos dias
#
df['spy'][:-120].corr(df['skew'][:-120], method = 'pearson')
df['spy'][:-90].corr(df['skew'][:-90], method = 'pearson')
df['spy'][:-60].corr(df['skew'][:-60], method = 'pearson')
df['spy'][:-30].corr(df['skew'][:-30], method = 'pearson')
df['spy'][:-10].corr(df['skew'][:-10], method = 'pearson')




##############################################################
#Marcando buying oportunities y ploteando las zonas donde hay un deadcross entre spy y movAvg
markers = [idx for idx, close in enumerate(df['spy']) if df['MovAvg'][idx] - close >= 10]
plt.suptitle("Buying Opportunities?")
plt.plot(df['spy'],marker='D',markerfacecolor='r',markevery=markers)
plt.grid(True)
plt.show()


############################################
#Shading un area de un grafico
fig, ax = plt.subplots()
ax.plot(df['spy'], label='spy')
ax.axvspan(datetime(2000,3,1), datetime(2003,2,9), alpha=0.5, color='red')
ax.axvspan(datetime(2007,10,1), datetime(2009,2,9), alpha=0.5, color='red')
ax.axvspan(datetime(2020,2,24), datetime.today(), alpha=0.5, color='red')
plt.grid(True)
plt.show()


############################################
# test graficando varios datos en un mismo plot
fig, ax = plt.subplots()
ax.plot(df['spy'], label='spy')
ax.plot(df['MovAvg20'], label='SPY 20D Moving Average')
ax.plot(df['MovAvg50'], label='SPY 50D Moving Average')
ax.plot(df['MovAvg200'], label='SPY 200D Moving Average')
plt.suptitle("Grafico de Moving Averages del SPY")
plt.grid(True)
plt.show()

##############################################
# Graficamos dos distintos moving averages de dos datos
x=100
df['x']=100
fig, ax = plt.subplots()
# ax.plot(df['spy'], label='spy')
ax.plot(df['MovAvg20'], label='SPY 20 SMA')
ax.plot(df['skew_SMA_10'], label='Skew SMA10', color='g')
ax.plot(df['x'],label = 'recta 100', color = 'black')
plt.suptitle("Grafico de 20SMA del SPY y Skew")
plt.grid(True)
plt.show()







##############################################################
#Skew and VIX or VXX

data_skew = yf.download("^SKEW", start=start, end=end, group_by="ticker")
data_vix = yf.download("^vix", start=start, end=end, group_by="ticker")

# Los colocamos en un dataframe
df = pd.DataFrame(index=data_spy.index)
df['vix']=data_vix['Close']
df['skew']=data_skew['Close']

# Graficamos en dos partes la relacion
df[['vix','skew']].plot(subplots=True)
plt.show()

#Otro metodo de graficar, donde podemos colocar labels
fig, ax = plt.subplots(figsize=(12,6))
ax = plt.subplot(211)
plt.plot(df['vix'],label='Vix')
plt.legend(loc=0)

ax = plt.subplot(212)
plt.plot(df['skew'],label='CBOE Skew',color='g')
plt.legend(loc=0)
plt.show()