import spacy
from spacy import displacy
from pathlib import Path

nlp = spacy.load('pt')

doc = nlp(u'Quantidade de alunos por disciplina e resultado visualizado como gráfico de barras.')
print(dir(doc))

print('--------------------------------------------------------------------')
print('Token')
tokens = [token for token in doc]
print(tokens)
print(dir(tokens[0])) # obter membros

print('--------------------------------------------------------------------')
print('Texto do Token')
tokens_txt = [token.orth_ for token in doc]
print(tokens_txt)

print('--------------------------------------------------------------------')
print('Texto do Token sem pontuação')
tokens_txt = [token.orth_ for token in doc if not token.is_punct]
print(tokens_txt)

print('--------------------------------------------------------------------')
print('Similaridade "de" e "por"')
print(tokens[1].similarity(tokens[3]))

print('--------------------------------------------------------------------')
print('Classes das palavras (pos-tag)')
palavras_classes = [(token.orth_, token.pos_) for token in doc]
print(palavras_classes)

print('--------------------------------------------------------------------')
print('Classes filtradas por NOUN - substantivo')
palavras_substantivo = [(token.orth_, token.pos_) for token in doc if token.pos_ == 'NOUN']
print(palavras_substantivo)

print('Sentido primitivo das palavras - ideal para verbos')
lemmas = [token.lemma_ for token in doc]
print(lemmas)


print('--------------------------------------------------------------------')
print('Visualização do Texto')
svg = displacy.render(doc, style="dep")
#print(svg)
output_path = Path("sentence.svg")
print(output_path)
output_path.open("w", encoding="utf-8").write(svg)


# Part-of-speech tagging
# ------+----------------------------+-------------------------------------------------
# POS   | DESCRIPTION                | EXAMPLES
# ADJ   | adjective                  | big, old, green, incomprehensible, first
# ADP   | adposition                 | in, to, during
# ADV   | adverb                     | very, tomorrow, down, where, there
# AUX   | auxiliary                  | is, has (done), will (do), should (do)
# CONJ  | conjunction                | and, or, but
# CCONJ | coordinating conjunction   | and, or, but
# DET   | determiner                 | a, an, the
# INTJ  | interjection               | psst, ouch, bravo, hello
# NOUN  | noun                       | girl, cat, tree, air, beauty
# NUM   | numeral                    | 1, 2017, one, seventy-seven, IV, MMXIV
# PART  | particle                   | ’s, not,
# PRON  | pronoun                    | I, you, he, she, myself, themselves, somebody
# PROPN | proper                     | noun Mary, John, London, NATO, HBO
# PUNCT | punctuation                | ., (, ), ?
# SCONJ | subordinating conjunction  | if, while, that
# SYM   | symbol                     | $, %, §, ©, +, −, ×, ÷, =, :), 😝
# VERB  | verb                       | run, runs, running, eat, ate, eating
# X     | other                      | sfpksdpsxmsa
# SPACE | space                      |


# Syntactic Dependency Parsing
# -----------+-------------------------------------------------------------------------
# LABEL      | DESCRIPTION
# acl        | clausal modifier of noun (adjectival clause)
# advcl      | adverbial clause modifier
# advmod     | adverbial modifier
# amod       | adjectival modifier
# appos      | appositional modifier
# aux        | auxiliary
# case       | case marking
# cc         | coordinating conjunction
# ccomp      | clausal complement
# clf        | classifier
# compound   | compound
# conj       | conjunct
# cop        | copula
# csubj      | clausal subject
# dep        | unspecified dependency
# det        | determiner
# discourse  | discourse element
# dislocated | dislocated elements
# expl       | expletive
# fixed      | fixed multiword expression
# flat       | flat multiword expression
# goeswith   | goes with
# iobj       | indirect object
# list       | list
# mark       | marker
# nmod       | nominal modifier
# nsubj      | nominal subject
# nummod     | numeric modifier
# obj        | object
# obl        | oblique nominal
# orphan     | orphan
# parataxis  | parataxis
# punct      | punctuation
# reparandum | overridden disfluency
# root       | root
# vocative   | vocative
# xcomp      | open clausal complement
