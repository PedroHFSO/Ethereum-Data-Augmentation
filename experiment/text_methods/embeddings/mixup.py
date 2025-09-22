from transformers import RobertaTokenizer, RobertaModel
import torch

tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")


# Tokenize
inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True)

# Get embeddings
with torch.no_grad():
    outputs = model(**inputs)
