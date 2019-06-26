import model.dataBase as db
import model.MetaDadosDB as meta
import model.ImportacaoDB as imp
import spacy
from spacy import displacy
import model.DadosTabela as dbTab
import model.MetaDadosDB as meta
import controls.componentes as comp
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')


def ListarPainel(tipo=None):
    session = db.getSession()

    if tipo == None:
        lista = session.query(db.Painel).all()
    else:
        lista = session.query(db.Painel).filter_by(tipo=tipo).all()

    session.close()

    for painel in lista:
        painel.ds_tipo = ''
        if painel.tipo == 'A':
            painel.ds_tipo = 'Aluno'
        elif painel.tipo == 'P':
            painel.ds_tipo = 'Professor'

        painel.comandoEditar = '<a href="/defdashboard?id=' + str(painel.id) + '">' + painel.nome + '</a>'
        painel.comandoVisualizar = '<a href="/viewdashboard?id=' + str(painel.id) + '">Visualizar</a>'

    return lista


def ObterPainel(iid):
    if int(iid) ==  0:
        return db.Painel(0, '', 'P', '')
    else:
        session = db.getSession()
        obj = session.query(db.Painel).filter_by(id=iid).first()
        session.close()
        return obj

def SalvarPainel(painel):
    session = db.getSession()

    if int(painel.id) == 0:
        painel.id = None
        session.add(painel)
    else:
        iid = painel.id
        obj2 = session.query(db.Painel).filter_by(id=iid).first()
        obj2.nome = painel.nome
        obj2.tipo = painel.tipo
        obj2.modelo = painel.modelo

    session.commit()
    session.close()

def Parametros(expressao):
    d_filtro = dict()
    conta=0
    while True:
        ini = expressao.find('"')
        if ini == -1:
            break
        
        fim = expressao[ini+1:].find('"')
        if fim == -1:
            expressao = expressao.replace('"', '')
            break
        
        conta+= 1
        filtro = expressao[ini:ini+fim+2]
        nomeParam = 'param'+str(conta)
        d_filtro[nomeParam] = filtro.replace('"', '')
        
        expressao = expressao.replace(filtro, nomeParam)
        print(nomeParam, filtro)
        print(expressao)
    
    return expressao, d_filtro

def PainelDinamicoPln(expressao):
    expressao, d_filtro = Parametros(expressao)

    nlp = spacy.load('pt') # pt_core_news_sm
    doc = nlp(expressao)
    sents = [sent for sent in doc.sents]
    #tokenCalculoMedidas = [token for token in nlp('soma,média,mínimo,máximo') if token.is_punct == False]
    id_tabela = 53 # parte fixa no código
    listaObjColunas =  [coluna for coluna in meta.ListarColunas(id_tabela) if coluna.sinonimos != '']

    html = ''
    js = ''
    conta=0
    tokenFiltro = [token for token in nlp('onde')][0]

    for sent in sents:
        print(str(sent))
        existeFiltro = False
        sentencaTotal = str(sent)
        sentencaBase =  str(sent)
        sentencaFiltro = ''

        for token in sent:
            d_similaridade = tokenFiltro.similarity(token)
            print(str(token), d_similaridade)
            if tokenFiltro.similarity(token) > 0.9:
                sentencaFiltro = sentencaTotal[sentencaTotal.find(str(token)):]
                sentencaBase = sentencaTotal[:sentencaTotal.find(str(token))-1]
                print('existe filtro!')
                print('sentenca base:', sentencaBase)
                print('sentenca filtro:', sentencaFiltro)
                existeFiltro = True
                break
        
        sentFiltro = None
        if existeFiltro:
            sent = nlp(sentencaBase)
            sentFiltro = nlp(sentencaFiltro)

        conta+= 1
        caminho = "/static/images/sentence" + str(conta) + ".svg"

        if not existeFiltro:
            svg = displacy.render(sent, style="dep")
            output_path = Path("." + caminho)
            output_path.open("w", encoding="utf-8").write(svg)
            html += '<div class="row"><div class="col-lg-5"><img src="' + caminho + '" style="max-width: 120%" /></div>'
        else:
            svg = displacy.render(sent, style="dep")
            output_path = Path("." + caminho)
            output_path.open("w", encoding="utf-8").write(svg)

            caminhoFiltro = "/static/images/sentence" + str(conta) + "_filtro.svg"            
            svg = displacy.render(sentFiltro, style="dep")
            output_path = Path("." + caminhoFiltro)
            output_path.open("w", encoding="utf-8").write(svg)
            
            html += '<div class="row"><div class="col-lg-5"><img src="' + caminho + '" style="max-width: 100%" /><br><img src="' + caminhoFiltro + '" style="max-width: 100%" /></div>'

        tokens = [token for token in sent if not token.is_punct]
        
        colunasMedidas, colunasDimensoes = ProcessarSentenca(nlp, tokens, listaObjColunas)
        filtro = ' (final_result = \'\' or final_result LIKE \'LA :: Prev%\' )'
        if existeFiltro:
            tokensFiltros = [token for token in sentFiltro if not token.is_punct]
            filtro_medidas, filtro_dimensoes = ProcessarSentenca(nlp, tokensFiltros, listaObjColunas, tokenFiltro)
            print('filtro_ColMedida', filtro_medidas)
            print('filtro_ColDimensoes', filtro_dimensoes)

            conta=0
            for col in filtro_dimensoes:
                conta+= 1
                nomeParam = 'param' + str(conta)
                aux_filtro = col.nome+'= \'' + d_filtro[nomeParam] + '\''
                if filtro != '':
                    filtro += ' and ' + aux_filtro
                else:
                    filtro = aux_filtro

        df = None
        if len(colunasMedidas) == 0:
            df = GerarDfVisaoPln(id_tabela, listaObjColunas, [], filtro)
        else:
            df = GerarDfVisaoPln(id_tabela, colunasDimensoes, colunasMedidas, filtro)

        obj = GerarVisao(str(sent), df, colunasDimensoes, colunasMedidas)
        if obj != None:
            html += '<div class="col-lg-7">' + obj.grf + '</div>'
            js += obj.js
        
        html+= "</div>"

    return html, js

def GerarVisao(expressao, df, colunasDimensoes, colunasMedidas):
    if len(colunasMedidas) == 0 and len(colunasDimensoes) > 1:
        print('Informação em Grid')
        return comp.compGrid(expressao, list(df.T.to_dict().values()), colunasDimensoes)

    elif len(colunasDimensoes) == 0 and len(colunasMedidas) == 1:
        print('Informação em Cards')
        return comp.infCard(expressao, list(df.T.to_dict().values()), colunasMedidas)

    elif len(colunasDimensoes) == 1 and len(colunasMedidas) == 1:
        campoSerie = colunasDimensoes[0]
        campoValor = 'Sum_' + colunasMedidas[0].nome
        if len(df[campoSerie.nome].values) < 5:
            print('gráfico de pizza')
            return comp.grfPizza(expressao, df, campoSerie.nome, campoValor)

        else:
            print('gráfico de barras')
            return comp.grfBarras(expressao, df, campoSerie.nome, '', campoValor)

    elif len(colunasDimensoes) == 2 and len(colunasMedidas) == 1:
        campoSerie = colunasDimensoes[0]
        campoCateg = colunasDimensoes[1]
        campoValor = 'Sum_' + colunasMedidas[0].nome

        if len(df[campoSerie.nome].values) < 5:
            print('gráfico de barras')
            return comp.grfBarras(expressao, df, campoCateg.nome, campoSerie.nome, campoValor)

        else:
            print('gráfico de linhas!!!')
            return comp.grfBarras(expressao, df, campoCateg.nome, campoSerie.nome, campoValor)
            #return comp.grfLinhas('', df, campoCateg.nome, campoSerie.nome, campoValor)
			
    else:
        print('Operação não permitida')

    return None

def ProcessarSentenca(nlp, tokens, listaObjColunas, tokenFiltro=None):
    print('---------------------------------------------------------------------------')
    print('>>> ProcessarSentenca')
    print(tokens)
    colunasDimensoes=[]
    colunasMedidas=[]
    acumula_medidas = True
    e_filtro = False
    for token in tokens:
        print('---------------------------------------------------------------------------')
        print('palavra:', token.text)
        print('dep_ ' + token.dep_)
        print('head ' + str(token.head))
        print('pos_ ' + token.pos_)
        print('conjuncts ' + str(token.conjuncts))

        if not e_filtro and tokenFiltro != None:
            d_similaridde = tokenFiltro.similarity(token)
            if d_similaridde > 0.9:
                e_filtro = True
                print('é filtro (onde). palavra:', token.text, d_similaridde)
                continue

        
        if token.pos_ == 'ADP':
            acumula_medidas  = False
            continue

        if e_filtro and token.text[:5] == 'param':
            print('ignorado...')
            continue

        colunaSelecionada = None
        maiorSimilaridade = 0

        if token.pos_ != 'NOUN':
            continue

        for coluna in listaObjColunas:
            sinonimos = [tokenCol for tokenCol in nlp(coluna.sinonimos) if tokenCol.is_punct == False] 
            print('>>>>>')
            print('similaridades...')
            for sinonimo in sinonimos:
                d_similaridade = token.similarity(sinonimo)
                print(sinonimo.text)
                print(d_similaridade)
                if maiorSimilaridade < d_similaridade:
                    colunaSelecionada = coluna
                    maiorSimilaridade = d_similaridade
        print('\r')
        print('Coluna selecionada:', colunaSelecionada.nome,'(', colunaSelecionada.sinonimos, ')', maiorSimilaridade)

        if acumula_medidas and not e_filtro:
            colunasMedidas.append(colunaSelecionada)
        else:
            colunasDimensoes.append(colunaSelecionada)
    
    print('---------------------------------------------------------------------------------')
    print('Medidas', '(', len(colunasMedidas), ')')
    for col in colunasMedidas:
        print(col.nome)
    print('Dimensoes', '(', len(colunasDimensoes), ')')
    for col in colunasDimensoes:
        print(col.nome)

    return colunasMedidas, colunasDimensoes


def GerarDfVisaoPln(id_tabela, colunasDimensoes, colunasMedidas, filtro=''):
    # montar itens da visão
    listaColunas = []
    listaTodasColunas = []
    listaColunasExibGrd = []
    defColunasAgrp = {  }
    campoCateg = None
    filtroClasse = 'O'
    for coluna in colunasDimensoes:
        listaColunas.append(coluna.id)
        nomeCampo = coluna.nome

        if campoCateg == '':
            campoCateg = coluna.nome
        else:
            campoSerie = coluna.nome

        defColunasAgrp[coluna.id] = ''
        listaTodasColunas.append(nomeCampo)
        listaColunasExibGrd.append( {'campo': coluna.nome, 'titulo': coluna.titulo } )

    for coluna in colunasMedidas:
        listaColunas.append(coluna.id)
        nomeCampo = coluna.nome

        if coluna.tipo == 'N':
            defColunasAgrp[coluna.id] = 'Sum'

        listaTodasColunas.append(nomeCampo)
        listaColunasExibGrd.append( {'campo': coluna.nome, 'titulo': coluna.titulo } )

    sql = dbTab.GerarSQL(id_tabela, filtroClasse, listaColunas, True, defColunasAgrp, filtro)
    df = db.consultarSQLDataFrame(sql)
    for col in df.columns:
        if col == 'final_result':
            df[col][df[col] == 'LA :: Prev :: Falha'] = 'Falha'
            df[col][df[col] == 'LA :: Prev :: Sucesso'] = 'Sucesso'

    return df
