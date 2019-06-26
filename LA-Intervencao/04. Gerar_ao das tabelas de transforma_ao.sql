------------------------------------------------------------------------------------------
--						CHEGAR INEXISTÊNCIA DE REGISTOS
------------------------------------------------------------------------------------------
SELECT *
  FROM __studentInfo AS std
 WHERE NOT EXISTS (
SELECT *
  FROM __studentVle AS stdVle
 WHERE stdVle.id_student = std.id_student
 LIMIT 1);
 
SELECT *
  FROM __studentInfo AS std
 WHERE NOT EXISTS (
SELECT *
  FROM __studentAssessment AS stdas
 WHERE stdas.id_student = std.id_student
  LIMIT 1);

------------------------------------------------------------------------------------------
SELECT *
  FROM __studentInfo;
 
------------------------------------------------------------------------------------------
-- LISTAR ESTUDANTES COM AS NOTAS
------------------------------------------------------------------------------------------

SELECT SUM(CASE WHEN assmt.assessment_type = 'TMA'  THEN stdas.score ELSE 0 END) AS TMA,
       SUM(CASE WHEN assmt.assessment_type = 'CMA'  THEN stdas.score ELSE 0 END) AS CMA,
       SUM(CASE WHEN assmt.assessment_type = 'Exam' THEN stdas.score ELSE 0 END) AS Exam,
       
       std.id_student        AS id_student,
       std.code_module       AS code_module,
       std.code_presentation AS code_presentation
  FROM __studentInfo AS std
  LEFT JOIN __studentAssessment AS stdas
    ON stdas.id_student = std.id_student
  LEFT JOIN __assessments AS assmt
    ON assmt.id_assessment = stdas.id_assessment
 --WHERE std.id_student = '28400' somente para validar registros
 GROUP BY
       std.id_student,
       std.code_module,
       std.code_presentation;
	   
------------------------------------------------------------------------------------------
-- LISTAR AS INTERAÇÕES DOS ESTUDANTES NO VLE
------------------------------------------------------------------------------------------
SELECT SUM(CASE WHEN vle.activity_type = 'dataplus'       THEN stdVle.sum_click ELSE 0 END) AS click_dataplus,
       SUM(CASE WHEN vle.activity_type = 'dualpane'       THEN stdVle.sum_click ELSE 0 END) AS click_dualpane,
       SUM(CASE WHEN vle.activity_type = 'externalquiz'   THEN stdVle.sum_click ELSE 0 END) AS click_externalquiz,
       SUM(CASE WHEN vle.activity_type = 'folder'         THEN stdVle.sum_click ELSE 0 END) AS click_folder,
       SUM(CASE WHEN vle.activity_type = 'forumng'        THEN stdVle.sum_click ELSE 0 END) AS click_forumng,
       SUM(CASE WHEN vle.activity_type = 'glossary'       THEN stdVle.sum_click ELSE 0 END) AS click_glossary,
       SUM(CASE WHEN vle.activity_type = 'homepage'       THEN stdVle.sum_click ELSE 0 END) AS click_homepage,
       SUM(CASE WHEN vle.activity_type = 'htmlactivity'   THEN stdVle.sum_click ELSE 0 END) AS click_htmlactivity,
       SUM(CASE WHEN vle.activity_type = 'oucollaborate'  THEN stdVle.sum_click ELSE 0 END) AS click_oucollaborate,
       SUM(CASE WHEN vle.activity_type = 'oucontent'      THEN stdVle.sum_click ELSE 0 END) AS click_oucontent,
       SUM(CASE WHEN vle.activity_type = 'ouelluminate'   THEN stdVle.sum_click ELSE 0 END) AS click_ouelluminate,
       SUM(CASE WHEN vle.activity_type = 'ouwiki'         THEN stdVle.sum_click ELSE 0 END) AS click_ouwiki,
       SUM(CASE WHEN vle.activity_type = 'page'           THEN stdVle.sum_click ELSE 0 END) AS click_page,
       SUM(CASE WHEN vle.activity_type = 'questionnaire'  THEN stdVle.sum_click ELSE 0 END) AS click_questionnaire,
       SUM(CASE WHEN vle.activity_type = 'quiz'           THEN stdVle.sum_click ELSE 0 END) AS click_quiz,
       SUM(CASE WHEN vle.activity_type = 'repeatactivity' THEN stdVle.sum_click ELSE 0 END) AS click_repeatactivity,
       SUM(CASE WHEN vle.activity_type = 'resource'       THEN stdVle.sum_click ELSE 0 END) AS click_resource,
       SUM(CASE WHEN vle.activity_type = 'sharedsubpage'  THEN stdVle.sum_click ELSE 0 END) AS click_sharedsubpage,
       SUM(CASE WHEN vle.activity_type = 'subpage'        THEN stdVle.sum_click ELSE 0 END) AS click_subpage,
       SUM(CASE WHEN vle.activity_type = 'url'            THEN stdVle.sum_click ELSE 0 END) AS click_url,    
       
       stdVle.id_student        AS id_student,
       stdVle.code_module       AS code_module,
       stdVle.code_presentation AS code_presentation
  FROM __studentVle stdVle
 INNER JOIN __vle AS vle
    ON vle.id_site = stdVle.id_site
 GROUP BY
       stdVle.id_student,
       stdVle.code_module,
       stdVle.code_presentation;