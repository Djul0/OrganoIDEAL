#together
import json
import numpy as np
from PIL import Image, ImageDraw

#change here the final location
path_to_output = "/Users/djulo/Documents/ETH/Project1/OrganoID-master/23-50_ModelTraining/Augmented/validation/segmentations"

# change here the location of json file
with open('/Users/djulo/Documents/ETH/Project1/OrganoID-master/23-50_ModelTraining/valid/_annotations.coco.json') as f:
    coco_data = json.load(f)


from PIL import Image, ImageDraw
import numpy as np
import os

#  change here the location of non combined segmented images
output_dir = '/Users/djulo/Documents/ETH/Project1/OrganoID-master/23-50_ModelTraining/Augmented/intermed'
os.makedirs(output_dir, exist_ok=True)

# Function to convert COCO polygon segmentation to a sequence of (x, y) tuples
def coco_poly_to_points(poly):
    return [(poly[i], poly[i + 1]) for i in range(0, len(poly), 2)]

# Function to create mask from polygons
def create_mask_from_polygons(image_shape, polygons):
    mask_img = Image.new('L', (image_shape[1], image_shape[0]), 0)
    mask_draw = ImageDraw.Draw(mask_img)
    for polygon in polygons:
        points = coco_poly_to_points(polygon)
        mask_draw.polygon(points, outline=1, fill=1)
    return np.array(mask_img)

# A dictionary to map image ids to their file names and dimensions
image_info = {image['id']: {'file_name': image['file_name'], 'height': image['height'], 'width': image['width']} for image in coco_data['images']}


# Iterate over annotations and create masks
for annotation in coco_data['annotations']:
    # Get the corresponding image info
    img_info = image_info[annotation['image_id']]
    image_height, image_width = img_info['height'], img_info['width']
    
    # Only process if segmentation information is available and is a list (polygons)
    if 'segmentation' in annotation:
        # Get the segmentation points for the current annotation
        segmentation = annotation['segmentation']
        # Create the binary mask
        binary_mask = create_mask_from_polygons((image_height, image_width), segmentation)
        # Convert the numpy array to a PIL image
        #binary_mask_img = Image.fromarray((binary_mask * 255).astype(np.uint8))
        binary_mask_img = Image.fromarray(binary_mask.astype(np.bool_))
        # Create a mask file name
        mask_file_name = f"{os.path.splitext(img_info['file_name'])[0]}_{annotation['id']}.png"  
        # Save the binary mask as PNG
        binary_mask_img.save(os.path.join(output_dir, mask_file_name))
    else :
        print(annotation)
        binary_mask_img = Image.new('L', (512, 512), 0)
        # Create a mask file name
        mask_file_name = f"{os.path.splitext(img_info['file_name'])[0]}_{annotation['id']}.png"  
        # Save the binary mask as PNG
        binary_mask_img.save(os.path.join(output_dir, mask_file_name))

# Return the path to the directory containing the masks
output_dir


########-----------------------------------------------


import os
import numpy as np
from PIL import Image
from collections import defaultdict

def fuse_images(image_files):
    # Initialize an array with zeros with the shape of the first image
    base_img = Image.open(image_files[0])
    fused_array = np.zeros(base_img.size, dtype=np.uint8)

    # Fuse the images using a logical OR operation
    for file in image_files:
        img = Image.open(file)
        img_array = np.array(img)
        fused_array = np.logical_or(fused_array, img_array)

    # Convert the fused array back to an image
    return Image.fromarray(np.uint8(fused_array) * 255)  # Convert boolean to uint8

def main(input_directory, output_directory):
    # Create a dictionary to hold lists of image paths, grouped by their prefix
    image_groups = defaultdict(list)

    # Scan the input directory for PNG files and group them
    for filename in os.listdir(input_directory):
        if filename.endswith('.png'):
            # Extract the prefix which is the part of the filename before "_jpg_"
            prefix = '_'.join(filename.split('_')[:-1])
            image_groups[prefix].append(os.path.join(input_directory, filename))

    # Process each group of images
    for prefix, image_files in image_groups.items():
        fused_image = fuse_images(image_files)
        output_filename = prefix + '_fused.png'
        output_path = os.path.join(output_directory, output_filename)
        fused_image.save(output_path)
        print(f'Saved fused image: {output_path}')

# Usage
# Replace 'path_to_input_directory' with the path to the directory containing your images.
# Replace 'path_to_output_directory' with the path where you want to save the fused images.
main(output_dir, path_to_output)
