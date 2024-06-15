import plistlib
import os
import ast
from PIL import Image

def parse_frame(frame_str):
    frame_str = frame_str.replace('{', '(').replace('}', ')')
    return eval(frame_str)

def create_gif_from_frames(frames, png_path, output_gif_path):
    # PNG 이미지 열기
    png_image = Image.open(png_path)

    # 프레임 추출 및 GIF 생성
    gif_frames = []
    for frame_name in frames:
        try:
            frame_info = frames[frame_name]
            # frame 정보 파싱
            frame_box = parse_frame(frame_info['frame'])
            frame_region = png_image.crop((
                frame_box[0][0],
                frame_box[0][1],
                frame_box[0][0] + frame_box[1][0],
                frame_box[0][1] + frame_box[1][1]
            ))
            # 투명 배경 설정
            frame_region = frame_region.convert("RGBA")
            background = Image.new("RGBA", frame_region.size, (255, 255, 255, 0))
            background.paste(frame_region, (0, 0), frame_region)
            gif_frames.append(background)
        except Exception as e:
            print(f"\033[91mError processing frame {frame_name}: {e}\033[0m")

    if gif_frames:
        # GIF 저장
        gif_frames[0].save(output_gif_path, save_all=True, append_images=gif_frames[1:], duration=100, loop=0, transparency=0, disposal=2)
        print(f"GIF 파일이 {output_gif_path}에 저장되었습니다.")
    else:
        print(f"No valid frames found for {output_gif_path}")

def process_plist(plist_path, output_dir):
    try:
        with open(plist_path, 'rb') as fp:
            plist_data = plistlib.load(fp)
        
        if 'frames' in plist_data:
            frames = plist_data['frames']
            animations = {}
            for frame_name, frame_info in frames.items():
                animation_name = '_'.join(frame_name.split('_')[:-1])
                if animation_name not in animations:
                    animations[animation_name] = {}
                animations[animation_name][frame_name] = frame_info
            
            png_file = plist_path.replace('.plist', '.png')

            for animation_name, animation_frames in animations.items():
                output_gif_path = os.path.join(output_dir, f"{animation_name}.gif")
                create_gif_from_frames(animation_frames, png_file, output_gif_path)
    except Exception as e:
        print(f"\033[91mError processing plist file {plist_path}: {e}\033[0m")

def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.plist'):
                plist_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_gif_dir = os.path.join(output_dir, relative_path)
                os.makedirs(output_gif_dir, exist_ok=True)
                process_plist(plist_path, output_gif_dir)

# Example usage
input_directory = './app/resources'
output_directory = './out'

process_directory(input_directory, output_directory)
