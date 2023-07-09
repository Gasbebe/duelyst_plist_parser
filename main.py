from d_parser import *
import os
import glob
from PIL import Image

def print_info(path):
    parse = d_parse()
    parse.load(os.path.join(os.getcwd(), path))
    # print(parse.get_frames())
    # print(parse.get_metadata())
    parse.get_file_name()
    cropped_image_list = []
    for frame_info in parse.get_frames().values():
        test = frame_info["frame"]

        c_pos = parse.get_position(test)
        image = Image.open(path.replace("plist", "png"))

        x1 = int(c_pos[0].x)
        y1 = int(c_pos[0].y)

        x2 = int(c_pos[0].x) + int(c_pos[1].x)
        y2 = int(c_pos[0].y) + int(c_pos[1].y)
        # end 

        test2 = image.crop((x1,y1, x2,y2))
        cropped_image_list.append(test2)
    if len(cropped_image_list) > 1 :
        cropped_image_list[0].save("output/" + parse.get_file_name().replace("png", "gif"), save_all=True, append_images=cropped_image_list[1:], optimize=False, duration=10, loop=1, transparency=0, disposal = 2)
    else:
        pass
    pass

def main():
    # ss = re.findall(r"\{[\d]+,\s*[\d]+\}", "gleeee")
    parse = d_parse()
    parse.load(os.path.join(os.getcwd(), "resources/fx/f3_fx_circleofdessication.plist"))
    print(parse.get_frames())
    print(parse.get_metadata())

    # for frame_info in parse.get_frames().values():
    #     test = frame_info["frame"]
    #     # pos_list = test.split(",") 
    #     # print(test)
    #     # print(parse.get_position(test))
    #     for item in parse.get_position(test):
    #         print("===================")
    #         print(item.x)
    #         print(item.y)

        # for pos in pos_list:
        #     # print(pos)
        #     print(parse.get_position(pos))
    print("Hello, World!")
    file_list = glob.glob("**/*.plist", recursive=True)
    for pf in file_list:
        print_info(pf)
    
    

if __name__ == "__main__":
    main()