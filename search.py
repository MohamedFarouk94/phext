import torch
import clip
import numpy as np


def search(query, N=5, device='cpu', image_embeddings_name='image_embeddings.npy', image_files_name='image_files.npy'):
    model, preprocess = clip.load("ViT-B/32", device=device)
    image_embeddings = np.load(image_embeddings_name)
    image_files = np.load(image_files_name)

    text_tokens = clip.tokenize([query]).to(device)

    with torch.no_grad():
        text_embedding = model.encode_text(text_tokens)

    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)

    similarities = (image_embeddings @ text_embedding.cpu().numpy().T).squeeze()

    top_idx = similarities.argsort()[::-1][:N]

    best_fit = image_files[top_idx[0]]
    return best_fit, {image_files[i]: similarities[i] for i in top_idx}
