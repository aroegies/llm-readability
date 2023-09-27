from vertexai.preview.language_models import ChatModel, InputOutputTextPair
import vertexai, sys, json
from tenacity import retry,wait_exponential


vertexai.init(project="marsinternet", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison@001")
parameters = {
    "temperature": 1.0,
}

@retry(wait=wait_exponential(multiplier=1,min=4,max=30))
def process_chat(msg):
    chat = chat_model.start_chat()
    return chat.send_message(msg, **parameters).text


outfile = open(sys.argv[2],'w')
with open(sys.argv[1]) as promptsfil:
  count=0
  for prompttxt in promptsfil:
    prompt=json.loads(prompttxt)
    msg= prompt['instruction']+"\n"+ prompt['input']
    prompt['output']=process_chat(msg)
    outfile.write(json.dumps(prompt))
    outfile.write("\n")
    count+=1
    if (count % 100) == 0:
      print("Sleeping: ", count)
