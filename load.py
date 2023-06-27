from datasets import load_dataset
import openai
import requests
#build GPT response API

dataset = load_dataset('coastalcph/fairlex', 'scotus', split='test')
itera = 1
text = ""
for example in dataset:
    if(itera == 2):
        break
    text = example['text']
    itera += 1

# #make env file

# openai.api_key = 'YOUR_API_KEY'

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", 
  messages = [{"role": "system", "content" : "read the script and predict the relevant issue area in these categories: a classification label (the relevant issue area). The issue areas are: (1, Criminal Procedure), (2, Civil Rights), (3, First Amendment), (4, Due Process), (5, Privacy), (6, Attorneys), (7, Unions), (8, Economic Activity), (9, Judicial Power), (10, Federalism), (11, Interstate Relations), (12, Federal Taxation), (13, Miscellaneous), (14, Private Action)."},
{"role": "user", "content" : "what kind of crime is robbery"},
{"role": "assistant", "content" : "it is a felony"},
{"role": "user", "content" : "what would the predicted label for this" + text[:3000] + "will be?"}]
)

print(completion['choices'][0]['message']['content'])
