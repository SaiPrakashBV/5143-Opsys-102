"""
 
   _____  _    ___ _        ____ ___  __  __ __  __    _    _   _ ____  
  |_   _|/ \  |_ _| |      / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
    | | / _ \  | || |     | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
    | |/ ___ \ | || |___  | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
    |_/_/   \_\___|_____|  \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                        
 
"""

def tail(command, shell_obj,output_dict):
    content = ""
    num_lines = 10
    output = ""
    if "-n" in command["flags"]:
        for i in command['params']: 
            if i.isdigit():
                num_lines = int(i)
                command["params"].remove(i)
                
    if output_dict['output']:
        t = output_dict['output'].split('\n')
        t = t[-min(num_lines+1,len(t)+1):]
        output += "".join([i+"\n" for i in t])
        if output: output=output[:-1]
        output_dict["output"] = output
        output_dict["stdout"] = output
        return output_dict
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
                if len(command['params'])>1:
                    content += "<< " + i + ">>\n"
                if temp_dir.metadata["File Type"] != "Directory":
                    t = temp_dir.file.read().decode().split("\n")
                    t = t[-min(num_lines+1,len(t)+1):]
                    content += "".join([i+"\n" for i in t])
                    content = content[:-1]
                    if len(command['params'])>1:
                        content += "\n\n"
                else:
                    output_dict["error"] =  "Invalid File "+ i
                    return output_dict
            else:
                output_dict["error"] =  "File " + i+" does not exist"
                return output_dict
    output_dict["output"] = content
    output_dict["stdout"] = content
    return output_dict