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
area = {"0": ([0], [0], [], []), "1": ([0], [0], [], []), "2": ([0], [0], [], []), "3": ([0], [0], [], []), "4": ([0], [0], [], [])}
region = {"0": ([0], [0], [], []), "1": ([0], [0], [], []), "2": ([0], [0], [], []), "3": ([0], [0], [], []), "4": ([0], [0], [], []), "5": ([0], [0], [], []), "6": ([0], [0], [], []), "7": ([0], [0], [], []), "8": ([0], [0], [], [])}
#similar to decision direction: total, correct, true, predicted. But it is for seven province regions

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
      if(total == 1000):
        break
      
      input_text = example['text']
      input_ans = example['label']
      input_lan = example['decision_language']
      input_area = example['legal_area']
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

ave_f1_scores_language = (f1_scores_G + f1_scores_F + f1_scores_I) / 3

GD = math.sqrt(1/3 * math.pow(f1_scores_G - ave_f1_scores_language, 2) * math.pow(f1_scores_F - ave_f1_scores_language, 2) * math.pow(f1_scores_I - ave_f1_scores_language, 2))
print("The mf1 average is:", ave_f1_scores_language)
print("The GD score is:", GD)
print("The worst mf1 score is:", min(f1_scores_G, f1_scores_F, f1_scores_I))


print("Real answer from dataset for public: ", area["0"][2])
print("GPT's response for Public: ", area["0"][3])
print("Real answer from dataset for penal: ", area["1"][2])
print("GPT's response for penal: ", area["1"][3])
print("Real answer from dataset for social: ", area["2"][2])
print("GPT's response for social: ", area["2"][3])
print("Real answer from dataset for civil: ", area["3"][2])
print("GPT's response for civil: ", area["3"][3])
print("Real answer from dataset for insurance: ", area["4"][2])
print("GPT's response for insurance: ", area["4"][3])
print("For Public this is the total and total correct ", area["0"][0][0], " ----", area["0"][1][0])
print("For Penal this is the total and total correct ", area["1"][0][0], " ----", area["1"][1][0])
print("For Social this is the total and total correct ", area["2"][0][0], " ----", area["2"][1][0])
print("For Civil this is the total and total correct ", area["3"][0][0], " ----", area["3"][1][0])
print("For Insurance this is the total and total correct ", area["4"][0][0], " ----", area["4"][1][0])

f1_scores_pub = f1_score(area["0"][2], area["0"][3], average="macro")
f1_scores_p = f1_score(area["1"][2], area["1"][3], average="macro")
f1_scores_s = f1_score(area["2"][2], area["2"][3], average="macro")
f1_scores_c = f1_score(area["3"][2], area["3"][3], average="macro")
f1_scores_i = f1_score(area["4"][2], area["4"][3], average="macro")

ave_f1_scores_area = (f1_scores_pub + f1_scores_p + f1_scores_s + f1_scores_c + f1_scores_i) / 5

GD = math.sqrt(0.2 * math.pow(f1_scores_pub - ave_f1_scores_area, 2) * math.pow(f1_scores_p - ave_f1_scores_area, 2) * math.pow(f1_scores_s - ave_f1_scores_area, 2) * math.pow(f1_scores_c - ave_f1_scores_area, 2) * math.pow(f1_scores_i - ave_f1_scores_area, 2))
print("The mf1 average is:", ave_f1_scores_area)
print("The GD score is:", GD)
print("The worst mf1 score is:", min(f1_scores_pub, f1_scores_p, f1_scores_s, f1_scores_c, f1_scores_i))


f1_scores_BJ = f1_score(region["0"][2], region["0"][3], average="macro")
f1_scores_LN = f1_score(region["1"][2], region["1"][3], average="macro")
f1_scores_HN = f1_score(region["2"][2], region["2"][3], average="macro")
f1_scores_GD = f1_score(region["3"][2], region["3"][3], average="macro")
f1_scores_SC = f1_score(region["4"][2], region["4"][3], average="macro")
f1_scores_GX = f1_score(region["5"][2], region["5"][3], average="macro")
f1_scores_ZJ = f1_score(region["6"][2], region["6"][3], average="macro")
f1_scores_F1 = f1_score(region["7"][2], region["7"][3], average="macro")
f1_scores_F2 = f1_score(region["8"][2], region["8"][3], average="macro")
f1_scores_F3 = f1_score(region["9"][2], region["9"][3], average="macro")


ave_f1_scores_reg = (f1_scores_BJ + f1_scores_LN + f1_scores_HN + f1_scores_GD + f1_scores_SC + f1_scores_GX + f1_scores_ZJ + f1_scores_F1 + f1_scores_F2 + f1_scores_F3) / 10

GD_res = math.sqrt(1/10 * math.pow(f1_scores_BJ - ave_f1_scores_reg, 2) * math.pow(f1_scores_LN - ave_f1_scores_reg, 2) * math.pow(f1_scores_HN - ave_f1_scores_reg, 2) * math.pow(f1_scores_GD - ave_f1_scores_reg, 2) * math.pow(f1_scores_SC - ave_f1_scores_reg, 2) * math.pow(f1_scores_GX - ave_f1_scores_reg, 2) * math.pow(f1_scores_ZJ - ave_f1_scores_reg, 2) * math.pow(f1_scores_F1 - ave_f1_scores_reg, 2) * math.pow(f1_scores_F2 - ave_f1_scores_reg, 2) * math.pow(f1_scores_F3 - ave_f1_scores_reg, 2))
print("The mf1 average is:", ave_f1_scores_reg)
print("The GD score is:", GD_res)
print("The worst mf1 score is:", min(f1_scores_BJ, f1_scores_LN, f1_scores_HN, f1_scores_GD, f1_scores_SC, f1_scores_GX, f1_scores_ZJ, f1_scores_F1, f1_scores_F2, f1_scores_F3))
