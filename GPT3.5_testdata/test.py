# This is for FSCS dataset on GPT3.5-Turbo
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
dataset = load_dataset('coastalcph/fairlex', 'fscs', split='train')

# Example data
text = dataset[0]['text']

language = {"0": ([0], [0], [], []), "1": ([0], [0], [], []), "2": ([0], [0], [], [])} #Dictionary for decision direction. Gender: (0: male, 1: female){inside tuple: Total, correct, truelable, reslabel}
area = {"0": ([0], [0], [], []), "1": ([0], [0], [], []), "2": ([0], [0], [], []), "3": ([0], [0], [], []), "4": ([0], [0], [], []), "5": ([0], [0], [], [])}
region = {"0": ([0], [0], [], []), "1": ([0], [0], [], []), "2": ([0], [0], [], []), "3": ([0], [0], [], []), "4": ([0], [0], [], []), "5": ([0], [0], [], []), "6": ([0], [0], [], []), "7": ([0], [0], [], []), "8": ([0], [0], [], []), "9": ([0], [0], [], [])}
#similar to decision direction: total, correct, true, predicted. But it is for seven province regions

# Numbers
total = 0
total_right = 0
buffer = 0
is_first = True
checking_ifpassed = 0
the_one = ""
found = 0

# Loop now
for example in dataset:
    if(is_first is True):
       is_first = False
       continue

    if(found == 100):
       break
    
    if(str(example['decision_language']) == "2"):
      found += 1
      input_text = example['text']
      input_ans = example['label']
      input_lan = example['decision_language']
      input_area = example['legal_area']
      the_one = str(input_lan)
      input_region = example['court_region']

      completion = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-3.5-turbo", 
        messages = [{"role": "system", "content" : "read the script and predict and predict if it is in these categories: (0, dismissal), (1, approved)."},
        {"role": "user", "content" : "what would the predicted label for this" + text[:4000] + "will be? Respond with just the label number"},
        {"role": "assistant", "content" : "0"},
        {"role": "user", "content" : "what would the predicted label for this" + input_text[:4000] + "will be? Respond with just the label number"}]
      )

      if(completion['choices'][0]['message']['content'] == str(input_ans)): # Check if the predicted label is equal to actual label.
          total_right += 1
          language[str(input_lan)][1][0] += 1
          area[str(input_area)][1][0] += 1
          region[str(input_region)][1][0] += 1
          #appending correct label
      
      else: #A safe layer to check if the result is correct but format issue causing it to receive wrong answer
        if(len(completion['choices'][0]['message']['content']) > 1):
            match = re.search(r'\d+', completion['choices'][0]['message']['content']) #Regular expression to make sure there is only one item here.
            if match:
                completion['choices'][0]['message']['content'] = str(match.group())
                if completion['choices'][0]['message']['content'] == str(input_ans): #check if it is the correct label
                  total_right += 1 #Total correct append
                  language[str(input_lan)][1][0] += 1
                  area[str(input_area)][1][0] += 1
                  region[str(input_region)][1][0] += 1

      #If the result is wrong then it goes here.
      language[str(input_lan)][2].append(str(input_ans))
      language[str(input_lan)][3].append(completion['choices'][0]['message']['content'])
      area[str(input_area)][2].append(str(input_ans))
      area[str(input_area)][3].append(completion['choices'][0]['message']['content'])
      region[str(input_region)][2].append(str(input_ans))
      region[str(input_region)][3].append(completion['choices'][0]['message']['content'])
      # total++
      language[str(input_lan)][0][0] += 1
      area[str(input_area)][0][0] += 1
      region[str(input_region)][0][0] += 1
      
      #Add 1 to the total number
      checking_ifpassed += 1
      total += 1
      print(total, " out of 1000 complete")
      buffer += 1
      if(buffer % 10 == 0):
        time.sleep(10)
      #if(buffer % 200 == 0):
         #time.sleep(120)

print("Using GPT3.5 turbo")

print("Real answer from dataset for Germany: ", language["0"][2])
print("GPT's response for Germany: ", language["0"][3])
print("Real answer from dataset for French: ", language["1"][2])
print("GPT's response for French: ", language["1"][3])
print("Real answer from dataset for Italian: ", language["2"][2])
print("GPT's response for Italian: ", language["2"][3])
print("For Germany this is the total and total correct ", language["0"][0][0], " ----", language["0"][1][0])
print("For French this is the total and total correct ", language["1"][0][0], " ----", language["1"][1][0])
print("For Italian this is the total and total correct ", language["2"][0][0], " ----", language["2"][1][0])

f1_scores_G = f1_score(language["0"][2], language["0"][3], average="macro")
f1_scores_F = f1_score(language["1"][2], language["1"][3], average="macro")
f1_scores_I = f1_score(language["2"][2], language["2"][3], average="macro")
print(f1_scores_I)
ave_f1_scores_language = (f1_scores_G + f1_scores_F + f1_scores_I) / 3

GD = math.sqrt(1/3 * math.pow(f1_scores_G - ave_f1_scores_language, 2) * math.pow(f1_scores_F - ave_f1_scores_language, 2) * math.pow(f1_scores_I - ave_f1_scores_language, 2))
print("The mf1 average is:", ave_f1_scores_language)
print("The GD score is:", GD)
