import spacy
from spacy import displacy
from pathlib import Path

nlp = spacy.load('pt')

doc = nlp(u'Quantidade de alunos por disciplina e resultado visualizado como gráfico de barras. Quantidade de dados por usuário.')
print(doc)
sents = [sent for sent in doc.sents]
print(sents)
