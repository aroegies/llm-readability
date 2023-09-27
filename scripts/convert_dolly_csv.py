import json, sys, os, csv

writerfil = open(sys.argv[2],'w')

writer = csv.writer(writerfil,delimiter=',',quotechar='"')
with open(sys.argv[1]) as responses:
   for line in responses:
     elt = json.loads(line)
     writer.writerow([elt['instruction'],elt['context'],elt['response']])
writerfil.close()