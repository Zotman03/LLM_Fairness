from datasets import load_dataset
import openai
import os
from dotenv import load_dotenv

load_dotenv()

dataset = load_dataset('coastalcph/fairlex', 'scotus', split='test')
itera = 1
text = ""
for example in dataset:
    if(itera == 2):
        break
    text = example['text']
    itera += 1

api_key = os.getenv('NEXT_PUBLIC_OPENAI_API_KEY')
openai.api_key = api_key

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", 
  messages = [{"role": "system", "content" : "read the script and predict the relevant issue area in these categories: a classification label (the relevant issue area). The issue areas are: (0, Criminal Procedure), (1, Civil Rights), (2, First Amendment), (3, Due Process), (4, Privacy), (5, Attorneys), (6, Unions), (7, Economic Activity), (8, Judicial Power), (9, Federalism), (10, Interstate Relations), (11, Federal Taxation), (12, Miscellaneous), (13, Private Action)."},
{"role": "user", "content" : "what kind of crime is robbery"},
{"role": "assistant", "content" : "it is a felony"},
{"role": "user", "content" : "what would the predicted label for this" + text[:3000] + "will be?"}]
)

print(completion['choices'][0]['message']['content'])
