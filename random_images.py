import os
import requests


def download_random_images(N=10, save_dir="test_images"):
    # Using Picsum for truly random images
    base_url = "https://picsum.photos/600/400"  # width=600, height=400

    os.makedirs(save_dir, exist_ok=True)

    for i in range(N):
        try:
            r = requests.get(base_url, timeout=10)
            if r.status_code == 200:
                with open(f"{save_dir}/img_{i}.jpg", "wb") as f:
                    f.write(r.content)
                print(f"Downloaded: img_{i}.jpg")
            else:
                print(f"Failed (status {r.status_code})")
        except Exception as e:
            print(f"Error: {e}")


download_random_images(50)
