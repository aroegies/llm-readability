from readability import Readability
import json, sys, os
from nltk.tokenize import TweetTokenizer



cldict = dict()
fkdict = dict()
dcdict = dict()
count = 0 
score_count = 0
tokenizer = TweetTokenizer()
resplen = 0
with open(sys.argv[1]) as responses:
   #elts = json.load(responses)
   for line in responses:
      elt = json.loads(line)
      text = elt['response']
      words = tokenizer.tokenize(text)
      count+=1
      try:
        scores = Readability(text)
        fk = scores.flesch_kincaid()
        gl = 13
        if int(fk.grade_level) <= 6:
          gl = 6
        elif int(fk.grade_level) <= 9:
          gl = 9
        elif int(fk.grade_level) <= 12:
          gl = 12

        fkdict[gl] = fkdict.get(gl,0)+1
        dc = scores.dale_chall()
        dcgrade = dc.grade_levels[0]
        dcgl = 13
        if dcgrade == '1' or dcgrade == '5':
            dcgl = 6
        elif dcgrade == '7' or dcgrade == '9':
            dcgl = 9
        elif dcgrade == '11':
            dcgl = 12
        cl = scores.coleman_liau()
        gl = 13
        if int(cl.grade_level) <= 6:
          gl = 6
        elif int(cl.grade_level) <= 9:
          gl = 9
        elif int(cl.grade_level) <= 12:
          gl = 12
        cldict[gl] = cldict.get(gl,0)+1
        score_count+=1
        resplen += len(words)
      except:
        continue

print("Flesch-Kincaid")
for k,v in fkdict.items():
  print(k,v)

print("===================")

print("Dale-Chall")
for k,v in dcdict.items():
  print(k,v)

print("===================")

print("Coleman-Liau")
for k,v in cldict.items():
  print(k,v)
print("==================")
print(count,score_count,resplen/score_count)
