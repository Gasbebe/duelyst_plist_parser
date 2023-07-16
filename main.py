from d_parser import *
import os
import glob
from PIL import Image

def print_info(path):
    
    parse = d_parse()
    parse.load(os.path.join(os.getcwd(), path))

    directory_path = os.path.dirname(path)
    out_put_dir_path = "output" + os.sep + directory_path
    os.makedirs(out_put_dir_path, exist_ok=True)

    image_path = path.replace("plist", "png")
    if len(parse.get_frames()) > 0 :
        image = Image.open(os.path.join(os.getcwd(), image_path))

    # print(parse.get_frames())
    # print(parse.get_metadata())
    parse.get_file_name()
    cropped_image_list = []
    frame_type = ""
    for k, frame_info in parse.get_frames().items():
        # frame_check_type = re.sub(r"\d", "", k)
        frame_check_type = re.sub(r"_([0-9]+)", "", k)

        #first
        if frame_type == "":
            frame_type = frame_check_type

        #파일이 다르면
        if frame_type != frame_check_type:
            # 잘린 이미지가 여러개 있으면 저장
            if len(cropped_image_list) > 1 :
                # cropped_image_list[0].save("output/" + parse.get_file_name().replace("png", "gif"), save_all=True, append_images=cropped_image_list[1:], optimize=False, duration=10, loop=1, transparency=0, disposal = 2)
                cropped_image_list[0].save(out_put_dir_path  + os.sep + frame_type + ".gif", save_all=True, append_images=cropped_image_list[1:], optimize=False, duration=10, loop=1, transparency=0, disposal = 2)
                cropped_image_list.clear()

            # if len(cropped_image_list) > 1 :
            #     cropped_image_list[0].save("output/" + frame_check_type + ".gif", save_all=True, append_images=cropped_image_list[1:], optimize=False, duration=10, loop=1, transparency=0, disposal = 2)
            frame_type = frame_check_type


        #[^a-zA-Z0-9] 
        frame_dict = frame_info["frame"]

        #이미지 자르기
        c_pos = parse.get_position(frame_dict)

        x1 = int(c_pos[0].x)
        y1 = int(c_pos[0].y)

        x2 = int(c_pos[0].x) + int(c_pos[1].x)
        y2 = int(c_pos[0].y) + int(c_pos[1].y)
        # end 

        one_frame = image.crop((x1,y1, x2,y2))
        cropped_image_list.append(one_frame)
        
    #마지막 이미지 
    if len(cropped_image_list) > 1 :
        cropped_image_list[0].save(out_put_dir_path  + os.sep + frame_type + ".gif", save_all=True, append_images=cropped_image_list[1:], optimize=False, duration=10, loop=1, transparency=0, disposal = 2)
        cropped_image_list.clear()

def main():
    print("Hello, World!")
    file_list = glob.glob("**/*.plist", recursive=True)
    for pf in file_list:
        print_info(pf)

if __name__ == "__main__":
    main()