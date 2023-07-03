from datasets import load_dataset
import openai
import os
from dotenv import load_dotenv
import time
import re

# Dataset loading and API
load_dotenv()
api_key = os.getenv('NEXT_PUBLIC_OPENAI_API_KEY')
openai.api_key = api_key
dataset = load_dataset('coastalcph/fairlex', 'scotus', split='test')

# Example data
text = dataset[0]['text']
input_ans = dataset[0]['label']

# Numbers
total = 0
total_right = 0

# Loop now
for example in dataset:
    if(total == 100):
      break
    
    input_text = example['text']
    input_ans = example['label']
    completion = openai.ChatCompletion.create(
      temperature=0,
      model="gpt-3.5-turbo", 
      messages = [{"role": "system", "content" : "read the script and predict the relevant issue area in these categories (0, Criminal Procedure), (1, Civil Rights), (2, First Amendment), (3, Due Process), (4, Privacy), (5, Attorneys), (6, Unions), (7, Economic Activity), (8, Judicial Power), (9, Federalism), (10, Interstate Relations), (11, Federal Taxation), (12, Miscellaneous), (13, Private Action)."},
      {"role": "user", "content" : "what would the predicted label for this" + text[:4000] + "will be? Respond with just the label number"},
      {"role": "assistant", "content" : "2"},
      {"role": "user", "content" : "what would the predicted label for this" + input_text[:4000] + "will be? Respond with just the label number"}]
    )

    if(completion['choices'][0]['message']['content'] == str(input_ans)): # Check if the predicted label is equal to actual label.
        total_right += 1
    else:
       if(len(completion['choices'][0]['message']['content']) > 1):
           match = re.search(r'\d+', completion['choices'][0]['message']['content'])
           if match:
              extracted_number = str(match.group())
              if extracted_number == str(input_ans):
                 total_right += 1
    total += 1
    time.sleep(6)
    print(total, " out of 100 complete")

print(total_right / total)
