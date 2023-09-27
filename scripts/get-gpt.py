import openai, json, sys, time
from tenacity import retry,wait_exponential

@retry(wait=wait_exponential(multiplier=1,min=1,max=30))
def query_gpt(msgs):
    completion = openai.ChatCompletion.create(model="gpt-4", messages = msgs)
    return completion.choices[0].message.content


with open(sys.argv[1]) as creds:
  c = json.load(creds)
  openai.api_key = c['api']

outfile = open(sys.argv[3],'w')
with open(sys.argv[2]) as promptsfil:
  count=0
  for prompttxt in promptsfil:
    prompt=json.loads(prompttxt)
    prompt['output']= query_gpt([{"role":"user","content":prompt['instruction']},{"role":"user","content":prompt['input']}])
    outfile.write(json.dumps(prompt))
    outfile.write("\n")
    count+=1
    if (count % 100) == 0:
      print("Sleeping: ", count)

outfile.close()
