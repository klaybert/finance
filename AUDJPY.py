import yfinance as yf
start = "2020-1-1"
end = "2020-7-9"

# data_AUDJPY = yf.download("AUDJPY=X", start=start, end=end, group_by="ticker", interval = "1d")
data_AUDJPY = yf.download("AUDJPY=X", start=start, end=end, group_by="ticker")
data_spy = yf.download("SPY", start=start, end=end, group_by="ticker")
AUDJPY_close = data_gold['Close']

#Resetamos el index (date) a ser parte del dataframe
data_AUDJPY = data_AUDJPY.reset_index()

#Y seteamos el Date como el index
data_AUDJPY.index = data_AUDJPY['Date']

#Redondeamos los valores generales y de close a 2
AUDJPY_close = AUDJPY_close.round(2)
data_AUDJPY = data_AUDJPY.round(2)
#Buscamos valores nulos
AUDJPY_close.isnull().sum()

#Si los posee, hacemos el drop de dichos valores 
AUDJPY_close.dropna(inplace = True, axis = 0)

# relacion entre SPY y AUDJPY
df = pd.DataFrame(index=data_spy.index)
df['spy']=data_spy['Close']
df['AUDJPY']=data_AUDJPY['Close']

###################################################
# Extraemos el precio de cierre combinados para calcular correlacion, recordar que los dates son importantes

import pandas_datareader.data as web
start = "2019-1-1"
# end = start-timedelta(days=7) 
end = "2020-7-2"

stock_a='spy'
# stock_b='AUDJPY=X'
# stock_b='^XDN'
stock_b='^vix'
combined_df = web.DataReader([stock_a,stock_b], 'yahoo', start = start, end = end)['Adj Close']

#Hacemos la revision de los null  o NULL values
combined_df.dropna(inplace = True, axis = 0)
combined_df.round(2)
combined_df.head()

# Analicemos ahora la correlacion entre los datos que tenemos en combined_df
#Guardemos el Daily return de la combined_df en un nuevo dataframe
pct_chg_df = combined_df.pct_change()*100
#quitamos los na
pct_chg_df.dropna(inplace = True, how = 'any', axis = 0)
#hacemos el plot cruzado de scatter y histograma
import seaborn as sns
sns.set(style = 'ticks', font_scale = 1.25)
sns.pairplot(pct_chg_df)
plt.show()

#Joinplots Graficos de scatter e histogramas, resultado la correlacion, y el pvalue
# PearsonR es el valor de la correlacion, y p-value es 
from scipy.stats import stats
# sns.jointplot('SPY', '^VIX', pct_chg_df, kind='scatter').annotate(stats.pearsonr)
sns.jointplot(stock_a, stock_b, pct_chg_df, kind='scatter').annotate(stats.pearsonr)
# sns.jointplot('EURUSD=X', 'AUDJPY=X', pct_chg_df, kind='scatter').annotate(stats.pearsonr)
plt.show()



#####################################################
#CORRELACION PEARSON-R

start = "2018-1-1"
end = "2020-7-10"

#Buscando los datos del GF=C Futuros del Oro
# data_audjpy = yf.download("AUDJPY=X", start=start, end=end, group_by="ticker")
data_spy = yf.download("SPY", start=start, end=end, group_by="ticker")
# data_cad = yf.download("CAD=X", start=start, end=end, group_by="ticker")
data_gold = yf.download("GC=F", start=start, end=end, group_by="ticker")
# data_spx = yf.download("^spx", start=start, end=end, group_by="ticker") #Este indice solo se busca 4horas



# Los colocamos en un dataframe
df = pd.DataFrame(index=data_spy.index)
df['spy']=data_spy['Close']
# df['audjpy']=data_audjpy['Close']
# df['usdcad']=data_cad['Close']
df['gold']=data_gold['Close']

#REseteamos el index, asi que el index se convierte en numeros del 0 al n, y la fecha es parte del DF
df = df.reset_index()

# df['spx'] = data_spx['Close']
df.isnull().sum()
df.dropna(axis = 0, inplace = True)
# 
#Daily change
df['Spy_Day_Chg'] = df['spy'].pct_change()*100
df['audjpy_Day_Chg'] = df['audjpy'].pct_change()*100
df['usdcad_Day_Chg'] = df['usdcad'].pct_change()*100
df['gold_Day_Chg'] = df['gold'].pct_change()*100
df.isnull().sum()
df.dropna(axis = 0, inplace = True)

# Correlacion de daily changes
df['Spy_Day_Chg'].corr(df['audjpy_Day_Chg'], method = 'pearson')
df['usdcad_Day_Chg'].corr(df['audjpy_Day_Chg'], method = 'pearson')


#Correlacion de los precios de toda la serie
df['spy'].corr(df['audjpy'], method = 'pearson')
df['spy'][:-90].corr(df['audjpy'][:-90], method = 'pearson')
df['spy'][:-90].corr(df['gold'][:-90], method = 'pearson')
# df['spx'][:-90].corr(df['audjpy'][:-90], method = 'pearson')
# df['usdcad'].corr(df['audjpy'], method = 'pearson')


#################################################
# Correlaciones del SPY con el Futuro del gold [inicio:fin] concuerda excel, pero no es la serie. La serie viene con el loop for mas abajo
df['spy'][-10:].corr(df['gold'][-10:], method = 'pearson')
df['spy'][-30:].corr(df['gold'][-30:], method = 'pearson')
df['spy'][-50:].corr(df['gold'][-50:], method = 'pearson')
df['spy'][-90:].corr(df['gold'][-90:], method = 'pearson')


#################################################################
# Funcional
# Correlacion de la serie para 10 dias
correl = {}
j=0
for i in df.index:
    # df['correl_spy_gold'][j:j+1] = df['spy'][j-10:j].corr(df['gold'][j-10:j], method = 'pearson')
    correl[j]=df['spy'][j-90:j].corr(df['gold'][j-90:j], method = 'pearson')
    j = j+1
#################################################################
# Convertimos a DF

df_correl = pd.DataFrame(correl.items())
df_correl.columns = ['index', '10D_spy_gold_corr']
# df_correl = pd.concat([df_correl, df_correl], axis=1, sort=False)

df_correl30 = pd.DataFrame(correl.items())
df_correl30.columns = ['index', '30D_spy_gold_corr']
df_correl = pd.concat([df_correl, df_correl30], axis=1, sort=False)

df_correl50 = pd.DataFrame(correl.items())
df_correl50.columns = ['index', '50D_spy_gold_corr']
df_correl = pd.concat([df_correl, df_correl50], axis=1, sort=False)

df_correl90 = pd.DataFrame(correl.items())
df_correl90.columns = ['index', '90D_spy_gold_corr']
df_correl = pd.concat([df_correl, df_correl90], axis=1, sort=False)

# Concatenar todos los data frames
df_total = pd.concat([df, df_correl], axis=1, sort=False)
df_total.dropna(axis = 0, inplace = True)
################################################
#graficas de las series de correlacion

fig, ax = plt.subplots(figsize=(12,6))

	#Trabajamos por el 1er plot, 211
ax = plt.subplot(211)
plt.plot(df_total['spy'],label='spy') #SPY
plt.grid(True)
plt.legend(loc=0)
	#Trabajamos por el 2do plot, 212
ax = plt.subplot(212)
plt.plot(df_total['10D_spy_gold_corr'],label='10D Correlacion entre spy y gold',color='g')
plt.grid(True)
plt.legend(loc=0)
plt.show()














# Add a new column to DF
# df1.loc[:,'f'] = pd.Series(np.random.randn(sLength), index=df1.index)
# result = pd.concat([df1, df4], axis=1, sort=False)

# Esto funciona
# >>> df['spy'][10:20].corr(df['gold'][10:20], method = 'pearson')

#Correlacion de -X dias de los valores, muestra los ultimos dias
#REVISAR NO ME SALE EL FOR
df['usdcad'][:-90].corr(df['audjpy'][:-90], method = 'pearson')






















d = {-90, -60, -45, -30, -10} #lista
d = map(int, d) #Convertimos los strings a integers
# d_df = pd.DataFrame(d)
# d_df.columns = ['dias']

df_correl = []

for i=10 in df.index:
	    df['correl_spy_gold_10'] = df['spy'][-10:i].corr(df['gold'][-10:i], method = 'pearson')
df_correl

	# df_correl['corr'] = df['spy'][d_df['dias']:].corr(df['audjpy'][d_df['dias']:], method = 'pearson')
	# df_correl['corr'] = df['spy'][d_df['dias']:i].corr(df['audjpy'][d_df['dias']:i], method = 'pearson')
	    # df_correl['corr_gold'] = df['spy'][-10:i].corr(df['gold'][-10:i], method = 'pearson')


#################################################################
# Funcional
# Correlacion de la serie para 10 dias
j=0
for i in df.index:
    df['correl_spy_gold_10'][j] = df['spy'][j:j+10].corr(df['gold'][j:j+10], method = 'pearson')
    j = j+1

j=0
for i in df.index:
    df[j:j+1]
    j = j+1
j=1
df['correl_spy_gold_10'][j:j+10] = df['spy'][j:j+10].corr(df['gold'][j:j+10], method = 'pearson')
    



# pruebas de fechas MEJORAR
from datetime import datetime, timedelta
days_to_subtract=10
start="2020-6-30"
d = start - timedelta(days=days_to_subtract)
print(d)