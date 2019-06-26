import model.dataBase as db
import model.MetaDadosDB as meta
import model.ImportacaoDB as imp
import model.VisaoDB as vis
import controls.componentes as comp
import json


def GerarSQL(idTabela, filtroClasse = '', somenteColunas = [], agrupar=False, defColunasAgrp = { }, filtroSql=''):
    """ filtroClasse
         S = sem classe     = para TREINAR
         O = somente classe = para PREVER
    """

    tabela = imp.ObterTabela(idTabela)
    listaColunas = meta.ListarColunas(idTabela)
    listaExibicao = ListarExibicao(idTabela)
    conta_tb = 0

    sql_table = '[' + tabela.nome + ']'
    if not (tabela.sql_destino == None or tabela.sql_destino == ''):
        sql_table = '(' + tabela.sql_destino + ')'

    sql_table = sql_table

    sql = ''
    sql_coluna = '       rowid'
    sql_coluna_classe = ''
    sql_inner_join = ''
    sql_where = '\n WHERE 0=0 \n'
    sql_group = ''

    if agrupar == True:
        sql_group = ''

    for col in listaColunas:
        if col.desabilitado == True:
            existeSomenteCol = False
            for idCol in somenteColunas:
                if int(idCol) == col.id:
                    existeSomenteCol = True
            if existeSomenteCol == False:
                continue

        if len(somenteColunas) != 0:
            existeFiltroColuna = False
            for idCol in somenteColunas:
                if int(idCol) == int(col.id):
                    existeFiltroColuna = True

            if existeFiltroColuna == False:
                continue

        sql_coluna_tmp = col.sql.replace(col.nome, 't0.' + col.nome)
        sql_coluna_one = sql_coluna_tmp + ' AS ' + col.nome

        if agrupar == True:
            if defColunasAgrp[col.id] != '':
                sql_coluna_one = defColunasAgrp[col.id] + '(' + sql_coluna_tmp + ') AS ' + defColunasAgrp[col.id] + '_' + col.nome
            elif defColunasAgrp[col.id] == '':
                if sql_group == '':
                    sql_group = ' GROUP BY ' + sql_coluna_tmp
                else:
                    sql_group = sql_group + ',' + sql_coluna_tmp

        if col.classe:
            sql_coluna_classe = sql_coluna_one
            if filtroClasse == 'S':
                sql_where += ' AND ' + sql_coluna_tmp + ' IS NOT NULL \n'
                sql_where += ' AND ' + sql_coluna_tmp + ' <> \'\' \n'
                sql_where += ' AND ' + sql_coluna_tmp + ' <> \'?\' \n'
                sql_where += ' AND ' + sql_coluna_tmp + ' NOT LIKE \'LA :: Prev%\' \n'
            elif filtroClasse == 'O':
                sql_where += ' AND (' + sql_coluna_tmp + ' IS NULL \n'
                sql_where += '  OR  ' + sql_coluna_tmp + ' = \'\' \n'
                sql_where += '  OR  ' + sql_coluna_tmp + ' = \'?\' \n'
                sql_where += '  OR  ' + sql_coluna_tmp + ' LIKE \'LA :: Prev%\' ) \n'
        elif sql_coluna == '':
            sql_coluna = '       ' + sql_coluna_one
        else:
            sql_coluna = sql_coluna + ', \n       ' + sql_coluna_one

    tabelasJoin = {  }

    for colExib in listaExibicao:

        col = meta.ObterColuna(colExib.id_coluna)
        col_fk = meta.ObterColuna(col.id_coluna_fk)
        col_lookup = meta.ObterColuna(colExib.id_coluna_fk)
        tabela_fk = imp.ObterTabela(colExib.id_tabela_fk)

        if col_lookup.desabilitado == True:
            continue

        if len(somenteColunas) != 0:
            existeFiltroColuna = False
            for idCol in somenteColunas:
                if int(idCol) == int(col_lookup.id):
                    existeFiltroColuna = True

            if existeFiltroColuna == False:
                continue

        sql_table_join = tabela_fk.nome
        if (tabela_fk.sql_destino != None):
            sql_table_join = tabela_fk.sql_destino

        prefixo = ''
        tb_corrente = -1
        if tabela_fk.nome in tabelasJoin:
            tb_corrente = tabelasJoin[tabela_fk.nome]
            prefixo = 't' + str(tb_corrente)
        else:
            conta_tb = conta_tb + 1
            tb_corrente = conta_tb
            prefixo = 't' + str(tb_corrente)
            tabelasJoin[tabela_fk.nome] = conta_tb
            tb_corrente = conta_tb

            sql_inner_join = sql_inner_join + ' INNER JOIN ' + sql_table_join  + ' AS ' + prefixo + ' ON t0.' + col.nome + ' = ' + prefixo + '.' + col_fk.nome

        sql_coluna_tmp = col_lookup.sql.replace(col.nome, prefixo + '.' + col_lookup.nome)
        sql_coluna_one = sql_coluna_tmp + ' AS ' + col_lookup.nome

        if agrup == True:
            if sql_group == '':
                sql_group = ' GROUP BY ' + sql_coluna_tmp
            else:
                sql_group = sql_group + ',' + sql_coluna_tmp


        if col_lookup.classe:
            sql_coluna_classe = sql_coluna_one
            if filtroClasse == 'S':
                sql_where += ' AND ' + sql_coluna_tmp + ' IS NOT NULL'
                sql_where += ' AND ' + sql_coluna_tmp + ' <> \'\' '
                sql_where += ' AND ' + sql_coluna_tmp + ' <> \'?\' '
                sql_where += ' AND ' + sql_coluna_tmp + ' NOT LIKE \'LA :: Prev%\' '
            elif filtroClasse == 'O':
                sql_where += ' AND (' + sql_coluna_tmp + ' IS NULL'
                sql_where += '  OR  ' + sql_coluna_tmp + ' = \'\' '
                sql_where += '  OR  ' + sql_coluna_tmp + ' = \'?\' '
                sql_where += '  OR  ' + sql_coluna_tmp + ' LIKE \'LA :: Prev%\' )'

        else:
            sql_coluna = sql_coluna + ', ' + sql_coluna_one


    if sql_coluna_classe != '':
        sql_coluna = sql_coluna + ', ' + sql_coluna_classe

    if filtroSql != '':
        sql_where+= '\n and ' + filtroSql


    sql = 'SELECT \n' + sql_coluna + ' FROM \n' + sql_table + ' as t0 ' + sql_inner_join + sql_where + '\n' + sql_group

    print('GerarSQL:')
    print(sql)

    return sql

def ListarDados(idTabela, idColunas):
    sql = GerarSQL(idTabela, '', idColunas)
    resultado = db.consultarSQL(sql)

    return resultado

def InformDados(idTabela, idColunas):

    sql = GerarSQL(idTabela, '', idColunas, True)


    return resultado

def ListarExibicao(idTabela):
    session = db.getSession()
    lista = session.query(db.ExibicaoColuna).filter_by(id_tabela=idTabela).all()
    session.close()

    return lista

def ListarExibicaoColuna(idTabela, idColuna):
    session = db.getSession()
    lista = session.query(db.ExibicaoColuna).filter_by(id_tabela=idTabela).filter_by(id_coluna=idColuna).all()
    session.close()

    return lista

def GerarVisao(id):
    visao = vis.ObterVisao(id)
    tabela = imp.ObterTabela(visao.id_tabela)
    modelo = json.loads(visao.modelo)

    tipo = visao.tipo

    listaColunas = []
    listaTodasColunas = []
    listaColunasExibGrd = []
    defColunasAgrp = {  }
    campoCateg = None
    campoSerie = None
    campoValor = None
    filtroClasse = ''
    colunaClasse = ''
    for mod in modelo:
        id_coluna = int(mod['id_coluna'])
        listaColunas.append(id_coluna)
        coluna = meta.ObterColuna(id_coluna)

        nomeCampo = coluna.nome

        if coluna.classe:
            filtroClasse = 'O'
            colunaClasse = coluna.nome

        if mod['agrupador'] != '':
            nomeCampo = mod['agrupador'] + '_' + coluna.nome

        if mod['grafico'] == 'S':
            campoSerie = coluna
        elif mod['grafico'] == 'C':
            campoCateg = coluna
        elif mod['grafico'] == 'V':
            if mod['agrupador'] != '':
                campoValor = mod['agrupador'] + '_' + coluna.nome
            else:
                campoValor = coluna.nome

        defColunasAgrp[id_coluna] = mod['agrupador']
        listaTodasColunas.append(nomeCampo)
        listaColunasExibGrd.append( {'campo': coluna.nome, 'titulo': coluna.titulo } )

    sql = GerarSQL(visao.id_tabela, filtroClasse, listaColunas, True, defColunasAgrp)
    df = db.consultarSQLDataFrame(sql)

    if filtroClasse == 'O':
        valoresClasse = df[colunaClasse]
        for index, row in df.iterrows():
            df[colunaClasse][index] = str(row[colunaClasse]).replace('LA :: Prev :: ', '')


    obj = comp.defGrafico('', '')

    if tipo == '1': #  Gráfico de Pizza
        print('Gráfico de Pizza')
        obj = comp.grfPizza(visao.nome, df, campoSerie.nome, campoValor, '')
    elif tipo == '2': # Gráfico Barras
        print('Gráfico Barras')
        obj = comp.grfBarras(visao.nome, df, campoCateg.nome, campoSerie.nome, campoValor)
    elif tipo == '3': # Gráfico Linha
        print('Gráfico Linha')
        obj = comp.grfLinhas(visao.nome, df, campoCateg.nome, campoSerie.nome, campoValor)
    elif tipo == '4': # Informação em Cards
        print('Informação em Cards')
        obj = comp.infCard(visao.nome, list(df.T.to_dict().values()), listaTodasColunas)
    elif tipo == '5': # Informação em Grid
        print('Informação em Grid')
        obj = comp.compGrid(visao.nome, list(df.T.to_dict().values()), listaColunasExibGrd)

    return obj

def GerarSQLTop10(idTabela):
    return GerarSQL(idTabela) + ' LIMIT 10'

def ListarDadosTOP10(idTabela):
    sql = GerarSQLTop10(idTabela)
    resultado = db.consultarSQL(sql)

    return resultado


