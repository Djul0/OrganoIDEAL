import os
from PIL import Image

def convert_images_to_grayscale(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            path = os.path.join(directory, filename)
            image = Image.open(path).convert('L')
            gray_image_path = os.path.join(directory, f"{filename}")
            image.save(gray_image_path)
            print(f"Converted {filename} to grayscale.")

# Replace 'your_directory_path' with the path to the directory containing your images
convert_images_to_grayscale('/Users/djulo/Documents/ETH/Project1/OrganoID-master/23-50_ModelTraining/train/Augmented/segmentations')