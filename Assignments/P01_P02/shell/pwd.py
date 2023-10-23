"""
 
   ______        ______     ____ ___  __  __ __  __    _    _   _ ____  
  |  _ \ \      / /  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |_) \ \ /\ / /| | | | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  |  __/ \ V  V / | |_| | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_|     \_/\_/  |____/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                        
 
"""

def pwd(command,current_shell,output_dict):
    temp = current_shell.current_dir_obj
    pwd = temp.filename+"/"
    while temp.parent_id != None:
        temp = current_shell.file_model.objects(id = temp.parent_id).first()
        if temp:
            pwd = temp.filename+"/" + pwd
    output_dict["output"]=current_shell.current_path
    output_dict["stdout"]=current_shell.current_path
    output_dict["error"]=None
    return output_dict