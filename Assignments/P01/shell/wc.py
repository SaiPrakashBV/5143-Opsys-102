"""
 
  __        ______    ____ ___  __  __ __  __    _    _   _ ____  
  \ \      / / ___|  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
   \ \ /\ / / |     | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
    \ V  V /| |___  | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
     \_/\_/  \____|  \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                  
 
"""

def wc(command, shell_obj,output_dict):
    content = ""
    output=""
    if output_dict['output']:
        content = output_dict['output']
        i=""
    else:
        for i in command['params']:
            if i:
                content = ""
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
        lines = content.split('\n')
        if "-l" in command['flags']:
            line_count = len(lines)
            output += f'{line_count} '
        if "-m" in command['flags']:
            char_count = len(content)          
            output+=f'{char_count} '
        if "-w" in command['flags']:
            word_count = sum(len(line.split()) for line in lines)
            output+= f'{word_count} '
        elif "-l" not in command['flags'] and "-m" not in command['flags']  and "-w" not in command['flags']:
            line_count = len(lines)
            word_count = sum(len(line.split()) for line in lines)
            char_count = len(content)          
            output += f'{line_count} '
            output+= f'{word_count} '
            output+=f'{char_count} '
        output += i
        output+= "\n"
    output_dict["output"] = output
    output_dict["stdout"] = output
    return output_dict