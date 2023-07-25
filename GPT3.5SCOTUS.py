# This is for SCOTUS dataset on GPT3.5-Turbo
from datasets import load_dataset
import openai
import os
from dotenv import load_dotenv
import time
import re
from sklearn.metrics import f1_score
import math

# Dataset loading and API
load_dotenv()
api_key = os.getenv('NEXT_PUBLIC_OPENAI_API_KEY')
openai.api_key = api_key
dataset = load_dataset('coastalcph/fairlex', 'scotus', split='train')

# Example data
text = dataset[0]['text']
true_labels_lib = []
response_labels_lib = []
liberal_Total = 0
liberal_Correct = 0
con_Total = 0
con_Correct = 0
true_labels_con = []
response_labels_con = []

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
      if(total == 1000):
        break
      
      input_text = example['text']
      input_ans = example['label']
      input_direction = example['decision_direction']
      completion = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-3.5-turbo", 
        messages = [{"role": "system", "content" : "read the script and predict the relevant issue area in these categories (0, Criminal Procedure), (1, Civil Rights), (2, First Amendment), (3, Due Process), (4, Privacy), (5, Attorneys), (6, Unions), (7, Economic Activity), (8, Judicial Power), (9, Federalism), (10, Interstate Relations), (11, Federal Taxation), (12, Miscellaneous), (13, Private Action)."},
        {"role": "user", "content" : "what would the predicted label for this" + text[:4000] + "will be? Respond with just the label number"},
        {"role": "assistant", "content" : "9"},
        {"role": "user", "content" : "what would the predicted label for this" + input_text[:4000] + "will be? Respond with just the label number"}]
      )

      if(completion['choices'][0]['message']['content'] == str(input_ans)): # Check if the predicted label is equal to actual label.
          if(input_direction == 0):
             con_Correct += 1
          elif(input_direction == 1):
             liberal_Correct += 1
          total_right += 1
      else:
        if(len(completion['choices'][0]['message']['content']) > 1):
            match = re.search(r'\d+', completion['choices'][0]['message']['content'])
            if match:
                completion['choices'][0]['message']['content'] = str(match.group())
                if completion['choices'][0]['message']['content'] == str(input_ans):
                  total_right += 1
                  if(input_direction == 0):
                    con_Correct += 1
                  elif(input_direction == 1):
                    liberal_Correct += 1

      if(input_direction == 0):
        true_labels_con.append(str(input_ans))
        response_labels_con.append(completion['choices'][0]['message']['content'])
        con_Total += 1
      elif(input_direction == 1):
        true_labels_lib.append(str(input_ans))
        response_labels_lib.append(completion['choices'][0]['message']['content'])
        liberal_Total += 1
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
print("Real answer from dataset for lib: ", true_labels_lib)
print("GPT's response for lib: ", response_labels_lib)
print("Real answer from dataset for con: ", true_labels_con)
print("GPT's response for con: ", response_labels_con)
print("For conservative this is the total and total correct ", con_Total, " ----", con_Correct)
print("For liberal this is the total and total correct ", liberal_Total, " ----", liberal_Correct)

f1_scores_lib = f1_score(true_labels_lib, response_labels_lib, average="macro")
f1_scores_con = f1_score(true_labels_con, response_labels_con, average="macro")

print("mF1 Score for liberal:", f1_scores_lib)
print("mF1 Score for conservative:", f1_scores_con)

ave_f1_scores_decision_dir = (f1_scores_con + f1_scores_lib) / 2

GD = math.sqrt(0.5 * math.pow(f1_scores_lib - ave_f1_scores_decision_dir, 2) * math.pow(f1_scores_con - ave_f1_scores_decision_dir, 2))
print("The mf1 average is:", ave_f1_scores_decision_dir)
print("The GD score is:", GD)
print("The worst mf1 score is:", min(f1_scores_con, f1_scores_lib))
