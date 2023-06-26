from datasets import load_dataset
import openai
#build GPT response API

# dataset = load_dataset('coastalcph/fairlex', 'scotus', split='test')
# itera = 1
# for example in dataset:
#     if(itera == 2):
#         break
#     text = example['text']
#     label = example['label']
#     itera += 1
#     print(text, label)

# #make env file
# openai.api_key = 'YOUR_API_KEY'

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", 
  messages = [{"role": "system", "content" : "read the script and answer in three bullet points"},
{"role": "user", "content" : "what kind of crime is robbery"},
{"role": "assistant", "content" : "it is a felony"},
{"role": "user", "content" : "what kind of crime is burning a building?"}]
)
print(completion)
