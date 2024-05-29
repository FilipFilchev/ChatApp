#FINETUNING DialoGPT transformer

from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch
#init
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

def tokenize_function(examples, tokenizer):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

def train(data_path):
    #tokenize data
    dataset = load_dataset('csv', data_files=data_path)
    #call tokenizer
    tokenized_datasets = dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    print(tokenized_datasets)
    
    training_args = TrainingArguments(
        output_dir='./results',
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,  # Adjust batch size according to GPU/CPU memory
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='./logs',  # Directory for storing logs
        logging_steps=500,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
        tokenizer=tokenizer,
    )

    # Start training
    trainer.train()

# MAIN 
train('dataset.csv')
