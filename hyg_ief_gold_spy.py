#####################################################
#CORRELACION PEARSON-R

start = "2017-1-1"
end = "2020-9-4"

#Buscando los datos del GF=C Futuros del Oro
# data_audjpy = yf.download("AUDJPY=X", start=start, end=end, group_by="ticker")
data_spy = yf.download("SPY", start=start, end=end, group_by="ticker")
data_cad = yf.download("CAD=X", start=start, end=end, group_by="ticker")
data_gold = yf.download("GC=F", start=start, end=end, group_by="ticker")
data_AUDJPY = yf.download("AUDJPY=X", start=start, end=end, group_by="ticker")
data_skew = yf.download("^SKEW", start=start, end=end, group_by="ticker")
data_vix = yf.download("^VIX", start=start, end=end, group_by="ticker")
data_hyg = yf.download("hyg", start=start, end=end, group_by="ticker")
data_ief = yf.download("ief", start=start, end=end, group_by="ticker")# ishares 7-10 treasury Bond fed
#data_spx = yf.download("^spx", start=start, end=end, group_by="ticker") #Este indice solo se busca 4horas



# Los colocamos en un dataframe
df = pd.DataFrame(index=data_spy.index)
df['spy']=data_spy['Close']
df['cad']=data_cad['Close']
df['gold']=data_gold['Close']
df['AUDJPY']=data_AUDJPY['Close']
df['skew']=data_skew['Close']
df['vix']=data_vix['Close']
df['hyg']=data_hyg['Close']
df['ief']=data_ief['Close']
# df['usdcad']=data_cad['Close']

#Reseteamos el index, asi que el index se convierte en numeros del 0 al n, y la fecha es parte del DF
df = df.reset_index()

# df['spx'] = data_spx['Close']
df.isnull().sum()
df.dropna(axis = 0, inplace = True) #drop valores ausente (axis = 0 es fila, mientras que axis = 1 es columna)

#division entre hyg e ief (referencia kerb)
df['hyg_ief'] = df['hyg']/df['ief']


#Analisis exploratorio de datos, EDA, matriz de dispersion 
import matplotlib.pyplot as plt
import seaborn as sns

cols = ['spy', 'cad', 'gold', 'AUDJPY', 'skew', 'vix']
cols = ['spy', 'gold', 'hyg_ief']

sns.pairplot(df[cols], size=1.2)
plt.tight_layout()
# plt.savefig('images/10_03.png', dpi=300)
plt.show()


###########################################################
#Ahora realizaremos un mapa de calor de cols
cm = np.corrcoef(df[cols].values.T)
#sns.set(font_scale=1.5)
hm = sns.heatmap(cm,
                 cbar=True,
                 annot=True,
                 square=True,
                 fmt='.2f',
                 annot_kws={'size': 11},
                 yticklabels=cols,
                 xticklabels=cols)

plt.tight_layout()
# plt.savefig('images/10_04.png', dpi=300)
plt.show()





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


#################################################
# Correlaciones del Gold con ratio hyg_ief [inicio:fin] concuerda excel, pero no es la serie. La serie viene con el loop for mas abajo
df['hyg_ief'][-10:].corr(df['gold'][-10:], method = 'pearson')
df['hyg_ief'][-30:].corr(df['gold'][-30:], method = 'pearson')
df['hyg_ief'][-50:].corr(df['gold'][-50:], method = 'pearson')
df['hyg_ief'][-90:].corr(df['gold'][-90:], method = 'pearson')



#################################################################
# Funcional
# Correlacion de la serie para X dias
correl = {}
j=0
for i in df.index:
    # df['correl_spy_gold'][j:j+1] = df['spy'][j-10:j].corr(df['gold'][j-10:j], method = 'pearson')
    correl[j]=df['hyg_ief'][j-100:j].corr(df['gold'][j-100:j], method = 'pearson')
    j = j+1
#################################################################
# Convertimos a DF

df_correl = pd.DataFrame(correl.items())
df_correl.columns = ['index', '10D_hyg_ief_gold_corr']
# df_correl = pd.concat([df_correl, df_correl], axis=1, sort=False)

df_correl21 = pd.DataFrame(correl.items())
df_correl21.columns = ['index', '21D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl21], axis=1, sort=False)

df_correl30 = pd.DataFrame(correl.items())
df_correl30.columns = ['index', '30D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl30], axis=1, sort=False)

df_correl50 = pd.DataFrame(correl.items())
df_correl50.columns = ['index', '50D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl50], axis=1, sort=False)

df_correl70 = pd.DataFrame(correl.items())
df_correl70.columns = ['index', '70D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl70], axis=1, sort=False)

df_correl90 = pd.DataFrame(correl.items())
df_correl90.columns = ['index', '90D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl90], axis=1, sort=False)

df_correl100 = pd.DataFrame(correl.items())
df_correl100.columns = ['index', '100D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl100], axis=1, sort=False)
df['MovAvg100_hyg_ief'] = df_correl['100D_hyg_ief_gold_corr'].rolling(100).mean()


df_correl150 = pd.DataFrame(correl.items())
df_correl150.columns = ['index', '150D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl150], axis=1, sort=False)

df_correl200 = pd.DataFrame(correl.items())
df_correl200.columns = ['index', '200D_hyg_ief_gold_corr']
df_correl = pd.concat([df_correl, df_correl200], axis=1, sort=False)



# Concatenar todos los data frames
df_total = pd.concat([df, df_correl], axis=1, sort=False)
df_total.dropna(axis = 0, inplace = True)
################################################
#graficas de las series de correlacion

fig, ax = plt.subplots(figsize=(12,8))

	#Trabajamos por el 1er plot, 211
ax = plt.subplot(311)
plt.plot(df_total['spy'],label='spy') #SPY
plt.grid(True)
plt.legend(loc=0)
	#Trabajamos por el 2do plot, 212

ax = plt.subplot(312)
plt.plot(df_total['gold'],label='gold',color='red')
plt.grid(True)
plt.legend(loc=0)

ax = plt.subplot(313)
plt.plot(df_total['50D_hyg_ief_gold_corr'],label='50D Correlacion entre hyg_ief y gold',color='blue')
plt.grid(True)
plt.legend(loc=0)

plt.show()






################################################################################
# Hagamos el plot de HYG/IEF y su media movil de 100sma
# Calculemos la media movil de HYG/IEF
df_t = pd.DataFrame(index=data_spy.index)
df_t['spy']=data_spy['Close']
df_t['cad']=data_cad['Close']
df_t['gold']=data_gold['Close']
df_t['AUDJPY']=data_AUDJPY['Close']
df_t['skew']=data_skew['Close']
df_t['vix']=data_vix['Close']
df_t['hyg']=data_hyg['Close']
df_t['ief']=data_ief['Close']

df_t.isnull().sum()
df_t.dropna(axis = 0, inplace = True) #drop valores ausente (axis = 0 es fila, mientras que axis = 1 es columna)

# df_t = df_t.drop(['SMA100_hyg_ief'], axis=1) Aqui me habia equivocado, eliminar una col de df_t

#division entre hyg e ief (referencia kerb)
df_t['hyg_ief'] = df_t['hyg']/df_t['ief']
# Movin average 100sma
df_t['SMA100_hyg_ief'] = df_t['hyg_ief'].rolling(100).mean()
df_t['SMA100_spy'] = df_t['spy'].rolling(100).mean()


# Correlaciones del HYG/IEF vs SPY [inicio:fin] concuerda excel, pero no es la serie. La serie viene con el loop for mas abajo
df_t['hyg_ief'][-10:].corr(df_t['spy'][-10:], method = 'pearson')
df_t['hyg_ief'][-30:].corr(df_t['spy'][-30:], method = 'pearson')
df_t['hyg_ief'][-50:].corr(df_t['spy'][-50:], method = 'pearson')
df_t['hyg_ief'][-90:].corr(df_t['spy'][-90:], method = 'pearson')

# Correlaciones de los moving average HYG/IEF vs SPY [inicio:fin] concuerda excel, pero no es la serie. La serie viene con el loop for mas abajo
df_t['SMA100_hyg_ief'][-10:].corr(df_t['SMA100_spy'][-10:], method = 'pearson')
df_t['SMA100_hyg_ief'][-30:].corr(df_t['SMA100_spy'][-30:], method = 'pearson')
df_t['SMA100_hyg_ief'][-50:].corr(df_t['SMA100_spy'][-50:], method = 'pearson')
df_t['SMA100_hyg_ief'][-90:].corr(df_t['SMA100_spy'][-90:], method = 'pearson')



df_t = df_t.reset_index()
#################################################################
# Funcional
# Correlacion de la serie para X dias
correl = {}
j=0
for i in df_t.index:
    # df['correl_spy_gold'][j:j+1] = df['spy'][j-10:j].corr(df['gold'][j-10:j], method = 'pearson')
    correl[j]=df_t['gold'][j-100:j].corr(df_t['hyg_ief'][j-100:j], method = 'pearson')
    j = j+1
#################################################################
# Convertimos a DF


df_correl = pd.DataFrame(correl.items())
df_correl.columns = ['index', '10D_spy_hyg_eif_corr']

df_correl30 = pd.DataFrame(correl.items())
df_correl30.columns = ['index', '30D_spy_hyg_eif_corr']
df_correl = pd.concat([df_correl, df_correl30], axis=1, sort=False)

df_correl90 = pd.DataFrame(correl.items())
df_correl90.columns = ['index', '90D_spy_hyg_eif_corr']
df_correl = pd.concat([df_correl, df_correl90], axis=1, sort=False)


df_correl100 = pd.DataFrame(correl.items())
df_correl100.columns = ['index', '100D_spy_hyg_eif_corr']
df_correl = pd.concat([df_correl, df_correl100], axis=1, sort=False)

#####
# Nueva, correlacion con el precio futuros - Oro
df_correl100_gold = pd.DataFrame(correl.items())
df_correl100_gold.columns = ['index', '100D_gold_hyg_eif_corr']
df_correl = pd.concat([df_correl, df_correl100_gold], axis=1, sort=False)


#contamos los valores nuelos
df_correl.isnull().sum()

df_correl.dropna(axis = 0, inplace = True)

df_total_1 = pd.concat([df_t, df_correl], axis=1, sort=False)
df_total_1.isnull().sum()

df_total_1.dropna(axis = 0, inplace = True)


#########################################################
# GRAFICAS


# # grafica 1 - Graficamos en dos partes la relacion
# df_t[['hyg_ief','SMA100_hyg_ief']].plot(subplots=False, figsize=(12,6))
# plt.grid(True)
# plt.show()


# Grafica 2 - Graficando varios datos en un mismo plot
# xlim=["2018-06-01", "2019-08-31"]
fig, ax = plt.subplots(figsize=(12, 8))
ax.set(xlabel="Date",
       ylabel="Rango Y",
       title="Relacion HYG/IEF vs 100SMD")
#        xlim=["2018-6-1", "2019-8-31"])
# ax.plot(df_t['spy'], label='spy')
ax.plot(df_t['hyg_ief'], label='Relación HYG/IEF')
ax.plot(df_t['SMA100_hyg_ief'], label='HYG 100D Moving Average')
# ax.plot(df_t['MovAvg200'], label='SPY 200D Moving Average')
# plt.suptitle("Grafico de HYG/IEF vs 100 Moving Average")
plt.grid(True)
plt.show()



#graficamos ahora dos plot en uno
# Grafico de la dif entre 200sma vs spy
#Otro metodo de graficar, donde podemos colocar labels
fig, ax = plt.subplots(figsize=(12,6))
ax = plt.subplot(211)
plt.plot(df_t['spy'],label='spy')
plt.plot(df_t['SMA100_spy'], label='100SMA del spy')
# plt.plot(df_t['MovAvg300'], label='300D-sma')
plt.grid(True)
plt.legend(loc=0)

ax = plt.subplot(212)
plt.plot(df_t['hyg_ief'],label='Relación HYG/IEF')
plt.plot(df_t['SMA100_hyg_ief'],label='HYG 100D Moving Average')
# plt.legend(loc=0)
# plt.axhline(y=0, color='r', linestyle='-')
plt.grid(True)
plt.show()



#graficamos ahora dos plot en uno
# Grafico de CORRELACIONES
#Otro metodo de graficar, donde podemos colocar labels
fig, ax = plt.subplots(figsize=(12,6))
ax = plt.subplot(311)
ax.plot(df_total_1['spy'],label='spy')
ax.plot(df_total_1['SMA100_spy'], label='100SMA del spy', color = 'blue')
# plt.plot(df_t['MovAvg300'], label='300D-sma')
plt.grid(True)
plt.legend(loc=0)

# ax1= ax.twinx() #instancia un segundo eje que comparte el eje X

ax = plt.subplot(312)

# ax.plot(df_correl['100D_gold_hyg_eif_corr'],label='correlacion 100D de SPY vs HYG/IEF', color='black')
ax.plot(df_total_1['hyg_ief'],label='Relación HYG/IEF', color='green')
# ax1= ax.twinx()
ax.plot(df_total_1['SMA100_hyg_ief'],label='HYG 100D Moving Average')
plt.grid(True)
plt.legend(loc=0)

ax = plt.subplot(313)
plt.plot(df_total_1['100D_gold_hyg_eif_corr'],label='correlacion 100D de SPY vs HYG/IEF')
# plt.plot(df_correl['90D_spy_hyg_eif_corr'],label='correlacion 90D de SPY vs HYG/IEF')
plt.grid(True)
plt.legend(loc=0)



plt.show()



