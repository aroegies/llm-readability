from readability import Readability
import json, sys, os, re
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer



cldict = dict()
fkdict = dict()
dcdict = dict()
count = 0
score_count = 0
tokenizer = TweetTokenizer()
porter_stemmer = PorterStemmer()


def syllable_count(word):
    """
    Simple syllable counting
    """

    word = word if type(word) is str else str(word)

    word = word.lower()

    if len(word) <= 3:
        return 1

    word = re.sub('(?:[^laeiouy]es|[^laeiouy]e)$', '', word) # removed ed|
    word = re.sub('^y', '', word)
    matches = re.findall('[aeiouy]{1,2}', word)
    return len(matches)

def is_punct(token):
  match = re.match('^[.,\/#!$%\'\^&\*;:{}=\-_`~()]$', token)
  return match is not None

dale_chall_set = set()
with open("scripts/dale_chall_porterstem.txt") as dcfil:
  dale_chall_set = set(line.strip() for line in dcfil)

def is_dale_chall_complex(t):
  stem = porter_stemmer.stem(t.lower())
  return stem not in dale_chall_set

with open(sys.argv[1]) as responses:
#   elts = json.load(responses)
   for prompt in responses:
      elt = json.loads(prompt)
      text = elt['response']
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
      except:
        tokens = tokenizer.tokenize(text)
        word_count = 0
        dc_complex = 0
        chars_count = 0
        syll_count = 0
        for t in tokens:
          if not is_punct(t):
            word_count+=1
            chars_count += len(t)
            dc_complex += 1 if is_dale_chall_complex(t) else 0
            syll_count += syllable_count(t) 
        if word_count != 0:
          print(word_count, dc_complex/word_count, chars_count/word_count,syll_count/word_count)
        continue
