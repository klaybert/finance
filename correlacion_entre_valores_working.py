#####################################################
#CORRELACION PEARSON-R

start = "2018-1-1"
end = "2020-7-10"

#Buscando los datos del GF=C Futuros del Oro
# data_audjpy = yf.download("AUDJPY=X", start=start, end=end, group_by="ticker")
data_spy = yf.download("SPY", start=start, end=end, group_by="ticker")
data_cad = yf.download("CAD=X", start=start, end=end, group_by="ticker")
data_cad = yf.download("CAD=X", start=start, end=end, group_by="ticker")
data_gold = yf.download("GC=F", start=start, end=end, group_by="ticker")
data_skew = yf.download("^SKEW", start=start, end=end, group_by="ticker")
data_vix = yf.download("^VIX", start=start, end=end, group_by="ticker")
#data_spx = yf.download("^spx", start=start, end=end, group_by="ticker") #Este indice solo se busca 4horas



# Los colocamos en un dataframe
df = pd.DataFrame(index=data_spy.index)
df['spy']=data_spy['Close']
# df['audjpy']=data_audjpy['Close']
# df['usdcad']=data_cad['Close']
df['gold']=data_gold['Close']

#Reseteamos el index, asi que el index se convierte en numeros del 0 al n, y la fecha es parte del DF
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


