import requests
from PIL import Image
from io import BytesIO
import json
import os
from tqdm import tqdm
# Credit to Hassan-sd 

# Replace with your API key
api_key = "xxxxxxxxx"

# API endpoint
url = "https://civitai.com/api/v1/images"
headers = {"Authorization": f"Bearer {api_key}"}

# Make API request
response = requests.get(url, headers=headers)
response_data = response.json()

# Filter images with stats.heartCount greater than 10 and a non-empty meta.prompt
filtered_images = [image for image in response_data['items'] if image['stats']['heartCount'] > 10 and image['meta'] is not None and 'prompt' in image['meta'] and image['meta']['prompt']]

# Download and save filtered images and metadata
total_saved = 0
for image in tqdm(filtered_images, desc="Saving images and metadata", unit="image"):
    image_id = image['id']
    image_url = image['url']
    image_meta = image['meta']

    # Download image
    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))

    # Convert image to RGB if necessary
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Save image
    img_filename = f"{image_id}.jpg"
    img.save(img_filename)

    # Save meta.prompt as a text file
    meta_prompt = image_meta['prompt']
    meta_filename = f"{image_id}.txt"
    with open(meta_filename, "w") as meta_file:
        meta_file.write(meta_prompt)

    total_saved += 1

print(f"Downloaded and saved {total_saved}/{len(filtered_images)} images and metadata files.")
