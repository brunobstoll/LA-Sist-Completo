import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import warnings 

warnings.filterwarnings('ignore')

#1 = tree; 2 = knn; 3 = svm
tp_algoritmo = 3

def ObjeterAlgoritmo():
    if tp_algoritmo == 1:
        return tree.DecisionTreeClassifier()
    elif tp_algoritmo == 2:
        return KNeighborsClassifier(n_neighbors=5)
    elif tp_algoritmo == 3:
        return svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
                  decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
                  max_iter=-1, probability=True, random_state=None, shrinking=True,
                  tol=0.001, verbose=False)
    else:
        return None

def PrepararLista(lista, colResultado, valTeste):
    train = lista.copy()
    col_teste_um = '_TESTE_1_'

    valTesteSpl = valTeste.split(',')
    for j in range(0, len(valTesteSpl)):
        train[colResultado][train[colResultado] == valTesteSpl[j] ] = 1

    train[colResultado][train[colResultado] != 1] = 0
    train[col_teste_um] = 1

    #train[colResultado].value_counts()
    #train.head()
    #print "Shape: " + train.shape
    #train.head()
    #train.describe()

    target = []
    for x in train[colResultado].values:
        target.append(int(x))

    id=0
    lstPesos = [  ]
    cols = [ ]
    for col in list(train.columns.values):
        if str(colResultado) == str(col):
            continue
        if str(col_teste_um) == str(col):
            continue

        print('Coluna: ' + col)
        print('Quantidade única ' + str(len(train[col].unique())))

        pesos = { }
        pesos['id'] = id
        pesos['Campo'] = col

        cols.append(col)        
        identif = 0
        val_cols = []
        for val in train[col].unique():
            val_col = {  }
            identif +=1
            print ('    >>Valor: ' + str(val) + ' (' + str(identif) + ')')
            train[col][train[col] == val] = int(identif)

            val_col['Valor'] = val
            val_col['Qtd'] = list(train[col][train[col] == int(identif)].value_counts())[0]
            val_col['Validos'] = train[[col, colResultado, col_teste_um]][train[col] == int(identif)][col_teste_um][train[colResultado] == 1].values.sum()

            val_cols.append(val_col)

        pesos["Detalhes"] = val_cols

        lstPesos.append(pesos)
        id+= 1

    
    del train[colResultado]
    del train[col_teste_um]

    features = []
    for x in list(train.values):
        row = []
        for y in list(x):
            row.append(int(y))

        features.append(row)

    return dict(train=train,
                features=features,
                target=target,
                lstPesos=lstPesos)

def Calcular(lista, colResultado, valTeste, IgnoreImportance=None):
    prep = PrepararLista(lista, colResultado, valTeste)

    features = prep['features']
    target   = prep['target']
    lstPesos = prep['lstPesos']

    clf = ObjeterAlgoritmo()
    clf = clf.fit(features, target)
    score = clf.score(features, target)

    if (IgnoreImportance != None) and (IgnoreImportance == False):
        importances = clf.feature_importances_
        for k in range(0, len(importances)):
            print ('Importância ' + str(importances[k]))
            for p in list(lstPesos):
                if str(p['id']) == str(k):
                    p['Importance'] = importances[k]


    return dict(score  = score,
                i_tree = clf,
                pesos = lstPesos)

def PredictLista(lista, colResultado, valTeste, i_tree):

    prep = PrepararLista(lista, colResultado, valTeste)

    features = prep['features']
    target   = prep['target']

    lista['_Predict_Val_'] = 'NA'
    lista['_Real_Val_'] = 'NA'

    for id_row in range(0, len(lista)):
        valores = features[id_row]
        i_predict = i_tree.predict([valores])
        i_real = target[id_row]

        lista.set_value(id_row, '_Predict_Val_', i_predict[0])
        lista.set_value(id_row, '_Real_Val_', i_real)
        
    return lista


def RecalcularPredict(lista, i_tree, colResultado, valTeste):
    lista = lista.copy()
    del lista['qtd_reg']

    prep = PrepararLista(lista, colResultado, valTeste)

    features = prep['features']
    target   = prep['target']

    lista['predict'] = 'NA'
    lista['Max_predict'] = 'NA'
    lista['Min_predict'] = 'NA'
    max_val = 0
    min_val = 1
    for id_row in range(0, len(lista)):
        valores = features[id_row]
        i_predict = i_tree.predict_proba([valores])
        i_max_val = i_predict[0][0]
        i_min_val = i_predict[0][1]

        if i_max_val > max_val:
            max_val = i_max_val

        if i_min_val < min_val:
            min_val = i_min_val

        previsao = str(i_predict).replace('[[', '').replace(']]', '').strip().replace('  ', ' a ')

        lista.loc[id_row, 'Max_predict'] = i_max_val
        lista.loc[id_row, 'Min_predict'] = i_min_val
        lista.loc[id_row, 'predict'] = str(previsao)

    print(max_val)
    print(min_val)

    return lista

