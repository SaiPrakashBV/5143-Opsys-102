"""
 
   ____   _____        ___   _ _     ___    _    ____     ____ ___  __  __ __  __    _    _   _ ____  
  |  _ \ / _ \ \      / / \ | | |   / _ \  / \  |  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | | | | | | \ \ /\ / /|  \| | |  | | | |/ _ \ | | | | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  | |_| | |_| |\ V  V / | |\  | |__| |_| / ___ \| |_| | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |____/ \___/  \_/\_/  |_| \_|_____\___/_/   \_\____/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                                                      
 
"""

import os
def download(command,shell_obj,output_dict):
    try:
        for i in command["params"]:
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
                        with open(temp_dir.filename,"wb") as file:
                            file.write(temp_dir.file.read())
                    else:
                        download_dir(temp_dir,os.getcwd(),shell_obj)
                else:
                    output_dict["error"] = "File/Folder not exist"
    except:
        output_dict["error"] = "Error occured while downloading"
        return output_dict
def download_dir(temp_dir , path,shell_obj):
    path = os.path.join(path,temp_dir.filename,)
    if not os.path.exists(path):
        os.makedirs(path)

    items = shell_obj.file_model.objects(parent_id=temp_dir.id)

    for item in items:
        item_path = os.path.join(path, item.filename)
        if item.metadata["File Type"] == "Directory":
            download_dir(item, item_path,shell_obj)
        else:
            with open(item_path, 'wb') as local_file:
                local_file.write(item.file.read())