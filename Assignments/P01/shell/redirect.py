"""
 
   ____  _____ ____ ___ ____  _____ ____ _____    ____ ___  __  __ __  __    _    _   _ ____  
  |  _ \| ____|  _ \_ _|  _ \| ____/ ___|_   _|  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |_) |  _| | | | | || |_) |  _|| |     | |   | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  |  _ <| |___| |_| | ||  _ <| |__| |___  | |   | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_| \_\_____|____/___|_| \_\_____\____| |_|    \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                                              
 
"""

from  Filesystem import FilesystemBase 
import datetime
def redirect(command,shell_obj, output_dict):
    if output_dict["output"] == None:
        output_dict["output"] = ""
    if command["outfile"]:
        path_parts = command['outfile'][0].split("/")
        # print(path_parts)
        if path_parts[0] == "":
            temp_dir = shell_obj.file_model.objects(filename="/", parent_id = None).all()[0]
        else:
            temp_dir = shell_obj.current_dir_obj
        dir = temp_dir
        username = shell_obj.currentuser  
        exists  = True
        for path in path_parts[:-1]:
            if path == "..":
                dir = shell_obj.file_model.objects(id = temp_dir.parent_id).all()
            elif path == "~":
                dir = shell_obj.file_model.objects(parent_id=None,filename="/").all()
            elif path:
                dir = shell_obj.file_model.objects(filename=path, parent_id = temp_dir.id).all()
            if dir and dir[0].metadata["File Type"] == "Directory":
                # print(dir)
                temp_dir = dir[0]
            else:
                
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
                new_dir = FilesystemBase.create_dir(dir_name=path,metadata=meta_data,parent_id=temp_dir.id)
                if new_dir:
                    temp_dir=new_dir
        if shell_obj.file_model.objects(filename=path_parts[-1], parent_id = temp_dir.id).all():
            obj = shell_obj.file_model.objects(filename=path_parts[-1], parent_id = temp_dir.id).all()[0]
            if obj and obj.file:
                content = obj.file.read() + output_dict["output"].encode('utf-8')
                # Replace the file's content with the updated content
                obj.file.delete()
                obj.file.put(content,filename = obj.filename)
                obj.save()
                # obj.file.replace(obj.file.file.read() + output_dict["output"].encode('utf-8'))
        else:
            meta_data = {
                "File Name": "",
                "File Path": "/",
                "File Size (bytes)": len(output_dict["output"].encode('utf-8')),
                "File Type" : "text",
                "Owner": username,
                "Group": username,
                "Permissions": "drwxr-xr-x",  
                "Creation Time": datetime.datetime.now(),
                "Last Modification Time": datetime.datetime.now(),
                "Last Access Time": datetime.datetime.now()
            }
            FilesystemBase.save_file(filename = path_parts[-1], file_data = output_dict["output"].encode('utf-8'),metadata=meta_data,parent_id=temp_dir.id)
    output_dict={"output":None,"stdout":None,"error":None}
    return output_dict
