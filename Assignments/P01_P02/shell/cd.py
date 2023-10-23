"""
 
    ____ ____     ____ ___  __  __ __  __    _    _   _ ____  
   / ___|  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |   | | | | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  | |___| |_| | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
   \____|____/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                              
 
"""

def cd(command, shell_obj,output_dict):
    output_dict={"output":None,"stdout":None,"error":None}
    if len(command['params'])==0:
        command['params'] ="~"
    if len(command['params']):
        path_parts = command['params'][0].split("/")
        # print(path_parts)
        if path_parts[0] == "":
            temp_dir = shell_obj.file_model.objects(filename="/", parent_id = None).all()[0]
        else:
            temp_dir = shell_obj.current_dir_obj
        dir = temp_dir
        
        exists  = True
        for path in path_parts:
            if path == ".":
                dir = [temp_dir]
            elif path == "..":
                dir = shell_obj.file_model.objects(id = temp_dir.parent_id).all()
            elif path == "~":
                dir = shell_obj.file_model.objects(parent_id=None,filename="/").all()
            elif path:
                dir = shell_obj.file_model.objects(filename=path, parent_id = temp_dir.id).all()
            if dir and dir[0].metadata["File Type"] == "Directory":
                # print(dir)
                temp_dir = dir[0]
            else:
                exists = False
        if exists:
            shell_obj.current_dir_obj = temp_dir
            temp_path = ""
            temp_path_obj = temp_dir
            for i in range(3):
                if temp_path_obj != None:
                    temp_path = temp_path_obj.filename + "/" + temp_path
                    temp_path_obj = shell_obj.file_model.objects(id = temp_path_obj.parent_id).first()
                    # print(temp_path_obj)
            if temp_path_obj == None:
                temp_path = "~"+temp_path[1:]
            else:
                temp_path = "./" + temp_path
                    
            
            shell_obj.current_path = temp_path 
            shell_obj.current_working_dir = temp_dir.filename
        else:
            output_dict["error"] = "folder "+command["params"][0]+ " not found."
    return output_dict