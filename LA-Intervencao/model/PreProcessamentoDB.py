import model.dataBase as db
import model.MetaDadosDB as meta
import model.ImportacaoDB as imp


def RetornarValoresColuna(idTabela, idColuna):
    tabela = imp.ObterTabela(idTabela)
    coluna = meta.ObterColuna(idColuna)

    sql_table = tabela.nome
    if not (tabela.sql_destino == None or tabela.sql_destino == ''):
        sql_table = tabela.sql_destino

    sql = 'SELECT COUNT(*) AS qtd, ' + coluna.sql + ' as COL FROM "' + sql_table + '" GROUP BY COL'

    #resultado = db.consultarSQL(sql)
    resultado = db.consultarSQLDataFrame(sql)

    return resultado

def GerarSqlQuartil(tabela, coluna, tp):
    tpDisc = ''
    if tp == 'E':
        tpDisc = 'DISTINCT'

    sqlTexto = """
SELECT *,
       CASE WHEN coluna <= Q1 THEN 'Q1'
            WHEN coluna <= Q2 THEN 'Q2'
            WHEN coluna <= Q3 THEN 'Q3'
       ELSE 'Q4'
       END AS QUARTIL
  FROM (
SELECT *,
       (SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) AS QTD,
       (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}} ORDER BY 1 LIMIT (((SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) / 4) * 1), 1) Q1,
       (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}} ORDER BY 1 LIMIT (((SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) / 4) * 2), 1) Q2,
       (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}} ORDER BY 1 LIMIT (((SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) / 4) * 3), 1) Q3
  FROM (
SELECT {{tpQuartil}} {{coluna}} AS coluna
  FROM {{tabela}}) AS T
 ORDER BY 1
) AS T
LIMIT 1"""

    sqlNumero = """
SELECT *,
       CASE WHEN coluna <= Q1 THEN 'Q1'
            WHEN coluna <= Q2 THEN 'Q2'
            WHEN coluna <= Q3 THEN 'Q3'
       ELSE 'Q4'
       END AS QUARTIL
  FROM (
SELECT *,
       (SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) AS QTD,
       (SELECT {{tpQuartil}} CAST({{coluna}} AS FLOAT) FROM {{tabela}} ORDER BY 1 LIMIT (((SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) / 4) * 1), 1) Q1,
       (SELECT {{tpQuartil}} CAST({{coluna}} AS FLOAT) FROM {{tabela}} ORDER BY 1 LIMIT (((SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) / 4) * 2), 1) Q2,
       (SELECT {{tpQuartil}} CAST({{coluna}} AS FLOAT) FROM {{tabela}} ORDER BY 1 LIMIT (((SELECT COUNT(*) FROM (SELECT {{tpQuartil}} {{coluna}} FROM {{tabela}})) / 4) * 3), 1) Q3
  FROM (
SELECT {{tpQuartil}} CAST({{coluna}} AS FLOAT) AS coluna
  FROM {{tabela}}) AS T
 ORDER BY 1
) AS T
LIMIT 1"""

    objTabela = imp.ObterTabelaPorNome(tabela)
    objColuna = meta.ObterColunaPorTabNome(objTabela.id, coluna)
    if objColuna.tipo == 'N':
        sql = sqlNumero.replace('{{tabela}}', tabela).replace('{{coluna}}', coluna).replace('{{tpQuartil}}', tpDisc)
    else:
        sql = sqlTexto.replace('{{tabela}}', tabela).replace('{{coluna}}', coluna).replace('{{tpQuartil}}', tpDisc)

    resultado = db.consultarSQLDataFrame(sql)

    if objColuna.tipo == 'N':
        sqlResultado = 'CASE WHEN CAST(' + str(coluna) + ' AS FLOAT) <= ' + str(resultado['Q1'][0]) + ' THEN \'Q1\' WHEN CAST(' + str(coluna) + ' AS FLOAT) <= ' + str(resultado['Q2'][0]) + ' THEN \'Q2\'  WHEN CAST(' + str(coluna) + ' AS FLOAT) <= ' + str(resultado['Q3'][0]) + ' THEN \'Q3\' ELSE \'Q4\' END'
    else:
        sqlResultado = 'CASE WHEN ' + str(coluna) + ' <= ' + str(resultado['Q1'][0]) + ' THEN \'Q1\' WHEN ' + str(coluna) + ' <= ' + str(resultado['Q2'][0]) + ' THEN \'Q2\'  WHEN ' + str(coluna) + ' <= ' + str(resultado['Q3'][0]) + ' THEN \'Q3\' ELSE \'Q4\' END'

    return sqlResultado

def DiscretizarCampo(idColuna, nome, expressao):
    colunaDiscr = meta.ObterColuna(idColuna)
    colunaDiscr.sql = expressao

    meta.SalvarColuna(colunaDiscr)

