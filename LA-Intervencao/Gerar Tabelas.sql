------------------------------------------------------------------------------------------
-- GERAR Descrição dos Módulos
------------------------------------------------------------------------------------------

SELECT 'AAA' AS code_module,
       'Linguagem de Programação' AS descr_modeule
UNION 
SELECT 'BBB' AS code_module,
       'Redes de Computadores' AS descr_modeule
UNION 
SELECT 'CCC' AS code_module,
       'Banco de Dados' AS descr_modeule
UNION 
SELECT 'DDD' AS code_module,
       'Estrutura de Dados' AS descr_modeule       
UNION 
SELECT 'EEE' AS code_module,
       'Engenharia de Software' AS descr_modeule
UNION 
SELECT 'FFF' AS code_module,
       'Arquitetura de Computadores' AS descr_modeule
UNION 
SELECT 'GGG' AS code_module,
       'Gerenciamento de Projetos' AS descr_modeule;
	   
------------------------------------------------------------------------------------------
-- GERAR Nomes de uma base de dados exemplo
------------------------------------------------------------------------------------------

SELECT 'SELECT ' || '''' || First_NAME || ' ' || LAST_NAME || ''' AS NOME UNION'
  FROM __student LIMIT 400;

SELECT 'Kayla Jimenez' AS NOME UNION
SELECT 'Rene Ramos' AS NOME UNION
(...)
SELECT 'Jenny Sullivan' AS NOME UNION
SELECT 'Ellie Nguyen' AS NOME UNION
  


SELECT code_module, 
       code_presentation, 
       COUNT(*)
  FROM __studentInfo
 GROUP BY
       code_module, 
       code_presentation;
	   

