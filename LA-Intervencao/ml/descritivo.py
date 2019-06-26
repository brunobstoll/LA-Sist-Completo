
# ----------------------------------------------------------------
#
# https://docs.microsoft.com/en-us/power-bi/service-insight-types
#
# ----------------------------------------------------------------


# [  OK ] Associação
# [  OK ] Agrupamento ( Cluster )
# [  OK ] Detecção de desvios ( Outliers )
# [ NOK ] Padrões Sequenciais
# [ NOK ] Sumarização



# Associação 
# >> Apriori
# >> questão? como representar isto? Lista de Regras

# Agrupamento 
#   >> K-Means

# Outliers 
# http://scikit-learn.org/stable/modules/outlier_detection.html
# gráfico de ponto

# Padrões Sequenciais >> Média por qualquer campo "temporal" + regressão
# >> http://scikit-learn.org/stable/auto_examples/gaussian_process/plot_gpr_co2.html
# gráfico de linha

# Sumarização
# >> mínimo
# >> máximo
# >> média

import numpy as np
import pandas as pd

import math

from sklearn.cluster import KMeans
import apyori as ap



def Cluster(lista, qtd_clusters):
    kmeans = KMeans(n_clusters=qtd_clusters)
    kmeans.fit(lista)
    return kmeans

def Association(lista, top=999):
    transacoes = []
    for linha in lista:
        valores = []
        for idxCol in range(0, len(linha.items())):
            valores.append(str(linha.items()[idxCol][0]) + ' > ' + str(linha.items()[idxCol][1]))

        transacoes.append(valores)

    regras = ap.apriori(transacoes, min_length = 2)

    conta_regras = 0
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
            soma_lift = 0
            for r_item in r[2]:
                itemRegra = {  }
                item_base = next((v for i, v in enumerate(r_item.items_base) if i == 0))
                item_add = next((v for i, v in enumerate(r_item.items_add) if i == 0))

                if item_base == '' or item_add == '':
                    continue

                camposItem = '[' + item_base + '] >> [' + item_add + ']'

                lift = round(r_item.lift, 3)
                confidence = round(r_item.confidence, 3)
                soma_lift = soma_lift + lift

                itemRegra['campos'] = camposItem
                itemRegra['lift'] = lift
                itemRegra['confidence'] = confidence

                itemsRegra.append(itemRegra)

            if len(itemsRegra) > 0:
                conta_regras+= 1
                reg_regra['Qtd'] = i_conta_campos
                reg_regra['campos'] = campos
                reg_regra['lift'] = soma_lift / len(reg_regra)

                if len(reg_regra) > 2:
                    reg_regra['Regras'] = itemsRegra
                else:
                    reg_regra['Regras'] = []

                regras_tb.append(reg_regra)

                if conta_regras == top:
                    break

    return regras_tb

def Outliers(lista, colNum, colDesc):
    df = lista[ [colNum, colDesc] ]
    df[colNum] = df[colNum].astype('float64')
    media = np.average(df[colNum])
    df['media'] = media

    # quartil 1 e 3
    quartil1 = df[colNum].quantile([0.25]).values[0]
    quartil3 = df[colNum].quantile([0.75]).values[0]

    # Interquartil 
    iqt = quartil3 - quartil1

    lSup = math.trunc(media + (1.5 * iqt))
    lInf = math.trunc(media - (1.5 * iqt))

    print(df[colNum].values)
    print('----------------------------------------------------------------------')
    print('Media ' + str(media))
    print('Q1 ' + str(quartil1))
    print('Q3 ' + str(quartil3))
    print('IQR ' + str(iqt))
    print('L-Sup ' + str(lSup))
    print('L-Inf ' + str(lInf))

    print('----------------------------------------------------------------------')

    resulInfo = df[colNum][df[colNum] < lInf]
    resultSup = df[colNum][df[colNum] > lSup]

    qtdInf = resulInfo.count()
    qtdSup = resultSup.count()

    existeOutlier = False
    df['lSup'] = lSup
    df['lInf'] = lInf

    if qtdInf > 0 or qtdSup > 0:
        existeOutlier = True

    return existeOutlier, list(df.T.to_dict().values())


