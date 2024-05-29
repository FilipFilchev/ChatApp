from transformers import AutoModelForCausalLM, AutoTokenizer # Trainer, TrainingArguments
from datasets import load_dataset
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", padding_side='left')
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

def tokenize_function(examples, tokenizer):
    return tokenizer(examples["questions"], padding="max_length", truncation=True, max_length=128)

dataset = load_dataset('csv', data_files='dataset.csv')
print("dataSet",dataset)
tokenized_datasets = dataset.map(lambda examples: tokenize_function(examples, tokenizer), batched=True)
print("tok", tokenized_datasets)