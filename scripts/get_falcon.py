import sys, json
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model_id = "tiiuae/falcon-40b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    load_in_8bit=True,
    device_map="auto",
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    trust_remote_code=True,
    device_map="auto",
)


llm  = Llama(model_path=sys.argv[4], n_gqa=8, n_ctx=2048)
outfile = open(sys.argv[2],'w')
with open(sys.argv[1]) as promptsfil:
  count=0
  for prompttxt in promptsfil:
    prompt=json.loads(prompttxt)
    msg= prompt['instruction']+"\n"+ prompt['input']
    
    sequences = pipeline(
      msg,
      max_length=-1,
      num_return_sequences=1,
      eos_token_id=tokenizer.eos_token_id,
    )
    prompt['output']=sequences[0]['generated_text']
    outfile.write(json.dumps(prompt))
    outfile.write("\n")
    count+=1
    if (count % 100) == 0:
      print("Sleeping: ", count)
