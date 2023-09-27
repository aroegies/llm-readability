from readability import Readability
import json, sys, os
from nltk.tokenize import word_tokenize



with open(sys.argv[1]) as responses:
   elts = json.load(responses)
   for elt in elts:
      text = elt['output']
      words = word_tokenize(text)
      try:
        scores = Readability(text)
        fk = scores.flesch_kincaid()
#        print(json.dumps(elt))
      except:
        print(json.dumps(elt))
        continue
