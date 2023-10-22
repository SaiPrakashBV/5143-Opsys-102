"""
 
    ____ ____  _____ ____     ____ ___  __  __ __  __    _    _   _ ____  
   / ___|  _ \| ____|  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |  _| |_) |  _| | |_) | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  | |_| |  _ <| |___|  __/  | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
   \____|_| \_\_____|_|      \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                          
 
"""

def grep(command, shell_obj,output_dict):
    output = ""
    if len(command['params'])<2 and output_dict["output"] ==None:
        output_dict['error']  = "insufficicnet args"
        return output_dict
    if output_dict['output']:
        # print(output_dict)
        key = command['params'][0]
        output = "".join([i+"\n" for i in output_dict['output'].split("\n") if key in i])
        if output: output=output[:-1]
        output_dict["output"] = output
        output_dict["stdout"] = output
        return output_dict
    if "-l" in command['flags']:
        key = command['params'][0]
        content = ""
        for i in command['params'][1:]:
            if i:
                path_parts = i.split("/")  
                # print(path_parts)
                if path_parts[0] == "":
                    temp_dir = shell_obj.file_model.objects(filename="/", parent_id = None).all()[0]
                else:
                    temp_dir = shell_obj.current_dir_obj
                dir = temp_dir
                if path_parts[0] == ".":
                    if len(path_parts)>1:
                        path_parts = path_parts[1:]
                    else:
                        path_parts = []
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
                        if key in temp_dir.file.read().decode():
                            content += temp_dir.filename+"\n"
                    else:
                        for file_obj in shell_obj.file_model.objects(parent_id=temp_dir.id).all():
                            if file_obj.metadata["File Type"] != "Directory":
                                if key in file_obj.file.read().decode():
                                    content += file_obj.filename+"\n"
        output = content
        if output: output=output[:-1]
    else:
        key = command['params'][0]
        content = ""
        for i in command['params'][1:]:
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
                        content += temp_dir.file.read().decode()
        output = "".join([i+"\n" for i in content.split("\n") if key in i])
        if output: output=output[:-1]
    output_dict["output"] = output
    output_dict["stdout"] = output
    return output_dict