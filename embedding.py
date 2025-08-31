import os
import torch
import clip
from PIL import Image
import numpy as np
from tqdm import tqdm


def create_embeddings(image_folder='images', device='cpu', image_embeddings_name='image_embeddings.npy', image_files_name='image_files.npy'):
    model, preprocess = clip.load("ViT-B/32", device=device)
    image_embeddings = []
    image_files = []
    for filename in tqdm(os.listdir(image_folder)):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            image = preprocess(Image.open(os.path.join(image_folder, filename))).unsqueeze(0).to(device)
            with torch.no_grad():
                embedding = model.encode_image(image)
            embedding /= embedding.norm(dim=-1, keepdim=True)  # normalize
            image_embeddings.append(embedding.cpu().numpy())
            image_files.append(filename)

    image_embeddings = np.vstack(image_embeddings)
    np.save(image_embeddings_name, image_embeddings)
    np.save(image_files_name, np.array(image_files))
