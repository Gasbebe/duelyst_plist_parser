import plistlib
import re
from dataclasses import dataclass

@dataclass
class Position:
    x : str = None
    y : str = None

class d_parse:
    def __init__(self) :
        pass

    def load(self, path):
        with open(path, "rb") as fp:
            print("file path : {}", path)
            self.info = plistlib.load(fp)

    def get_frames(self):
        if "frames" in self.info :
            return self.info["frames"]
        else:
            return {}

    def get_metadata(self):
        if "metadata" in self.info :
            return self.info["metadata"]
        else:
            return {}
        
    def has_key(name, info):
        if name in info :
            return True
        else:
            return False
        
    def get_file_name(self):
        file_name = self.get_metadata()
        if "textureFileName" in file_name:
            print("\033[42m{}\033[m".format(file_name["textureFileName"]))
            return file_name["textureFileName"]
        else:
            return None


    #{0,0}
    def get_position(self, pos_str : str):
        find_list = re.findall(r"\{[\d]+,\s*[\d]+\}", pos_str)
        pos_list = []
        for item in find_list :
            coordinates = item.strip("{}")
            pos = Position()
            pos.x, pos.y = coordinates.replace(" ", "").split(",")
            pos_list.append(pos)
            # []
        return pos_list