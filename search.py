import torch
import clip
import numpy as np
from PIL import Image

# Load model
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
print("Model has been loaded successfully.")

# Load embeddings
image_embeddings = np.load("image_embeddings.npy")
image_files = np.load("image_files.npy")
print("Embeddings have been loaded successfully.")

# Encode query
text = input("Enter a text description: ")
text_tokens = clip.tokenize([text]).to(device)
print("Query has been encoded successfully.")

print("Embedding text query...")
with torch.no_grad():
    text_embedding = model.encode_text(text_tokens)
text_embedding /= text_embedding.norm(dim=-1, keepdim=True)

print("Searching...")
similarities = (image_embeddings @ text_embedding.cpu().numpy().T).squeeze()
top_idx = similarities.argsort()[::-1][:5]  # top 5 results
print("Search is complete")

print("Top matches:")
for i in top_idx:
    print(image_files[i], similarities[i])

print("Opening the best image.")
img = Image.open(f'images/{image_files[top_idx[0]]}')
img.show()
