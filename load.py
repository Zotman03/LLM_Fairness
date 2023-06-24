from datasets import load_dataset
import openai
#build GPT response API

# Load IMDb dataset and download specific rows
dataset = load_dataset('coastalcph/fairlex', 'scotus', split='test')
itera = 1
for example in dataset:
    if(itera == 2):
        break
    text = example['text']
    label = example['label']
    itera += 1
    print(text, label)

#make env file
openai.api_key = 'YOUR_API_KEY'

def checkGPTresponse(question):
    prompt = "Question: " + question + "\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Retrieve and return the generated answer
    answer = response.choices[0].text.strip().split(":")[1].strip()
    return answer

# Send a question to ChatGPT and print the answer
question = "What is the capital of France?"
answer = checkGPTresponse(question)
print("Answer:", answer)
