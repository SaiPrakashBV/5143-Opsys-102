"""
 
   ____  _____ __  __  _____     _______    ____ ___  __  __ __  __    _    _   _ ____   
  |  _ \| ____|  \/  |/ _ \ \   / / ____|  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \  
  | |_) |  _| | |\/| | | | \ \ / /|  _|   | |  | | | | |\/| | |\/| | / _ \ |  \| | | | | 
  |  _ <| |___| |  | | |_| |\ V / | |___  | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| | 
  |_| \_\_____|_|  |_|\___/  \_/  |_____|  \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/  
                                                                                         
 
"""

def remove(command, shell_obj,output_dict):
    if command["cmd"] == "rmdir":
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
                        temp_dir = dir[0]
                    else:
                        exists = False
                if exists:
                    if temp_dir.metadata["File Type"] == "Directory" and len(shell_obj.file_model.objects(parent_id = temp_dir.id).all()) == 0:
                        if (temp_dir.metadata["Permissions"][2] == "w" and temp_dir.metadata["Owner"] == shell_obj.currentuser) or temp_dir.metadata["Permissions"][-2] == "w":
                            temp_dir.delete()
                        else:
                            output_dict["error"] = "cannot remove "+temp_dir.filename+": Permission denied"
                            return output_dict
                    else:
                        if "-r" in command['flags'] and temp_dir.metadata["File Type"] == "Directory":
                            output_dict = rmdir(shell_obj,temp_dir,output_dict)
                            return output_dict
                        elif temp_dir.metadata["File Type"] != "Directory":
                                output_dict["error"] = "can not remove "+temp_dir.filename+": not a directory"
                                return output_dict
                        else:
                            output_dict["error"] = "can not remove "+temp_dir.filename+": non empty directory"
                            return output_dict
                else:
                    output_dict["error"] = i +" not exists"
                    return output_dict
    else:
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
                        temp_dir = dir[0]
                    else:
                        exists = False
                if exists:
                    if temp_dir.metadata["File Type"] != "Directory":
                        if (temp_dir.metadata["Permissions"][2] == "w" and temp_dir.metadata["Owner"] == shell_obj.currentuser) or temp_dir.metadata["Permissions"][-2] == "w":
                            temp_dir.delete()
                        else:
                            output_dict["error"] = "cannot remove "+temp_dir.filename+": Permission denied"
                            return output_dict
                    else:
                        if "-r" in command['flags']:
                            output_dict = rmdir(shell_obj,temp_dir,output_dict)
                            return output_dict
                        else:
                            output_dict["error"] = "cannot remove "+temp_dir.filename+" non empty directory"
                            return output_dict
                else:
                    output_dict["error"] = i +": is not exists"
                    return output_dict

def rmdir(shell_obj,dir_obj,output_dict):
    for obj in shell_obj.file_model.objects(parent_id = dir_obj.id):
        if obj.metadata["File Type"] != "Directory":
            if (obj.metadata["Permissions"][2] == "w" and shell_obj.currentuser == obj.metadata["Owner"]) or obj.metadata["Permissions"][-2] == "w":
                obj.delete()
            else:
                output_dict["error"] = "cannot remove "+dir_obj.filename+": Permission denied"
                return output_dict
        else:
            output_dict = rmdir(shell_obj,obj,output_dict)
            if output_dict["error"]:
                return output_dict
    if (dir_obj.metadata["Permissions"][2] == "w" and shell_obj.currentuser == dir_obj.metadata["Owner"]) or dir_obj.metadata["Permissions"][-2] == "w":
        dir_obj.delete()
    else:
        output_dict["error"] = "cannot remove "+dir_obj.filename+": Permission denied"
        return output_dict
    