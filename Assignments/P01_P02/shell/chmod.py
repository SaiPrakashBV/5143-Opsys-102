"""
 
    ____ _   _ __  __  ___  ____     ____ ___  __  __ __  __    _    _   _ ____  
   / ___| | | |  \/  |/ _ \|  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |   | |_| | |\/| | | | | | | | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  | |___|  _  | |  | | |_| | |_| | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
   \____|_| |_|_|  |_|\___/|____/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                                 
 
"""

from Filesystem import FilesystemBase
def chmod(command, current_shell,output_dict):
    permissions = None
    for i in command['params']:
        if i.isdigit():
            permissions = octal_to_rwx(i)
    file_list = []
    for i in command['params']:
        if "+" not in i and "-" not in i:
            path_parts = i.split("/")  
            # print(path_parts)
            if path_parts[0] == "":
                temp_dir = current_shell.file_model.objects(filename="/", parent_id = None).all()[0]
            else:
                temp_dir = current_shell.current_dir_obj
            dir = temp_dir
            exists  = True
            for path in path_parts:
                if path == "..":
                    dir = current_shell.file_model.objects(id = temp_dir.parent_id).all()
                if path == "~":
                    dir = current_shell.file_model.objects(parent_id=None,filename="/").all()
                elif path:
                    dir = current_shell.file_model.objects(filename=path, parent_id = temp_dir.id).all()
                if dir:
                    # print(dir)
                    temp_dir = dir[0]
                else:
                    exists = False
            if exists:
                file_list.append(temp_dir)
            else:
                output_dict["error"] = "File :"+ i +"not exists"
                return output_dict
        
        for file_obj in file_list:
            old_permissions = file_obj.metadata['Permissions']
            if permissions:
                old_permissions = old_permissions[0] + permissions
            else:
                old_permissions = list(old_permissions)
                for flag in command['add_flags']:
                    if "r" in flag: 
                        old_permissions[1] = 'r'
                        old_permissions[4] = 'r'
                        old_permissions[7] = 'r'
                    if "w" in flag:  
                        old_permissions[2] = 'w'
                        old_permissions[5] = 'w'
                        old_permissions[8] = 'w'
                    if "x" in flag:  
                        old_permissions[3] = 'x'
                        old_permissions[6] = 'x'
                        old_permissions[9] = 'x'
                for flag in command['remove_flags']:
                    if "r" in flag: 
                        old_permissions[1] = '-'
                        old_permissions[4] = '-'
                        old_permissions[7] = '-'
                    if'w' in flag: 
                        old_permissions[2] = '-'
                        old_permissions[5] = '-'
                        old_permissions[8] = '-'
                    if "x" in flag: 
                        old_permissions[3] = '-'
                        old_permissions[6] = '-'
                        old_permissions[9] = '-'
                old_permissions = "".join(old_permissions)
            file_obj.metadata["Permissions"] = old_permissions
            if file_obj.metadata["Owner"] == current_shell.currentuser:
                file_obj.save()
            else:
                output_dict["error"] = "cannot change permissions: Permission denied"
                return output_dict

def octal_to_rwx(octal_permission):
    rwx_format = ''
    oct_dict={"0":"---","1":"--x","2":"-w-","3":"-wx","4":"r--","5":"r-x","6":"rw-","7":"rwx"}
    for i in str(octal_permission):
        rwx_format += oct_dict[i]
    if len(rwx_format)!=9:
        return None
    return rwx_format 
