import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder

def VoltarModelo(row, modelo):
    rowCopy = []
    for col in row:
        col_mapping = modelo[col]
        for keyMapp in col_mapping:
            if col_mapping[keyMapp] == row[col]:
                rowCopy.append(int(keyMapp))
                break

    return rowCopy


def PrepararLista(lista):
    print('')
    print('----------------------------------------------------------------')
    print('PrepararLista...')
    listaCopy = lista.copy()
    modelo = {  }
    for col in list(lista.columns.values):
        print(col)
        col_le = LabelEncoder()

        col_labels = col_le.fit_transform(lista[col])
        col_mapping = {index: label for index, label in enumerate(col_le.classes_)}

        modelo[col] = col_mapping
        listaCopy[col] = col_labels

        # valores = {  }
        # identif = 0
        # for val in lista[col].unique():
        #     identif += 1
        #     valores[val] = identif
        #     listaCopy[col][listaCopy[col] == val] = int(identif)

    print(modelo)
    return modelo, listaCopy
    
def PrepararListaComModelo(modelo, lista):
    listaCopy = lista.copy()
    for col in list(lista.columns.values):
        valores =  modelo[col]
        identif = len(valores)
        for val in lista[col].unique():
            if val in valores:
                valor = valores[val]
                listaCopy[col][listaCopy[col] == val] = valor
            else:
                identif += 1
                valores[val] = identif
                listaCopy[col][listaCopy[col] == val] = identif

    return modelo, listaCopy

def TransformarNumeros(numeros):
    num = []
    for x in numeros:
        num.append(float(x))

    return np.array(num)
