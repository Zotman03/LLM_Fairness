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

decision_dir = {"0": ([0], [0], [], []), "1": ([0], [0], [], [])} #Dictionary for decision direction. Tuple: (0: conservative, 1: liberal){inside tuple: Total, correct, truelable, reslabel}

# Numbers
total = 0
total_right = 0
buffer = 0
is_first = True
# Loop now
for example in dataset:
    if(is_first is True):
       is_first = False
       continue # Check for the first time, and will never be checked again
    else:
      if(total == 10):
        break
      
      input_text = example['text']
      input_ans = example['label']
      input_direction = example['decision_direction']
      #Get the criteria such as decision_direction.

      completion = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-3.5-turbo", 
        messages = [{"role": "system", "content" : "read the script and predict the relevant issue area in these categories (0, Criminal Procedure), (1, Civil Rights), (2, First Amendment), (3, Due Process), (4, Privacy), (5, Attorneys), (6, Unions), (7, Economic Activity), (8, Judicial Power), (9, Federalism), (10, Interstate Relations), (11, Federal Taxation), (12, Miscellaneous), (13, Private Action)."},
        {"role": "user", "content" : "what would the predicted label for this" + text[:4000] + "will be? Respond with just the label number"},
        {"role": "assistant", "content" : "9"},
        {"role": "user", "content" : "what would the predicted label for this" + input_text[:4000] + "will be? Respond with just the label number"}]
      )

      if(completion['choices'][0]['message']['content'] == str(input_ans)): # Check if the predicted label is equal to actual label.
          total_right += 1
          decision_dir[str(input_direction)][1][0] += 1
      
      else: #A safe layer to check if the result is correct but format issue causing it to receive wrong answer
        if(len(completion['choices'][0]['message']['content']) > 1):
            match = re.search(r'\d+', completion['choices'][0]['message']['content']) #Regular expression to make sure there is only one item here.
            if match:
                completion['choices'][0]['message']['content'] = str(match.group())
                if completion['choices'][0]['message']['content'] == str(input_ans): #check if it is the correct label
                  total_right += 1 #Total correct append
                  decision_dir[str(input_direction)][1][0] += 1

      #If the result is wrong then it goes here.
      decision_dir[str(input_direction)][2].append(str(input_ans))
      decision_dir[str(input_direction)][3].append(completion['choices'][0]['message']['content'])
      decision_dir[str(input_direction)][0][0] += 1
      
      #Add 1 to the total number
      total += 1
      print(total, " out of 1000 complete")
      buffer += 1
      if(buffer % 10 == 0):
        time.sleep(10)
      if(buffer % 200 == 0):
         time.sleep(120)

print("Using GPT3.5 turbo")
print(total_right)
print(total)
print(total_right / total * 100)


print("Real answer from dataset for lib: ", decision_dir["1"][2])
print("GPT's response for lib: ", decision_dir["1"][3])
print("Real answer from dataset for con: ", decision_dir["0"][2])
print("GPT's response for con: ", decision_dir["1"][3])
print("For conservative this is the total and total correct ", decision_dir["0"][0][0], " ----", decision_dir["0"][1][0])
print("For liberal this is the total and total correct ", decision_dir["1"][0][0], " ----", decision_dir["1"][1][0])

f1_scores_lib = f1_score(decision_dir["1"][2], decision_dir["1"][3], average="macro")
f1_scores_con = f1_score(decision_dir["0"][2], decision_dir["0"][3], average="macro")

print("mF1 Score for liberal:", f1_scores_lib)
print("mF1 Score for conservative:", f1_scores_con)

ave_f1_scores_decision_dir = (f1_scores_con + f1_scores_lib) / 2

GD = math.sqrt(0.5 * math.pow(f1_scores_lib - ave_f1_scores_decision_dir, 2) * math.pow(f1_scores_con - ave_f1_scores_decision_dir, 2))
print("The mf1 average is:", ave_f1_scores_decision_dir)
print("The GD score is:", GD)
print("The worst mf1 score is:", min(f1_scores_con, f1_scores_lib))
