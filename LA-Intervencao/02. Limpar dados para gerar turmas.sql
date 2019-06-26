Limpar dados para gerar turmas



SELECT code_module, 
       code_presentation, 
       COUNT(*)
  FROM __studentInfo
 GROUP BY
       code_module, 
       code_presentation;
       
SELECT code_module, 
       code_presentation, 
       id_student, 
       final_result
  FROM __studentInfo
 WHERE code_module = 'AAA'
   AND code_presentation LIKE '2014%'
 ORDER BY 
       RANDOM() 
 LIMIT 5;
 
SELECT code_module, 
       code_presentation, 
       id_student, 
       final_result
  FROM __studentInfo
 WHERE code_module = 'BBB'
   AND code_presentation LIKE '2014%'
 ORDER BY 
       RANDOM() 
 LIMIT 5;
 
SELECT code_module, 
       code_presentation, 
       id_student, 
       final_result
  FROM __studentInfo
 WHERE code_module = 'CCC'
   AND code_presentation LIKE '2014%'
 ORDER BY RANDOM() 
 LIMIT 5;
 
SELECT code_module, 
       code_presentation, 
       id_student, 
       final_result
  FROM __studentInfo
 WHERE code_module = 'DDD'
   AND code_presentation LIKE '2014%'
 ORDER BY RANDOM() 
 LIMIT 5;
 
SELECT code_module, 
       code_presentation, 
       id_student, 
       final_result
  FROM __studentInfo
 WHERE code_module = 'EEE'
   AND code_presentation LIKE '2014%'
 ORDER BY RANDOM() 
 LIMIT 5;
 
SELECT code_module, 
       code_presentation, 
       id_student, 
       final_result
  FROM __studentInfo
 WHERE code_module = 'FFF'
   AND code_presentation LIKE '2014%'
 ORDER BY RANDOM() 
 LIMIT 5;
 
SELECT code_module, 
       code_presentation, 
       id_student, 
       final_result
  FROM __studentInfo
 WHERE code_module = 'GGG'
   AND code_presentation LIKE '2014%'
 ORDER BY RANDOM() 
 LIMIT 5;