
import sys, json
from llama_cpp import Llama

llm  = Llama(model_path=sys.argv[4], n_gqa=8, n_ctx=2048)
outfile = open(sys.argv[2],'w')
with open(sys.argv[1]) as promptsfil:
  count=0
  for prompttxt in promptsfil:
    prompt=json.loads(prompttxt)
    msg= prompt['instruction']+"\n"+ prompt['input']
    response = llm(msg,temperature=1.0,max_tokens=-1)
    prompt['output']=response
    outfile.write(json.dumps(prompt))
    outfile.write("\n")
    count+=1
    if (count % 100) == 0:
      print("Sleeping: ", count)
