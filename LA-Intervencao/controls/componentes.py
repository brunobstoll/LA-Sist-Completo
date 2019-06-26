from bottle import route, view, template
import string
import random
import pandas as pd
import numpy as np


i_conta = 0

class defGrafico(object):
    "Definição de Gráfico"

    def __init__(self, grf, js):        
        self.grf = grf
        self.js = js

def gerarId():
    global i_conta
    i_conta+= 1
    retId = 'a'

    id = string.ascii_uppercase + string.digits
    for i in range(0, 20):
        retId = retId + random.choice(id)

    return retId + '_' + str(i_conta)

def grid(titulo, lista, colunas, informacao = ''):
    "Gerar Grip (HTML + Javascript)"

    return template('grid.tpl', titulo=titulo, lista=lista, colunas=colunas, informacao=informacao)

def gridSP(titulo, lista, colunas, informacao = ''):
    "Gerar Grip (HTML + Javascript)"

    return template('gridSP.tpl', titulo=titulo, lista=lista, colunas=colunas, informacao=informacao)

def grfPizza(titulo, lista, colLabel, colValor, informacao=''):
    "Gerar gráfico de Pizza (HTML + Javascript)"
    obj = defGrafico('', '')
    obj.grf = ''
    obj.js = ''

    if lista is not None:
        id = gerarId()

        labels = lista[colLabel]
        valores = lista[colValor]        

        htmlGrfPizza = template('grfPizza.tpl', id=id, titulo=titulo, informacao=informacao)
        jsGrfPizza = template('grfPizza_script.tpl', id=id, labels=labels, valores=valores)

        obj.grf = htmlGrfPizza
        obj.js = jsGrfPizza

    return obj

def treeView(lista, campoTexto, campoValor, campoFilhos):
    "Gerar TreeView (HTML + Javascript)"
    idComp = gerarId()
    html = '<div id="' + idComp + '" class=""></div>'
    js = template('treeView_script.tpl', id=idComp, lista=lista, campoTexto=campoTexto, campoValor=campoValor, campoFilhos=campoFilhos)

    for item in lista:
        item[campoTexto]

    obj = defGrafico(html, js)
    return obj

def grfBolha(titulo, lista, labels, informacao):
    "Gerar Gráfico de Bolha (HTML + Javascript)"
    obj = defGrafico('', '')
    obj.grf = ''
    obj.js = ''

    if lista != None:
        id = gerarId()

        htmlGrfBolha = template('grfBubble.tpl', id=id, titulo=titulo, informacao=informacao)
        jsGrfBolha = template('grfBubble_script.tpl', id=id, labels=labels, lista=lista)

        obj.grf = htmlGrfBolha
        obj.js = jsGrfBolha

    return obj

def grfOutliers(lista, campoD, campoV, titulo='Outliers', informacao=''):
    "Gerar Gráfico de Linha para outlier (HTML + Javascript)"
    obj = defGrafico('', '')
    obj.grf = ''
    obj.js = ''

    id = gerarId()

    htmlGrfOutlier = template('grfOutliers.tpl', id=id, titulo=titulo, informacao=informacao)
    jsGrfOutliers  = template('grfOutliers_script.tpl', id=id, lista=lista, campoD=campoD, campoV=campoV)

    obj.grf = htmlGrfOutlier
    obj.js = jsGrfOutliers

    return obj

def grfBarras(titulo, lista, campoCateg, campoSerie, campoValor, informacao=''):
    "Gerar Gráfico de Barras (HTML + Javascript)"
    obj = defGrafico('', '')
    obj.grf = ''
    obj.js = ''

    id = gerarId()

    valoresSeries = []
    if campoSerie != '':
        for valSerie in lista[campoSerie].unique():
            valoresSeries.append(valSerie)

    valoresCateg = []
    if campoCateg != '':        
        for valCateg in lista[campoCateg].unique():
            valoresCateg.append(valCateg)

    html = template('grfBarras.tpl', id=id, titulo=titulo, informacao=informacao)
    jscr = template('grfBarras_script.tpl', 
                    id=id, 
                    lista=lista, 
                    valoresSeries=valoresSeries, 
                    valoresCateg=valoresCateg, 
                    campoValor=campoValor,
                    campoSerie=campoSerie,
                    campoCateg=campoCateg)

    obj.grf = html
    obj.js = jscr

    return obj

def grfLinhas(titulo, lista, campoCateg, campoSerie, campoValor,informacao=''):
    "Gerar Gráfico de Linhas (HTML + Javascript)"
    obj = defGrafico('', '')
    obj.grf = ''
    obj.js = ''

    id = gerarId()

    valoresSeries = []
    for valSerie in lista[campoSerie].unique():
        valoresSeries.append(valSerie)

    valoresCateg = []
    for valCateg in lista[campoCateg].unique():
        valoresCateg.append(valCateg)

    html = template('grfLinhas.tpl', id=id, titulo=titulo, informacao=informacao)
    jscr = template('grfLinhas_script.tpl', 
                    id=id, 
                    lista=lista, 
                    valoresSeries=valoresSeries, 
                    valoresCateg=valoresCateg, 
                    campoValor=campoValor,
                    campoSerie=campoSerie,
                    campoCateg=campoCateg)

    obj.grf = html
    obj.js = jscr

    return obj

def infCard(titulo, lista, colunas):
    "Gerar Cartão de Informação"
    obj = defGrafico('', '')
    obj.grf = ''
    obj.js = ''

    obj.grf = template('infCards.tpl', titulo=titulo, lista=lista, colunas=colunas)

    return obj

def compGrid(titulo, lista, colunas):
    "Gerar Grid"
    obj = defGrafico('', '')
    obj.grf = ''
    obj.js = ''

    obj.grf = grid(titulo, lista, colunas, '')

    return obj