from datasets import load_dataset
import openai
import os
from dotenv import load_dotenv
import time
import re
    
try_string = "dd21.d44dddd"
match = re.search(r'\d+', try_string)
if match:
    extracted_number = str(match.group())
print(extracted_number)
print(type(extracted_number))
