"""
 
   __  __ _  ______ ___ ____     ____ ___  __  __ __  __    _    _   _ ____  
  |  \/  | |/ /  _ \_ _|  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |\/| | ' /| | | | || |_) | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  | |  | | . \| |_| | ||  _ <  | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_|  |_|_|\_\____/___|_| \_\  \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                             
 
"""

from Filesystem import FilesystemBase
import datetime
def mkdir(command,current_shell,output_dict):
    parent_id = current_shell.current_dir_obj.id
    error=""
    username = current_shell.currentuser    
    for i in command['params']:
        if '/' not in i:
            dir_name=i
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
            dir_obj = FilesystemBase.create_dir(dir_name = dir_name, parent_id = parent_id, metadata = meta_data)
            if dir_obj == None:
                error += (f"Same folder:{dir_name} already exists\n")    
        else:
            error += (f"mkdir: cannot create directory '{i}': No such file or directory\n")
    output_dict['error'] = error
    return output_dict