#from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", padding_side='left')
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    
def dialogpt():
    text = "How are you?"
    input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
    response_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(response)
    return {'response': response}

dialogpt()