SELECT IFNULL((SELECT nm.NOME FROM __nomes_alunos AS nm WHERE CAST(nm.id_student AS INT) = CAST(std.id_student AS INT) LIMIT 1), 'DADO ANONIMO') AS Nome,
       IFNULL(stdvle.click_dataplus       , 0) AS click_dataplus,
       IFNULL(stdvle.click_dualpane       , 0) AS click_dualpane,
       IFNULL(stdvle.click_externalquiz   , 0) AS click_externalquiz,
       IFNULL(stdvle.click_folder         , 0) AS click_folder,
       IFNULL(stdvle.click_forumng        , 0) AS click_forumng,
       IFNULL(stdvle.click_glossary       , 0) AS click_glossary,
       IFNULL(stdvle.click_homepage       , 0) AS click_homepage,
       IFNULL(stdvle.click_htmlactivity   , 0) AS click_htmlactivity,
       IFNULL(stdvle.click_oucollaborate  , 0) AS click_oucollaborate,
       IFNULL(stdvle.click_oucontent      , 0) AS click_oucontent,
       IFNULL(stdvle.click_ouelluminate   , 0) AS click_ouelluminate,
       IFNULL(stdvle.click_ouwiki         , 0) AS click_ouwiki,
       IFNULL(stdvle.click_page           , 0) AS click_page,
       IFNULL(stdvle.click_questionnaire  , 0) AS click_questionnaire,
       IFNULL(stdvle.click_quiz           , 0) AS click_quiz,
       IFNULL(stdvle.click_repeatactivity , 0) AS click_repeatactivity,
       IFNULL(stdvle.click_resource       , 0) AS click_resource,
       IFNULL(stdvle.click_sharedsubpage  , 0) AS click_sharedsubpage,
       IFNULL(stdvle.click_subpage        , 0) AS click_subpage,
       IFNULL(stdvle.click_url            , 0) AS click_url,
       
       aval.TMA  AS TMA,
       aval.CMA  AS CMA,
       aval.Exam AS Exam,
          
       std.code_module          AS code_module,
       std.code_presentation    AS code_presentation,
       std.id_student           AS id_student,
       std.gender               AS gender,
       std.region               AS region,
       std.highest_education    AS highest_education,
       std.imd_band             AS imd_band,
       std.age_band             AS age_band,
       std.num_of_prev_attempts AS num_of_prev_attempts,
       std.studied_credits      AS studied_credits,
       std.disability           AS disability,
       std.final_result         AS final_result
  FROM __studentInfo std
  LEFT JOIN __interacoes_vle stdvle
    ON stdvle.id_student = std.id_student
   AND stdvle.code_module = std.code_module
   AND stdvle.code_presentation = std.code_presentation
  LEFT JOIN __avalicoes_alunos aval
    ON aval.id_student = std.id_student
   AND aval.code_module = std.code_module
   AND aval.code_presentation = std.code_presentation