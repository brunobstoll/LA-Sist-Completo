
import pandas as pd
import numpy as np
import apyori as ap
import json

dados = { 
    '1-leite':    [ 0,1,0,1,0,0,0,0,0,0 ], 
    '2-cafe':     [ 1,0,1,1,0,0,0,0,0,0 ], 
    '3-cerveja':  [ 0,1,0,0,1,0,0,0,0,0 ],
    '4-pao':      [ 1,1,1,1,0,1,0,0,0,0 ], 
    '5-manteiga': [ 1,1,1,1,0,1,0,0,0,0 ], 
    '6-arroz':    [ 0,0,0,0,0,0,0,0,1,1 ], 
    '7-feijao':   [ 0,0,0,0,0,0,0,1,1,1 ], 
    }

df = pd.DataFrame( data=dados )

print('Colunas')
print(df.columns)
print('Valores')
print(df.values)

transacoes = []
for i in range(0, len(df.values)):
    valores = []
    for j in range(0, len(df.columns)):
        if df.values[i,j] != 0:
            valores.append(df.columns[j])
        else:
            valores.append('')

    transacoes.append(valores)


regras = ap.apriori(transacoes, min_length = 2)
#regras = apriori(transacoes, min_support = 0.3, min_confidence = 0.1, min_lift = 1, min_length = 2)
#regras = apriori(transacoes) #, min_support = 0.5, min_confidence = 0.2, min_lift = 1, min_length = 1)

print('------------------------------------------------------------')
print('Resultado')
regras_tb = []
for r in regras:
    if len(r[0]) <= 1:
        continue

    reg_regra = {  }
    campos = ''
    i_conta_campos = 0
    for campo in r[0]:
        if campo == '':
            continue

        i_conta_campos += 1
        if campos == '':
            campos = '['+ campo + ']'
        else:
            campos += ' >> [' + campo + ']'

    if i_conta_campos > 1:
        #print(campos)
        if i_conta_campos > 2:
            print('Maior que 2')

        itemsRegra = []
        for r_item in r[2]:
            itemRegra = {  }
            item_base = next((v for i, v in enumerate(r_item.items_base) if i == 0))
            item_add = next((v for i, v in enumerate(r_item.items_add) if i == 0))

            if item_base == '' or item_add == '':
                continue

            camposItem = '[' + item_base + '] >> [' + item_add + ']'

            lift = round(r_item.lift, 3)
            confidence = round(r_item.confidence, 3)

            itemRegra['campos'] = camposItem
            itemRegra['lift'] = lift
            itemRegra['confidence'] = confidence

            itemsRegra.append(itemRegra)

        #print(r)
        reg_regra['Qtd'] = i_conta_campos
        reg_regra['campos'] = campos
        reg_regra['Regras'] = itemsRegra

        regras_tb.append(reg_regra)


#dfRegras = pd.DataFrame(data = regras_tb, columns = {'qtd. Cols', 'Regra', 'Lift', 'Confidence'})
for reg_regra in regras_tb:
    print('\r\n')
    print(reg_regra)

print(json.dumps(regras_tb))
#print('------------------------------------------------------------')
#print('Resultado Formatado')
#resultadoFormatado = []
#for j in range(0, len(resultado2)):
#    resultadoFormatado.append([ list(x) for x in resultado2[j][2] ])

#for rf in resultadoFormatado:
#    print(rf)