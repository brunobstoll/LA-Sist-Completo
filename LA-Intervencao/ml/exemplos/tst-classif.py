from sklearn.svm import SVC
import numpy as np
import pandas as pd


dados = pd.read_csv('C:/temp/iris.txt', header = None)



val_cols = []
identif = 0
for val in dados[4].unique():
    identif +=1

    dados[4][dados[4] == val] = int(identif)
    
    val_col = {  }
    val_col['Valor'] = val
    val_col['id'] = identif
    val_cols.append(val_col)
   
classe = dados[4]
print(val_cols)
del dados[4]

features = []
for x in list(dados.values):
    row = []
    for y in list(x):
        row.append(int(y))

    features.append(row)

target = []
for x in classe.values:
    target.append(int(x))

clf = SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
      decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
      max_iter=-1, probability=True, random_state=None, shrinking=True,
      tol=0.001, verbose=False)
clf.fit(features, target)




print(clf)


resultado = clf.predict([[7.5, 3.5, 4.2, 1.0]])
print(resultado)
resultado2 = clf.predict_proba([[7.5, 3.5, 4.2, 1.0]])
print(resultado2)

#for id_row in range(0, len(dados)):
#    
    


#clf = svm.SVC()
#clf.fit(X, y)  

#resultado = clf.predict([[2, 2]])

#print(resultado)
#print(type(resultado))


