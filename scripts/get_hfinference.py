import sys, json
from huggingface_hub import InferenceClient
from tenacity import retry,wait_exponential

apikey = ""
with open(sys.argv[1]) as creds:
  c = json.load(creds)
  apikey = c['api']


client = InferenceClient(model=sys.argv[4],token=apikey)
#@retry(wait=wait_exponential(multiplier=1,min=1,max=10))
def process_chat(msg):
  return client.text_generation(msg,max_new_tokens=3000, temperature = 1)

outfile = open(sys.argv[3],'w')
with open(sys.argv[2]) as promptsfil:
  count=0
  for prompttxt in promptsfil:
    prompt=json.loads(prompttxt)
    print(prompt)
    msg= prompt['instruction']+"\n"+ prompt['input']
    response = process_chat(msg)
    prompt['output']=response
    outfile.write(json.dumps(prompt))
    outfile.write("\n")
    count+=1
    if (count % 100) == 0:
      print("Sleeping: ", count)
