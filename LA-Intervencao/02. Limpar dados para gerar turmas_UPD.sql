UPDATE __studentInfo
   SET final_result = ''
 WHERE id_student IN ('447481', '2404408', '298034', '2649800', '260355')
   AND code_module = 'AAA'
   AND code_presentation = '2014J';

SELECT *
  FROM __studentInfo
 WHERE id_student IN ('447481', '2404408', '298034', '2649800', '260355')
   AND code_module = 'AAA'
   AND code_presentation = '2014J';

-------------------------------------------------------------------------------------

UPDATE __studentInfo
   SET final_result = ''
WHERE id_student IN ('633212', '608134', '631341', '627948', '679504')
   AND code_module = 'BBB'
   AND code_presentation LIKE '2014%';

SELECT *
  FROM __studentInfo
 WHERE id_student IN ('633212', '608134', '631341', '627948', '679504')
   AND code_module = 'BBB'
   AND code_presentation LIKE '2014%';

-------------------------------------------------------------------------------------

UPDATE __studentInfo
   SET final_result = ''
 WHERE id_student IN ('532020', '465331', '2559144', '645698', '554459')
  AND code_module = 'CCC'
  AND code_presentation LIKE '2014%';
 
SELECT *
  FROM __studentInfo
 WHERE id_student IN ('532020', '465331', '2559144', '645698', '554459')
  AND code_module = 'CCC'
  AND code_presentation LIKE '2014%';

-------------------------------------------------------------------------------------

UPDATE __studentInfo
   SET final_result = ''
 WHERE id_student IN ('676865', '477180', '154073', '2611371', '2542116')
  AND code_module = 'DDD'
  AND code_presentation LIKE '2014%';
 
SELECT *
  FROM __studentInfo
 WHERE id_student IN ('676865', '477180', '154073', '2611371', '2542116')
  AND code_module = 'DDD'
  AND code_presentation LIKE '2014%';

-------------------------------------------------------------------------------------

UPDATE __studentInfo
   SET final_result = ''
 WHERE id_student IN ('479987', '1663815', '652606', '630047', '683728')
   AND code_module = 'EEE'
   AND code_presentation LIKE '2014%';
 
SELECT *
  FROM __studentInfo
 WHERE id_student IN ('479987', '1663815', '652606', '630047', '683728')
   AND code_module = 'EEE'
   AND code_presentation LIKE '2014%';
   
-------------------------------------------------------------------------------------

UPDATE __studentInfo
   SET final_result = ''
 WHERE id_student IN ('602571', '633505', '697998', '629686')
   AND code_module = 'FFF'
   AND code_presentation LIKE '2014%';
 
SELECT *
  FROM __studentInfo
 WHERE id_student IN ('602571', '633505', '697998', '629686')
   AND code_module = 'FFF'
   AND code_presentation LIKE '2014%';

UPDATE __studentInfo
   SET final_result = ''
 WHERE id_student IN ('562064')
   AND code_module = 'FFF'
   AND code_presentation LIKE '2014%'
   AND num_of_prev_attempts = '1';
 
SELECT *
  FROM __studentInfo
 WHERE id_student IN ('562064')
   AND code_module = 'FFF'
   AND code_presentation LIKE '2014%'
   AND num_of_prev_attempts = '1';
   
-------------------------------------------------------------------------------------

UPDATE __studentInfo
   SET final_result = ''
  WHERE id_student IN ('621342', '674927', '614249', '651436', '513166')
   AND code_module = 'GGG'
   AND code_presentation LIKE '2014%';
 
SELECT *
  FROM __studentInfo
 WHERE id_student IN ('621342', '674927', '614249', '651436', '513166')
   AND code_module = 'GGG'
   AND code_presentation LIKE '2014%';

SELECT *
  FROM __studentInfo
 WHERE final_result = '';