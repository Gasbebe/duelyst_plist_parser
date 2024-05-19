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



# Example usage
gif_path = '_output/resources/units/boss_andromeda_attack.gif'
sprite_path = 'sprites/output_sprite.png'
gif_to_square_sprite(gif_path, sprite_path)
