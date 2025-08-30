import os
import torch
import clip
from PIL import Image
import numpy as np

print("Imports have been done successfully.")

# Load model
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

print("Model has been loaded successfully.")

# Folder with images
image_folder = "images"
image_embeddings = []
image_files = []

# Process all images
print("Processing images...")
for filename in os.listdir(image_folder):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        print(filename)
        image = preprocess(Image.open(os.path.join(image_folder, filename))).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)  # normalize
        image_embeddings.append(embedding.cpu().numpy())
        image_files.append(filename)

image_embeddings = np.vstack(image_embeddings)

print("Saving embeddings")
np.save("image_embeddings.npy", image_embeddings)
np.save("image_files.npy", np.array(image_files))

print("Done!")
