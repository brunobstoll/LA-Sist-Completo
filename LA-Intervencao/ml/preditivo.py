import pandas as dp
import numpy as np

import warnings
import pickle
from sklearn.metrics import confusion_matrix

import math

# Classificação
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB

# Regressão
from sklearn.svm import SVR
from sklearn import linear_model


warnings.filterwarnings('ignore')



i_clf_tree  = 1
i_clf_knn   = 2
i_clf_svm   = 3
i_clf_mlp   = 4
i_clf_naive = 5

i_reg_svr = 1
i_reg_lassolars = 2
i_reg_bayes = 3


algoritmo_clf = [ 'NA', 'Decision Tree-based', 'K-nearest Neighbors', 'Support Vector Machine', 'Multi-layer Perceptron Classifier', 'Naive Bayes' ]
algoritmo_reg = ['', 'Support Vector Regression', 'LassoLars', 'Bayesian Regression']

def ObterAlgoritmoClf(tp_algoritmo):
    if tp_algoritmo == i_clf_tree:
        return tree.DecisionTreeClassifier()
    elif tp_algoritmo == i_clf_knn:
        return KNeighborsClassifier(n_neighbors=5)
    elif tp_algoritmo == i_clf_svm:
        return svm.SVC(C=1.0)
    elif tp_algoritmo == i_clf_mlp:
        return MLPClassifier(hidden_layer_sizes=500, activation='relu')
    elif tp_algoritmo == i_clf_naive:
        return GaussianNB()

    else:
        return None

def ObterAlgoritmoReg(tp_algoritmo):
    if tp_algoritmo == i_reg_svr:
        return SVR(kernel='rbf', C=1e3, gamma=0.1)
    elif tp_algoritmo == i_reg_lassolars:
        return linear_model.LassoLars(alpha=0.01)
    elif tp_algoritmo == i_reg_bayes:
        return linear_model.BayesianRidge()
    else:
        return None

def PrepararTargetFeatures(lista, colunaClasse, tipo):
    train = lista.copy()

    colLista = train[colunaClasse]
    target = []
    for x in colLista.values:
        if tipo == 'clf':
            target.append(int(x))
        elif tipo == 'reg':
            target.append(float(x))

    del train[colunaClasse]

    features = []
    for x in list(train.values):
        row = []
        for y in list(x):
            row.append(int(y))

        features.append(row)

    return features, target, train

def ModeloClf(lista, colunaClasse, perc_uso_teste):
    print('ModeloClf...')
    tamanho = len(lista)
    tamanhoTreino = tamanho - int(tamanho * (perc_uso_teste / 100))
    tamanhoTeste  = tamanho - tamanhoTreino

    features, target, train = PrepararTargetFeatures(lista, colunaClasse, 'clf')

    clfTree = None

    listaModelos = []
    for idx_alg in range(1, 6):
        print(algoritmo_clf[idx_alg])

        modelo = {  }
        clf = ObterAlgoritmoClf(idx_alg)
        clf.fit(features[0:tamanhoTreino], target[0:tamanhoTreino])

        if idx_alg == i_clf_tree:
            clfTree = clf

        tx_acerto, mat_conf = ObterTxAcertos(clf, features, target, tamanhoTeste)

        modelo['Modelo'] = pickle.dumps(clf)
        modelo['id_alg'] = idx_alg
        modelo['Nome'] = algoritmo_clf[idx_alg]
        modelo['Pontos'] = round(clf.score(features, target), 4)
        modelo['TxAcerto'] = round(tx_acerto, 4)
        modelo['MatrizConfisao'] = mat_conf

        listaModelos.append(modelo)

        print(clf)
        print(tx_acerto)
        print(mat_conf)

    return listaModelos, clfTree

def ObterPesos(lista, clfTree, colunaTarget, valTarget):
    lstPesos = [ ]

    importances = clfTree.feature_importances_

    idx = 0
    for col in list(lista.columns.values):
        if col == colunaTarget:
            continue

        grp = lista[ [colunaTarget, col] ].groupby([colunaTarget, col] ).groups
        lstValores = [ ]
        pesos = { }
        pesos['Campo'] = col
        pesos['Peso'] = round(importances[idx], 5)
        idx+= 1

        qtdTotal = 0
        qtdTotalValTarget = 0
        qtdTotalValOutros = 0
        for item in grp.items():
            qtdTotal+= len(item[1])
            if item[0][0] == valTarget:
                qtdTotalValTarget+= len(item[1])
            if item[0][0] != valTarget:
                qtdTotalValOutros+= len(item[1])


        for item in grp.items():
            val = { }
            val['Valor'] = item[0][1]
            val['Classe'] = item[0][0]
            val['_qtd'] = len(item[1])
            val['_perc'] = round((len(item[1]) / qtdTotal) * 100, 2)
            if item[0][0] == valTarget:
                val['_percRelativo'] = round((len(item[1]) / qtdTotalValTarget) * 100, 2)
            if item[0][0] != valTarget:
                val['_percRelativo'] = round((len(item[1]) / qtdTotalValOutros) * 100, 2)

            qtdValor = 0
            for itemValor in grp.items():
                if item[0][1] == itemValor[0][1]:
                    qtdValor += len(itemValor[1])


            val['_qtdValor'] = qtdValor
            val['_percValor'] = 0
            if qtdValor != 0:
                val['_percValor'] = round((len(item[1]) / qtdValor) * 100, 2)

            lstValores.append(val)

        pesos['Valores'] = lstValores
        lstPesos.append(pesos)

    return lstPesos

def ObterTxAcertos(clf, features, target, tamanhoTeste):
    features2 = features[len(features) - tamanhoTeste:]
    target2 = target[len(target) - tamanhoTeste:]

    val_pred = []
    acertos = 0
    erros = 0

    for idx in range(0, tamanhoTeste):
        resultTst = clf.predict([ features2[idx] ])
        resultado = target2[idx]

        val_pred.append(resultTst[0])

        if resultado == resultTst[0]:
            acertos+= 1
        else:
            erros+= 1

    mat_conf = confusion_matrix(target2, val_pred)
    return (acertos / tamanhoTeste) * 100, mat_conf

def ModeloReg(lista, colunaClasse, perc_uso_teste):
    features, target, train = PrepararTargetFeatures(lista, colunaClasse, 'reg')

    listaModelos = []
    for idx_alg in range(1, 4):
        modelo = {  }
        reg = ObterAlgoritmoReg(idx_alg)
        reg.fit(features, target)

        modelo['Modelo'] = pickle.dumps(reg)
        modelo['id_alg'] = idx_alg
        modelo['Nome'] = algoritmo_reg[idx_alg]
        modelo['Pontos'] = round(reg.score(features, target), 4)
        modelo['TxAcerto'] = round(ObterTxAcertos(reg, features, target, perc_uso_teste), 4)

        listaModelos.append(modelo)

    return listaModelos