from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset

# Initialize the tokenizer and model globally
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def tokenize_and_format_function(examples):
    # Tokenize both questions and labels with proper padding and truncation
    tokenized_inputs = tokenizer(examples['questions'], truncation=True, padding='max_length', max_length=128)
    tokenized_labels = tokenizer(examples['labels'], truncation=True, padding='max_length', max_length=128)
    
    # Make sure to return the same keys as expected by the model, generally input_ids for input
    return {'input_ids': tokenized_inputs['input_ids'], 'labels': tokenized_labels['input_ids']}

def train(data_path):
    # Load the pretrained model
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

    # Load and prepare the dataset
    dataset = load_dataset('csv', data_files=data_path)
    tokenized_datasets = dataset.map(tokenize_and_format_function, batched=True, remove_columns=dataset['train'].column_names)

    # Define a data collator that will dynamically pad the batches during training
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer, padding=True)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='./logs',
        logging_steps=500,
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    # Start training
    trainer.train()

train('dataset.csv')

