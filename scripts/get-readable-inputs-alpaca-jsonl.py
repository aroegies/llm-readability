from readability import Readability
import json, sys, os, csv
from nltk.tokenize import word_tokenize



cldict = dict()
fkdict = dict()
dcdict = dict()
count = 0
score_count = 0

csvfil = open(sys.argv[2],'w')
csvw = csv.writer(csvfil, delimiter=',',quotechar='"' )
with open(sys.argv[1]) as responses:
#   elts = json.load(responses)
   for prompt in responses:
      elt = json.loads(prompt)
      text = elt['output']
      words = word_tokenize(text)
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
        dcdict[dc.grade_levels[0]] = dcdict.get(dc.grade_levels[0],0)+1  
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
        csvw.writerow([elt['instruction'].replace("\n","\t"),elt['input'].replace("\n","\t")])
        #print(elt['instruction'].replace("\n","\t"),"\t",elt['input'].replace("\n","\t"))
      except:
        continue

