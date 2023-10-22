"""
 
   _____ ___  _   _  ____ _   _    ____ ___  __  __ __  __    _    _   _ ____  
  |_   _/ _ \| | | |/ ___| | | |  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
    | || | | | | | | |   | |_| | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
    | || |_| | |_| | |___|  _  | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
    |_| \___/ \___/ \____|_| |_|  \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                               
 
"""

import datetime
from Filesystem import FilesystemBase
def touch(command, shell_obj,output_dict):
    error=""
    for path in command['params']:
        path_parts = path.split("/")
        # print(path_parts)
        if path_parts[0] == "":
            temp_dir = shell_obj.file_model.objects(filename="/", parent_id = None).all()[0]
        else:
            temp_dir = shell_obj.current_dir_obj
        dir = temp_dir
        username = shell_obj.currentuser  
        exists  = True
        for path in path_parts[:-1]:
            if path == "..":
                dir = shell_obj.file_model.objects(id = temp_dir.parent_id).all()
            elif path == "~":
                dir = shell_obj.file_model.objects(parent_id=None,filename="/").all()
            elif path:
                dir = shell_obj.file_model.objects(filename=path, parent_id = temp_dir.id).all()
            if dir and dir[0].metadata["File Type"] == "Directory":
                # print(dir)
                temp_dir = dir[0]
            else:
                meta_data = {
                    "File Name": "",
                    "File Path": "/",
                    "File Size (bytes)": 4096,
                    "File Type" : "Directory",
                    "Owner": username,
                    "Group": username,
                    "Permissions": "drwxr-xr-x",  
                    "Creation Time": datetime.datetime.now(),
                    "Last Modification Time": datetime.datetime.now(),
                    "Last Access Time": datetime.datetime.now()
                }
                new_dir = FilesystemBase.create_dir(dir_name=path,metadata=meta_data,parent_id=temp_dir.id)
                if new_dir:
                    temp_dir=new_dir
        if not shell_obj.file_model.objects(filename=path_parts[-1], parent_id = temp_dir.id).all():
            meta_data = {
                    "File Name": path_parts[-1],
                    "File Path": path,
                    "File Size (bytes)": 0,
                    "File Type" : "text",
                    "Owner": username,
                    "Group": username,
                    "Permissions": "drwxr-xr-x",  
                    "Creation Time": datetime.datetime.now(),
                    "Last Modification Time": datetime.datetime.now(),
                    "Last Access Time": datetime.datetime.now()
                }
            FilesystemBase.save_file(filename = path_parts[-1], file_data = None, metadata=meta_data,parent_id=temp_dir.id)
        else:
            error += path_parts[-1]+" already exists"
    output_dict={"output":None,"stdout":None,"error":error}
    return output_dict