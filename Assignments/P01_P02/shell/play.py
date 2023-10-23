"""
 
   ____  _        _ __   __   ____ ___  __  __ __  __    _    _   _ ____  
  |  _ \| |      / \\ \ / /  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |_) | |     / _ \\ V /  | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  |  __/| |___ / ___ \| |   | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_|   |_____/_/   \_\_|    \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                          
 
"""

import cv2
from PIL import Image
from io import BytesIO
import threading
import numpy as np
import base64

def is_image(media):
    file_extension = media.filename.split('.')[-1].lower()
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']
    return file_extension in image_extensions

media = None
def show_image(image_Data,filename):
    cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
    cv2.imshow(filename, image_Data)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show(command, shell_obj,output_dict):
    for i in command['params']:
        if i:
            path_parts = i.split("/")  
            # print(path_parts)
            if path_parts[0] == "":
                temp_dir = shell_obj.file_model.objects(filename="/", parent_id = None).all()[0]
            else:
                temp_dir = shell_obj.current_dir_obj
            dir = temp_dir
            exists  = True
            for path in path_parts:
                if path == "..":
                    dir = shell_obj.file_model.objects(id = temp_dir.parent_id).all()
                if path == "~":
                    dir = shell_obj.file_model.objects(parent_id=None,filename="/").all()
                elif path:
                    dir = shell_obj.file_model.objects(filename=path, parent_id = temp_dir.id).all()
                if dir:
                    # print(dir)
                    temp_dir = dir[0]
                else:
                    exists = False
            if exists:
                if temp_dir.metadata["File Type"] != "Directory":
                    media = temp_dir
            else:
                output_dict["error"] = "File not found/Invalid"
                return output_dict

    if media:
        # Check the media type based on your application logic
        if is_image(media):
            pil_image = Image.open(BytesIO(media.file.read()))
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            image_name = media.filename
            thread = threading.Thread(target=show_image,args=(opencv_image,image_name))
            thread.start()
            
            return output_dict
        else:
            print("Unknown media type.")
    else:
        output_dict["error"] = ["Media file not found."]
        return output_dict

    
