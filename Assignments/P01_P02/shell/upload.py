"""
 
   _   _ ____  _     ___    _    ____     ____ ___  __  __ __  __    _    _   _ ____   
  | | | |  _ \| |   / _ \  / \  |  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \  
  | | | | |_) | |  | | | |/ _ \ | | | | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | | 
  | |_| |  __/| |__| |_| / ___ \| |_| | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| | 
   \___/|_|   |_____\___/_/   \_\____/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/  
                                                                                       
 
"""


import os
import datetime
from Filesystem import FilesystemBase

def upload(command,shell_obj,output_dict):
    parent_id = shell_obj.current_dir_obj.id
    username = shell_obj.currentuser    
    for i in command["params"]:
        if os.path.isdir(i):
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
            obj = FilesystemBase.create_dir(dir_name = i,metadata = meta_data,parent_id = parent_id)
            if obj!= None:
                upload_dir(i,shell_obj,parent_id=obj.id)
            else:
                output_dict["error"] = "Folder already exists"
                return output_dict
        elif os.path.isfile(i):
            
            meta_data = FilesystemBase.read_meta_data(i)
            meta_data['Owner'] = username
            meta_data['Group'] = username
            with open(i, 'rb') as file_data:
                FilesystemBase.save_file(i.split("/")[-1], file_data, metadata=meta_data,parent_id = parent_id)
        else:
            output_dict["error"] = "Not Exists"
            return output_dict
    output_dict["output"] = "[green bold]Uploaded"
    output_dict["stdout"] = "[green bold]Uploaded"
    return output_dict


def upload_dir(dir,shell_obj,parent_id):
    username = shell_obj.currentuser    
    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)
        if os.path.isdir(item_path):
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
            obj = FilesystemBase.create_dir(dir_name = item,metadata = meta_data,parent_id = parent_id)
            # If it's a directory, call the function recursively
            upload_dir(item_path, parent_id = obj.id, shell_obj = shell_obj)
        
        else:
            meta_data = FilesystemBase.read_meta_data(item_path)
            meta_data['Owner'] = username
            meta_data['Group'] = username
            with open(item_path, 'rb') as file_data:
                FilesystemBase.save_file(item.split("/")[-1], file_data, metadata=meta_data,parent_id = parent_id)
    
    
