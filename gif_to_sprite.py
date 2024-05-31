import os
from PIL import Image, ImageSequence
import math

def gif_to_square_sprite(gif_path, sprite_path):
    # Open the GIF file
    gif = Image.open(gif_path)
    
    # Get all frames of the GIF
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    frame_count = len(frames)
    
    # Determine the number of columns and rows for the square sprite
    cols = math.ceil(math.sqrt(frame_count))
    rows = math.ceil(frame_count / cols)
    
    # Size of each frame
    frame_width, frame_height = frames[0].size
    
    # Size of the final sprite image
    sprite_width = cols * frame_width
    sprite_height = rows * frame_height
    
    # Create a new blank image for the sprite
    sprite_image = Image.new('RGBA', (sprite_width, sprite_height))
    
    # Paste all frames into the sprite image
    for index, frame in enumerate(frames):
        col = index % cols
        row = index // cols
        x = col * frame_width
        y = row * frame_height
        sprite_image.paste(frame, (x, y))
    
    # Save the sprite image
    sprite_image.save(sprite_path)

def process_gif_folder(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith('.gif'):
                gif_path = os.path.join(root, filename)
                # Preserve the directory structure in the output folder
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                sprite_filename = os.path.splitext(filename)[0] + '.png'
                sprite_path = os.path.join(output_dir, sprite_filename)
                gif_to_square_sprite(gif_path, sprite_path)
                print(f"Converted {gif_path} to {sprite_path}")

# Example usage
input_folder = 'path/to/your/input/folder'
output_folder = 'path/to/your/output/folder'
process_gif_folder(input_folder, output_folder)
