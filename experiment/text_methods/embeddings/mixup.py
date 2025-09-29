import torch
import random
from transformers import RobertaTokenizer, RobertaModel

tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")

def get_embedding(code: str) -> torch.Tensor:
    inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.pooler_output.squeeze(0) 

def generate_mixup_embedding(h1, h2, y1=None, y2=None, alpha=0.4):
    lam = torch.distributions.Beta(alpha, alpha).sample().item()
    h_new = lam * h1 + (1 - lam) * h2
    if y1 is not None and y2 is not None:
        y_new = lam * y1 + (1 - lam) * y2
        return h_new, y_new
    return h_new

code_snippets = [
    "(MOV R1 5) (ADD R1 R2) (SUB R3 R1)",
    "(LOAD R4 MEM[100]) (MUL R4 R5)"
]

embeddings = [get_embedding(c) for c in code_snippets]

h_new, y_new = generate_mixup_embedding(embeddings[0], embeddings[1])

print("New embedding shape:", h_new.shape)
print("New soft label:", y_new)
