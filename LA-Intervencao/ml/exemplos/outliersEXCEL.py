import numpy as np
import pandas as pd
import math

coluna = 'a'

valores = np.array([501,504,493,499,497,503,525,495,506,502])
df = pd.DataFrame(valores, columns=['a'])

#print(df['a'].describe())
#print(df['a'].quantile([0.25,0.5,0.75]))

media = np.average(valores)

quartil1 = df['a'].quantile([0.25]).values[0]
quartil3 = df['a'].quantile([0.75]).values[0]

# Interquartil 
iqt = quartil3 - quartil1

lsup = math.trunc(media + (1.5 * iqt))
linf = math.trunc(media - (1.5 * iqt))

print(valores)
print('----------------------------------------------------------------------')
print('Media ' + str(media))
print('Q1 ' + str(quartil1))
print('Q3 ' + str(quartil3))
print('IQR ' + str(iqt))
print('L-Sup ' + str(lsup))
print('L-Inf ' + str(linf))

print('----------------------------------------------------------------------')

resulInfo = df[coluna][df[coluna] < linf]
resultSup = df[coluna][df[coluna] > lsup]
print(resulInfo.count())
print(resultSup.count())

print(df.query('a < ' + str(linf)))


