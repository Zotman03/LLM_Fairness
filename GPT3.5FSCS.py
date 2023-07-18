#This is for FSCS dataset on GPT3.5-Turbo
from datasets import load_dataset
import openai
import os
from dotenv import load_dotenv
import time
import re
from sklearn.metrics import f1_score

# Dataset loading and API
load_dotenv()
api_key = os.getenv('NEXT_PUBLIC_OPENAI_API_KEY')
openai.api_key = api_key
dataset = load_dataset('coastalcph/fairlex', 'fscs', split='test')

# Example data
text = dataset[0]['text']
true_labels = []
response_labels = []

# Numbers
total = 0
total_right = 0
buffer = 0
is_first = True
# Loop now
for example in dataset:
    if(is_first is True):
       is_first = False
       continue
    else:
      if(total == 1):
        break
      
      input_text = example['text']
      input_ans = example['legal_area']
      completion = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-3.5-turbo", 
        messages = [{"role": "system", "content" : "read the script and predict the relevant issue area in these categories (0, public), (1, penal law), (2, social law), (3, civil law), (4, insurance law)."},
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
                completion['choices'][0]['message']['content'] = str(match.group())
                if completion['choices'][0]['message']['content'] == str(input_ans):
                  total_right += 1
      true_labels.append(str(input_ans))
      response_labels.append(completion['choices'][0]['message']['content'])
      total += 1
      print(total, " out of 100 complete")
      buffer += 1
      if(buffer == 10):
        time.sleep(10)
        buffer = 0   

print("Using GPT3.5 turbo")
print(total_right)
print(total)
print(total_right / total * 100)
print("Real answer from dataset: ", true_labels)
print("GPT's response: ", response_labels)
f1_scores = f1_score(true_labels, response_labels, average=None)

mF1_score = sum(f1_scores) / len(f1_scores)

print("F1 Scores:", f1_scores)
print("mF1 Score:", mF1_score)
