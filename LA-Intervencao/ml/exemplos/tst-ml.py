from sklearn import tree

lisa=1
irregular=0

doce=1
superDoce=2

maca=1
laranja=0

pomar     = [[150, lisa, doce], [130,lisa, superDoce], [180,irregular, doce], [160,irregular, doce]]
resultado = [maca,              maca,                  laranja,               laranja]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(pomar, resultado)


peso = input("Entre com o peso: ")
superficie = input("Entre com o superfície (1-lisa, 0-irregular): ")
sabor = input("Entre com o sabor (1-doce, 2-Super Doce): ")

resultadoUsuario = clf.predict([[peso, superficie, sabor]])
resultado2 = clf.predict_proba([[peso, superficie, sabor]])

if resultadoUsuario == 1:
    print("É uma maça")
else:
    print("É uma laranja")
