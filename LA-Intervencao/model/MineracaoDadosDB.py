import pandas as pd
import numpy as np

import model.DadosTabela as dbTab
import model.dataBase as db
import model.MetaDadosDB as meta
import model.ImportacaoDB as imp
import ml.preditivo as pred
import ml.descritivo as desc
import json
from datetime import datetime
from operator import itemgetter
import controls.componentes as comp
import os


import pickle
import ml.util as ut


id_alg_rule_association = 1
id_alg_clusters = 2
id_alg_outliers = 3

def CalcularPreditivo(idTabela, id_coluna, tam_tst):
    sql = dbTab.GerarSQL(idTabela, 'S')
    lista = db.consultarSQLDataFrame(sql)

    del lista['rowid']

    colunaClasse = meta.ObterColuna(id_coluna)

    modeloDados, listaCopy = ut.PrepararLista(lista)
    listaModeloPred = None

    jsModeloDados = json.dumps(modeloDados, default=iDefault)

    if colunaClasse.tipo == 'N':
        listaCopy[colunaClasse.nome] = ut.TransformarNumeros(lista[colunaClasse.nome].values())
        listaModeloPred = pred.ModeloReg(listaCopy, colunaClasse.nome, tam_tst)
    else:
        listaModeloPred, clfTree = pred.ModeloClf(listaCopy, colunaClasse.nome, tam_tst)

    lstPesos = pred.ObterPesos(lista, clfTree, colunaClasse.nome, colunaClasse.val_aluno_risco)
    strPesos = json.dumps(lstPesos)

    maiorTxAcerto = 0
    id_alg_sel = 0
    for modelo in listaModeloPred:
        txAcerto = modelo['TxAcerto']

        if maiorTxAcerto < txAcerto:
            id_alg_sel = modelo['id_alg']
            maiorTxAcerto = txAcerto


    tabPred = db.TabelaPredicao(0, idTabela, jsModeloDados, None, tam_tst, strPesos, id_alg_sel)

    tabPred = SalvarTabelaPredicao(tabPred)
    SalvarTabelaPredicaoAlg(tabPred.id, listaModeloPred, lstPesos)


    #modelo2, listaCopy2 = ut.PrepararListaComModelo(modeloDados, lista)

    ExportarDados(idTabela)

    return listaModeloPred

def iDefault(o):
    if isinstance(o, np.int64): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    raise TypeError

def SalvarTabelaPredicao(tabPred):
    session = db.getSession()

    iid = tabPred.id_tabela
    obj2 = session.query(db.TabelaPredicao).filter_by(id_tabela=iid).first()
    tabPred.dt_processo = datetime.now()

    if obj2 == None:
        tabPred.id = None
        session.add(tabPred)
        session.flush()
    else:
        obj2.modelo = tabPred.modelo
        obj2.reserva_treino = tabPred.reserva_treino
        obj2.pesos = tabPred.pesos
        obj2.id_alg_sel = tabPred.id_alg_sel

    session.commit()

    tabPred = session.query(db.TabelaPredicao).filter_by(id_tabela=iid).first()

    session.close()


    return tabPred

def SalvarTabelaPredicaoAlg(iid_tabPred, listaModeloPred, lstPesos):
    """
    Salvar dados do que foi previsto
    """
    session = db.getSession()

    for modeloPred in listaModeloPred:
        iid_alg = modeloPred['id_alg']
        mat_conf =  json.dumps( np.array(modeloPred['MatrizConfisao']).tolist() )
        obj = session.query(db.TabelaPredicaoAlg).filter_by(id_tabela_predicao=iid_tabPred).filter_by(id_alg=iid_alg).first()
        if obj == None:
            obj = db.TabelaPredicaoAlg(None, iid_tabPred, iid_alg, modeloPred['Modelo'], modeloPred['Nome'], modeloPred['Pontos'], modeloPred['TxAcerto'], mat_conf)
            session.add(obj)
        else:
            obj.modelo = modeloPred['Modelo']
            obj.pontos = modeloPred['Pontos']
            obj.tx_acerto = modeloPred['TxAcerto']
            obj.matriz_confusao = mat_conf

    session.commit()
    session.close()

def ObterTabelaPredicao(idTabela):
    session = db.getSession()

    obj = session.query(db.TabelaPredicao).filter_by(id_tabela=idTabela).first()

    if obj != None:
        iid = obj.id
        obj.Alg = session.query(db.TabelaPredicaoAlg).filter_by(id_tabela_predicao=iid).all()
        for alg in obj.Alg:
            alg.clf = pickle.loads(alg.modelo)
            alg.selecionado = alg.id_alg == obj.id_alg_sel
            alg.calcular = DM_Calcular

    session.close()

    return obj

def ObterModeloPredicaoAlg(idTabPredAlg):
    session = db.getSession()
    obj = session.query(db.TabelaPredicaoAlg).filter_by(id=idTabPredAlg).first()
    session.close()

    obj.clf = pickle.loads(obj.modelo)

    return obj

def ExibirMatrizConfusao(idTabela, idModPredAlg):
    modeloPredAlg = ObterModeloPredicaoAlg(idModPredAlg)
    tabPred = ObterTabelaPredicao(idTabela)
    tabela = imp.ObterTabela(idTabela)
    colunaClasse, id_coluna = meta.ObterColunaClasse(idTabela)

    modeloBanco = json.loads(tabPred.modelo)

    valoresCls = modeloBanco[colunaClasse]

    for valor in valoresCls:
        print(valor)


    matriz_confusao = json.loads(modeloPredAlg.matriz_confusao)

    return dict(idTabela=idTabela,
                tabela=tabela.nome,
                colunaClasse=colunaClasse,
                dt_processo=tabPred.dt_processo,
                algoritmo=modeloPredAlg.nome,
                valoresCls=valoresCls,
                matriz_confusao=matriz_confusao)

def ExibirPesos(id_tabela):
    tabela = imp.ObterTabela(id_tabela)
    nome_coluna, id_coluna = meta.ObterColunaClasse(tabela.id)
    coluna = meta.ObterColuna(id_coluna)
    tabPredicao = ObterTabelaPredicao(id_tabela)

    listaColunas = meta.ListarColunas(id_tabela)

    pesos = json.loads(tabPredicao.pesos)
    pesosOrdenado = sorted(pesos, key=itemgetter('Peso'), reverse=True)

    scriptGrafico = ''

    for peso in pesosOrdenado:
        df = pd.DataFrame(peso['Valores'])
        print(peso)
        print(df)

        maxFalha   = df[df['Classe'] == coluna.val_aluno_risco] ['_percValor'].max()
        maxSucesso = df[df['Classe'] != coluna.val_aluno_risco] ['_percValor'].max()
        df['destaca'] = ''
        df[ df['Classe'] == coluna.val_aluno_risco ][ df['_percValor'] == maxFalha ]  ['destaca'] = 'F'
        df[ df['Classe'] != coluna.val_aluno_risco ][ df['_percValor'] == maxSucesso ]['destaca'] = 'S'

        for item in peso['Valores']:
            item['destaca'] = ''
            if item['Classe'] == coluna.val_aluno_risco and item['_percValor'] == maxFalha:
                item['destaca'] = 'F'
            if item['Classe'] != coluna.val_aluno_risco and item['_percValor'] == maxSucesso:
                item['destaca'] = 'S'


        #df[dfClsFalha['_percRelativo'] == df['_percValor']] ['destaca'] = 'R'
        #df[dfClsSucesso['_percRelativo'] == df['_percValor']]['destaca'] = 'B'

        dfClsFalha = df[df['Classe'] == coluna.val_aluno_risco]
        dfClsSucesso = df[df['Classe'] != coluna.val_aluno_risco]

        legendaPadrao  = ' Registros com o campo "' + coluna.titulo + '"'
        legendaFalha   = legendaPadrao + ' igual a "' +   coluna.val_aluno_risco  + '"'
        legendaSucesso = legendaPadrao + ' diferente de "' +   coluna.val_aluno_risco + '"'

        grfFalha = comp.grfPizza(legendaFalha      , dfClsFalha, 'Valor', '_qtd','')
        grfSucesso = comp.grfPizza(legendaSucesso, dfClsSucesso , 'Valor', '_qtd','')
        scriptGrafico+= grfFalha.js
        scriptGrafico+= grfSucesso.js

        peso['grfFalha'] = grfFalha.grf
        peso['grfSucesso'] = grfSucesso.grf
        campo = ObterColunaPorNomeLista(listaColunas, peso['Campo'])
        peso['Campo'] = campo.titulo

    return dict(id_tabela=tabela.id,
                nome=tabela.nome,
                pesos=pesosOrdenado,
                scriptGrafico=scriptGrafico)

def ListarTabelaDescricao(idTabela):
    session = db.getSession()
    lista = session.query(db.TabelaDescricao).filter_by(id_tabela=idTabela).all()
    session.close()

    for tabDesc in lista:
        if tabDesc.id_alg == id_alg_rule_association:
            tabDesc.des_alg = 'Regras de Associação'
            tabDesc.link = '/mineracao_dados_rule_assoc?idTabela=' + str(idTabela) + '&id=' + str(tabDesc.id)
        elif tabDesc.id_alg == id_alg_clusters:
            tabDesc.des_alg = 'Clusters'
            tabDesc.link = '/mineracao_dados_cluster?idTabela=' + str(idTabela) + '&id=' + str(tabDesc.id)
        elif tabDesc.id_alg == id_alg_outliers:
            tabDesc.des_alg = 'Outliers'
            tabDesc.link = '/mineracao_dados_outlier?idTabela=' + str(idTabela) + '&id=' + str(tabDesc.id)

    return lista

def Association(idTabela, filtro, qtd_regras):

    tabela = imp.ObterTabela(idTabela)

    sql = dbTab.GerarSQL(idTabela, 'S')
    if tabela.sql_sem_hist != None and tabela.sql_sem_hist != '':
        if filtro == 'H':
            sql = sql + ' WHERE NOT (' + tabela.sql_sem_hist + ')'
        elif filtro == 'A':
            sql = sql + ' WHERE (' + tabela.sql_sem_hist + ')'

    lista = db.consultarSQL(sql)
    regras = desc.Association(lista, int(qtd_regras))

    dp_regras = json.dumps(regras)

    session = db.getSession()
    tabDesc = session.query(db.TabelaDescricao).filter_by(id_tabela=idTabela).filter_by(id_alg=id_alg_rule_association).first()
    if tabDesc == None:
        tabDesc = db.TabelaDescricao(None, idTabela, id_alg_rule_association, dp_regras, datetime.now())
        session.add(tabDesc)
    else:
        tabDesc.modelo = dp_regras
        tabDesc.dt_processo = datetime.now()

    session.commit()
    session.close()

    return tabDesc

def Cluster(idTabela, filtro, qtd_clusters):

    tabela = imp.ObterTabela(idTabela)

    sql = dbTab.GerarSQL(idTabela, 'S')
    if tabela.sql_sem_hist != None and tabela.sql_sem_hist != '':
        if filtro == 'H':
            sql = sql + ' WHERE NOT (' + tabela.sql_sem_hist + ')'
        elif filtro == 'A':
            sql = sql + ' WHERE (' + tabela.sql_sem_hist + ')'

    lista = db.consultarSQLDataFrame(sql)
    modeloDados, listaCopy = ut.PrepararLista(lista)

    kmeans = desc.Cluster(listaCopy, int(qtd_clusters))
    clusters = kmeans.cluster_centers_
    labels = kmeans.labels_

    display = list()
    for x in range(0, int(qtd_clusters)):
        display.append('Cluster_' + str(x))

    objModelo = {
        'n_clusters': qtd_clusters,
        'modeloDados': modeloDados,
        'clusters': clusters.tolist(),
        'labels' : labels.tolist(),
        'display': display
        }

    md_clusters = json.dumps(objModelo)

    session = db.getSession()
    tabDesc = session.query(db.TabelaDescricao).filter_by(id_tabela=idTabela).filter_by(id_alg=id_alg_clusters).first()
    if tabDesc == None:
        tabDesc = db.TabelaDescricao(None, idTabela, id_alg_clusters, md_clusters, datetime.now())
        session.add(tabDesc)
    else:
        tabDesc.modelo = md_clusters
        tabDesc.dt_processo = datetime.now()

    session.commit()
    session.close()


    return None

def Outlier(idTabela, filtro, campoD, campoV):

    tabela = imp.ObterTabela(idTabela)

    sql = dbTab.GerarSQL(idTabela, 'S')
    if tabela.sql_sem_hist != None and tabela.sql_sem_hist != '':
        if filtro == 'H':
            sql = sql + ' WHERE NOT (' + tabela.sql_sem_hist + ')'
        elif filtro == 'A':
            sql = sql + ' WHERE (' + tabela.sql_sem_hist + ')'

    lista = db.consultarSQLDataFrame(sql)

    campoVal = meta.ObterColuna(campoV).nome
    campoDesc = meta.ObterColuna(campoD).nome

    existeOutlier, listaDf = desc.Outliers(lista, campoVal, campoDesc)

    modelo = {
        'campoV': campoVal,
        'campoD': campoDesc,
        'existe': existeOutlier,
        'lista': listaDf
        }

    md_outlier = json.dumps(modelo)

    session = db.getSession()
    tabDesc = session.query(db.TabelaDescricao).filter_by(id_tabela=idTabela).filter_by(id_alg=id_alg_outliers).first()
    if tabDesc == None:
        tabDesc = db.TabelaDescricao(None, idTabela, id_alg_outliers, md_outlier, datetime.now())
        session.add(tabDesc)
    else:
        tabDesc.modelo = md_outlier
        tabDesc.dt_processo = datetime.now()

    session.commit()
    session.close()



    return "OK"

def ObterTabelaDescr(iid):
    session = db.getSession()
    tabDesc = session.query(db.TabelaDescricao).filter_by(id=iid).first()
    session.close()

    return tabDesc

def ListarDadosTOP10(idTabela):
    return None;

def ObterDadosPrevisao(idTabela):
    sql = dbTab.GerarSQL(idTabela, 'O')
    return db.consultarSQLDataFrame(sql)

def PreverValores(idTabela):
    tabela = imp.ObterTabela(idTabela)
    colunaClasse, id_coluna  = meta.ObterColunaClasse(idTabela)
    coluna = meta.ObterColuna(id_coluna)

    nomeTabela = tabela.nome
    nomeColunaClasse = coluna.nome

    LimparDadosColunaClasse(nomeTabela, nomeColunaClasse)


    tabPredicao = ObterTabelaPredicao(tabela.id)
    algPredicao = None
    for alg in tabPredicao.Alg:
        if alg.selecionado:
            algPredicao = alg

    modeloDb = json.loads(tabPredicao.modelo)
    modeloDbColClasse = modeloDb[colunaClasse]

    df = ObterDadosPrevisao(idTabela)
    dfListaCopy = df.copy()
    rowids = df['rowid']
    del dfListaCopy[colunaClasse]
    del dfListaCopy['rowid']

    for index, row in dfListaCopy.iterrows():
        rowPred = ut.VoltarModelo(dict(row), modeloDb)
        val_prev = algPredicao.clf.predict( [rowPred] )

        for key, value in modeloDbColClasse.items():
            if int(key) == int(val_prev):
                classe_prev = 'LA :: Prev :: ' + value
                rowid = rowids[index]
                AtualiarClasse(nomeTabela, nomeColunaClasse, classe_prev, rowid)
                break


def LimparDadosColunaClasse(nomeTabela, nomeColunaClasse):
    sqlLimparColuna = 'UPDATE "' + nomeTabela + '" SET "' + nomeColunaClasse + '" = \'\' WHERE "' + nomeColunaClasse + '"  LIKE \'LA :: Prev%\' '
    print(sqlLimparColuna)

    session = db.getSession()
    session.execute(sqlLimparColuna)
    session.commit()
    session.close()

def AtualiarClasse(nomeTabela, nomeColunaClasse, classe_prev, rowid):
    sqlAtulizarColuna = 'UPDATE "' + nomeTabela + '" SET "' + nomeColunaClasse + '" = \'' + classe_prev + '\' WHERE rowid = ' + str(rowid)
    print(sqlAtulizarColuna)

    session = db.getSession()
    session.execute(sqlAtulizarColuna)
    session.commit()
    session.close()

def SoAlunosEmRisco(id_tabela, nome_coluna, coluna):
    df = ObterDadosPrevisao(id_tabela)
    colClasse = df[coluna.nome]
    for i in range(0, len(colClasse)):
        valorClasse = colClasse[i]
        colClasse[i] = valorClasse.replace('LA :: Prev :: ', '')

    df[coluna.nome] = colClasse
    dfSoAlunosRisco = df[df[nome_coluna] == coluna.val_aluno_risco]
    return dfSoAlunosRisco

def GerarRecomendacoes(id_tabela):
    print('===============================================================================================')
    print('Gerar recomendações')
    tabela = imp.ObterTabela(id_tabela)
    nome_coluna, id_coluna = meta.ObterColunaClasse(tabela.id)
    coluna = meta.ObterColuna(id_coluna)
    tabPredicao = ObterTabelaPredicao(id_tabela)
    tx_acerto = 0
    for alg in tabPredicao.Alg:
        if alg.selecionado:
            tx_acerto = alg.tx_acerto


    pesos = json.loads(tabPredicao.pesos)
    pesosOrdenado = sorted(pesos, key=itemgetter('Peso'), reverse=True)

    dfSoAlunosRisco = SoAlunosEmRisco(id_tabela, nome_coluna, coluna)

    msgs = []

    for index, row in dfSoAlunosRisco.iterrows():
        i_conta_recomendacoes = 0

        for peso in pesosOrdenado:
            campo = peso['Campo']
            print('===============================================================================================')
            print('Campo: ' + campo)
            print('Peso: ' + str(peso['Peso']))
            print(peso)
            dfValorePesos = pd.DataFrame(peso['Valores'])
            print(dfValorePesos)

            dfClsFalha = dfValorePesos[dfValorePesos['Classe'] == coluna.val_aluno_risco]
            dfClsSucesso = dfValorePesos[dfValorePesos['Classe'] != coluna.val_aluno_risco]

            print('')
            print('dfClsFalha')
            print(dfClsFalha)

            print('')
            print('dfClsSucesso')
            print(dfClsSucesso)

            valorCol = row[campo]
            rowFalha = dict(next(dfClsFalha[dfClsFalha['Valor'] == valorCol].iterrows())[1])
            rowSucesso = dict(next(dfClsSucesso[dfClsSucesso['Valor'] == valorCol].iterrows())[1])

            qtdReg = len(dfClsFalha['Valor'])
            falhaPerc = rowFalha['_perc']
            falhaPercRel = rowFalha['_percRelativo']
            sucesPerc = rowSucesso['_perc']
            sucesPercRel = rowSucesso['_percRelativo']

            valorPercSucessoMax = valorCol
            percSucessoMax = dfClsSucesso[dfClsSucesso['Valor'] != valorCol] ['_percValor'].max()
            auxDfvalorPercSucesso = dfClsSucesso[ dfClsSucesso['_percValor'] == percSucessoMax  ]['Valor'].values
            if len(auxDfvalorPercSucesso) > 0:
                valorPercSucessoMax = auxDfvalorPercSucesso[0]

            if (falhaPercRel > sucesPercRel or falhaPerc > 25) and valorCol != valorPercSucessoMax:
                msg = dict()
                msg['Aluno'] = row['rowid']
                msg['Campo'] = campo
                msg['ValAtual'] = valorCol
                msg['ValSuger'] = valorPercSucessoMax
                msgs.append(msg)
                i_conta_recomendacoes+= 1

            if i_conta_recomendacoes == 5:
                break



    SalvarMensagens(tabela, msgs)

    return dfSoAlunosRisco



def SalvarMensagens(tabela, msgs):
    print('===============================================================================================')
    print('Salvar Mensagens')

    listaColunas = meta.ListarColunas(tabela.id)

    sqlDelete = 'DELETE FROM mensagem WHERE id_tabela = ' + str(tabela.id)

    print(sqlDelete)

    session = db.getSession()
    session.execute(sqlDelete)

    coluna_identif_aluno = None
    for col in listaColunas:
        if (col.fl_aluno):
            coluna_identif_aluno = col
            break

    dt_geracao = datetime.now()
    for msg in msgs:
        rowid = msg['Aluno']

        sql_busca_usuario = 'SELECT U.id  FROM "' + tabela.nome + '" AS T0 INNER JOIN usuario AS U ON "' + coluna_identif_aluno.nome + '" = U.login  WHERE T0.rowid = ' + str(rowid) + ' LIMIT 1'
        print(sql_busca_usuario)
        id_usuario_aluno = session.execute(sql_busca_usuario).fetchall()[0]['id']

        coluna = ObterColunaPorNomeLista(listaColunas, msg['Campo'])
        print(coluna.titulo)

        desc_mensagem = 'Na característica "' + coluna.titulo + '" esta informado: "' + msg['ValAtual'] + '".\nRecomendamos que seja modificado para "' + msg['ValSuger'] + '"'
        print(desc_mensagem)

        mensagem = db.Mensagem(None)
        mensagem.id_tabela = tabela.id
        mensagem.id_coluna = coluna.id
        mensagem.id_usuario_aluno = id_usuario_aluno
        mensagem.val_atual = msg['ValAtual']
        mensagem.val_suger = msg['ValSuger']
        mensagem.descartado = 'N'
        mensagem.lido = 'N'
        mensagem.dt_gerado = dt_geracao
        mensagem.descricao = desc_mensagem

        session.add(mensagem)

    session.commit()
    session.close()

def ObterColunaPorIdLista(listaColunas, id):
    for col in listaColunas:
        if col.nome == id:
            return col

    return None

def ObterColunaPorNomeLista(listaColunas, nome):
    for col in listaColunas:
        if col.nome == nome:
            return col

    return None

def ListarRecomendacoes(idTabela):
    session = db.getSession()
    listaMensagens = session.query(db.Mensagem).filter_by(id_tabela=idTabela).all()

    listaRetorno = []

    listaColunas = meta.ListarColunas(idTabela)

    for msg in listaMensagens:
        existeAluno = False
        edtRow = {  }
        msgsAluno = []

        for rowRet in listaRetorno:
            if rowRet['id_usuario_aluno'] == msg.id_usuario_aluno:
                existeAluno = True
                edtRow = rowRet
                msgsAluno = edtRow['MsgsAluno']
                break

        if existeAluno == False:
            edtRow['id_usuario_aluno'] = msg.id_usuario_aluno
            usuario = session.query(db.Usuario).filter_by(id=msg.id_usuario_aluno).first()
            edtRow['nome'] = usuario.nome
            listaRetorno.append(edtRow)

        msgsAluno.append(msg)
        edtRow['MsgsAluno'] = msgsAluno

    session.close()

    tabPredicao = ObterTabelaPredicao(idTabela)
    tx_acerto = 0
    for alg in tabPredicao.Alg:
        if alg.selecionado:
            tx_acerto = alg.tx_acerto

    return dict(tabela=imp.ObterTabela(idTabela),
                tx_acerto=tx_acerto,
                lista=listaRetorno)


def ObterAlunosParaRecomendacoes(id_aluno):
    listaMensanges = []
    nomeAluno = ''
    tx_acerto=0

    nomeColuna, id_colunaClasse = meta.ObterColunaClasse()

    colunaClasse = meta.ObterColuna(id_colunaClasse)
    tabela = imp.ObterTabela(colunaClasse.id_tabela)

    colunaIdAluno = meta.ObterColunaIdAluno(colunaClasse.id_tabela)

    listaAlunos = []
    listaColunas = []
    listaColunas.append(colunaIdAluno.id)
    listaColunas.append(colunaClasse.id)

    sql = dbTab.GerarSQL(tabela.id, 'O', listaColunas)
    dfAlunos = db.consultarSQLDataFrame(sql)

    session = db.getSession()

    for index, row in dfAlunos.iterrows():
        usuario = session.query(db.Usuario).filter_by(login=row[colunaIdAluno.nome]).first()
        usuario.selecionado = False

        if id_aluno == usuario.id:
            nomeAluno = usuario.nome
            usuario.selecionado=True

        listaAlunos.append(usuario)

    session.close()


    algPredicao= ObterTabelaPredicao(tabela.id)
    for alg in algPredicao.Alg:
        if alg.selecionado:
            tx_acerto = alg.tx_acerto

    if id_aluno != 0:
        listaMensanges = ObterRecomendacoesPorAluno(id_aluno)


    return dict(listaAlunos=listaAlunos,
                listaMensanges=listaMensanges,
                id_aluno=id_aluno,
                nomeAluno=nomeAluno,
                tx_acerto=tx_acerto)


def ObterRecomendacoesPorAluno(id_aluno):
    session = db.getSession()
    listaMensagens = session.query(db.Mensagem).filter_by(id_usuario_aluno=id_aluno).all()
    session.close()

    for msg in listaMensagens:
        msg.attHtml = dict()
        msg.attHtml['checked'] = ''
        msg.attHtml['disabled'] = ''

        if (msg.descartado == 'S'):
            msg.attHtml['checked'] = 'checked'
            msg.attHtml['disabled'] = 'disabled="disabled"'


    return listaMensagens

def SalvarMensagem(msg):
    session = db.getSession()
    obj = session.query(db.Mensagem).filter_by(id=msg.id).first()
    obj.descricao = msg.descricao
    obj.descartado = msg.descartado

    session.commit()
    session.close()

def ExportarDados(id_tabela):
    tabela = imp.ObterTabela(id_tabela)
    #-- Rede Gazeta
    #path = "C:/Users/bstoll/source/repos/LA-Intervencao/LA-Intervencao/arquivosUpld"
    #-- pythonanywhere
    path = "/home/bstoll/mysite/arquivosUpld"
    #-- Casa
    #path = "C:/Users/Bruno Stoll/source/repos/LA-Intervencao/LA-Intervencao"

    pathFile = "{path}/{file}".format(path=path, file=tabela.nome+".csv")

    listaColunas = meta.ListarColunas(id_tabela)
    ar_lst_cols = []
    for col in listaColunas:
        ar_lst_cols.append(col.id)

    sql = dbTab.GerarSQL(id_tabela, 'O', ar_lst_cols)
    df = dbTab.db.consultarSQLDataFrame(sql)
    if os.path.isfile(pathFile):
        os.remove(pathFile)

    df.to_csv(pathFile, index = False)

def DM_Calcular(mod_matriz_confusao, ret):
    matriz_confusao = np.array( json.loads(mod_matriz_confusao) )
    VP = matriz_confusao[0,0]
    FP = matriz_confusao[0,1]
    FN = matriz_confusao[1,0]
    VN = matriz_confusao[1,1]
    
    sensibilidade  = VP/(VP+FN)*100
    especificidade = VN/(VN+FP)*100
    acuracia       = ((VP+VN)/(VP+VN+FP+FN))*100
    #fi             = (VP*VN - FP*FN) / Math.sqrt((VP + FP)*(VP + FN)*(VN + FP)*(VN + FN))
    VPP            = (VP/(VP+FP))*100
    VPN            = (VN/(VN+FN))*100
    eficiencia     = (sensibilidade +especificidade)/2		
    totalP         = VP+FP
    totalN         = VN+FN
    totalVPFN      = VP+FN
    totalFPVN      = FP+VN
    totalG         = VP+FP+FN+VN

    if ret == 'sens':
        return round(sensibilidade, 1)
    elif ret == 'esp':
        return round(especificidade, 1)
    elif ret == 'acur':
        return round(acuracia, 1)
    elif ret == 'VPP':
        return round(VPP, 1)
    elif ret == 'VPN':
        return round(VPN, 1)
    elif ret == 'efic':
        return round(eficiencia, 1)
    elif ret == 'totP':
        return totalP
    elif ret == 'totN':
        return totalN
    elif ret == 'totG':
        return totalG
    else:
        return -1