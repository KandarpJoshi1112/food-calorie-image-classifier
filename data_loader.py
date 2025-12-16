import os
import requests
from PIL import Image
from io import BytesIO

# Your Unsplash Access Key (replace with your own key)
access_key = 'YOUR_UNSPLASH_ACCESS_KEY'  # Replace with your actual Unsplash Access Key

# Define categories and corresponding folders
categories = {
    'cake': ['data/raw/train/cake', 'data/raw/val/cake'],
    'ice_cream': ['data/raw/train/ice_cream', 'data/raw/val/ice_cream'],
    'pizza': ['data/raw/train/pizza', 'data/raw/val/pizza'],
    'burger': ['data/raw/train/burger', 'data/raw/val/burger'],
    'pasta': ['data/raw/train/pasta', 'data/raw/val/pasta'],
    'sandwich': ['data/raw/train/sandwich', 'data/raw/val/sandwich'],
    'french_fries': ['data/raw/train/french_fries', 'data/raw/val/french_fries'],
    'salad': ['data/raw/train/salad', 'data/raw/val/salad'],
    'paneer': ['data/raw/train/paneer', 'data/raw/val/paneer']
}

# Helper function to download image and save to folder
def download_image(image_url, folder, image_name):
    try:
        # Send HTTP request to the image URL
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))  # Open image with Pillow to check if it's valid
        img.save(os.path.join(folder, image_name))  # Save image to the folder
        print(f"Downloaded {image_name} to {folder}")
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")

# Function to fetch images for each category with pagination
def fetch_images_for_category(category, folder, num_images=50):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Total images fetched so far
    images_fetched = 0
    page = 1  # Start from page 1

    while images_fetched < num_images:
        # Unsplash API URL with pagination support
        url = f'https://api.unsplash.com/search/photos?query={category}&client_id={access_key}&page={page}&per_page=30'
        
        # Add headers for User-Agent to simulate a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Send request to Unsplash API
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            images = data['results']
            print(f"Fetched {len(images)} images from page {page}")

            # Loop through images and download them
            for img in images:
                if images_fetched >= num_images:
                    break
                image_url = img['urls']['regular']  # Regular image URL
                image_name = f"{category}_{images_fetched + 1}.jpg"
                download_image(image_url, folder, image_name)
                images_fetched += 1

            # Move to the next page
            page += 1

        else:
            print(f"Failed to fetch images for {category}: {response.status_code}")
            break

# Function to download more images for each category and split them into train and val sets
def download_more_images_for_all_categories():
    for category, folders in categories.items():
        print(f"\nDownloading images for {category}...")

        # Download images for training set (50 images)
        fetch_images_for_category(category, folders[0], num_images=50)

        # Download images for validation set (20 images)
        fetch_images_for_category(category, folders[1], num_images=20)

# Run the download process for all categories
if __name__ == "__main__":
    download_more_images_for_all_categories()
