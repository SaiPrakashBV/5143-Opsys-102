"""
 
   ____   ___  ____ _____    ____ ___  __  __ __  __    _    _   _ ____  
  / ___| / _ \|  _ \_   _|  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  \___ \| | | | |_) || |   | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
   ___) | |_| |  _ < | |   | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |____/ \___/|_| \_\|_|    \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                         
 
"""


def sort_cmd(command, shell_obj,output_dict):
    content = ""
    if output_dict['output']:
        content = output_dict['output']
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
                        content += temp_dir.file.read().decode()
    if content:
        if "-r" in command["flags"]:
            content = "".join([i+"\n" for i in sorted(content.split("\n"))][::-1])
        else:
            content = "".join([i+"\n" for i in sorted(content.split("\n"))])
        content = content[:-1]  
    output_dict["output"] = content
    output_dict["stdout"] = content
    return output_dict