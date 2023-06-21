from datasets import load_dataset

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