"""
 
   __  ____     __   ____ ___  __  __ __  __    _    _   _ ____   
  |  \/  \ \   / /  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \  
  | |\/| |\ \ / /  | |  | | | | |\/| | |\/| | / _ \ |  \| | | | | 
  | |  | | \ V /   | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| | 
  |_|  |_|  \_/     \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/  
                                                                  
 
"""

from Filesystem import FilesystemBase
import datetime
def mv(command, shell_obj,output_dict):
    output_dict={"output":None,"stdout":None,"error":None}
    source_path,dest_path = None,None
    source_obj,dest_obj = None, None
    username = shell_obj.currentuser
    if len(command['params'])==2 :
        source_path = command["params"][0]
        dest_path = command["params"][1]
    else:
        output_dict["error"] = "Invalid number of arguments"
        return output_dict
    
    if source_path and dest_path :
        #source_path
        temp_dir = shell_obj.current_dir_obj
        source_path_parts = source_path.split("/")
        file_or_dir = source_path_parts[-1]
        for path in source_path_parts[:-1]:
            if path == "..":
                if temp_dir.parent_id!= "None":
                    temp_dir = shell_obj.file_model.objects(id = temp_dir.parent_id).first()
                else:
                    output_dict["error"] = "Invalid source dir"
                    return output_dict
            elif path == ".":
                temp_dir = temp_dir
            else:
                result = shell_obj.file_model.objects(parent_id = temp_dir.id, filename = path).all()
                if result: 
                   temp_dir = result
                else:
                    output_dict["error"] = "Invalid source dir"
                    return output_dict
        if len(shell_obj.file_model.objects(parent_id = temp_dir.id, filename = file_or_dir).all()):
            source_obj = shell_obj.file_model.objects(parent_id = temp_dir.id, filename = file_or_dir).first()
        elif file_or_dir == ".":
            source_obj = temp_dir
        elif file_or_dir == ".." and temp_dir.parent_id!= None:
            source_obj = shell_obj.file_model.objects(id = temp_dir.parent_id).first()
        else:
            output_dict["error"] = "Invalid source dir/file"
            return output_dict
        
        temp_dir = shell_obj.current_dir_obj
        dest_path_parts = dest_path.split("/")
        file_or_dir = dest_path_parts[-1]
        for path in dest_path_parts[:-1]:
            if path == "..":
                if temp_dir.parent_id!= "None":
                    temp_dir = shell_obj.file_model.objects(id = temp_dir.parent_id).first()
                else:
                    output_dict["error"] = "Invalid destination dir"
                    return output_dict
            elif path == ".":
                temp_dir = temp_dir
            else:
                
                result = shell_obj.file_model.objects(parent_id = temp_dir.id, filename = path).all()
                if result: 
                   temp_dir = result
                else:
                    meta_data = {
                    "File Name": path,
                    "File Path": temp_dir.metadata["File Path"]+"/"+temp_dir.filename,
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
                    else:
                        output_dict["error"] = "Failed to create destination dir/file"
                        return output_dict
        if file_or_dir == ".":
            file_or_dir = temp_dir.filename
            temp_dir = shell_obj.file_model.objects(parent_id = temp_dir.id)

        if source_obj.metadata["File Type"]!= "Directory":
            
            if file_or_dir == ".":
                    obj = temp_dir
            elif file_or_dir == ".." and temp_dir.parent_id!=None:
                obj = shell_obj.file_model.objects(id = temp_dir.parent_id).first()
            else:
                obj = shell_obj.file_model.objects(filename=file_or_dir, parent_id = temp_dir.id).first()
            if obj:
                if obj.metadata["File Type"]!= "Directory":
                    try:
                        content =  source_obj.file.read()
                    except:
                        content = None
                    # Replace the file's content with the updated content
                    if obj.file:obj.file.delete()
                    try:
                        obj.file.put(content,filename = obj.filename)
                    except:
                        pass
                    obj.save()
                    source_obj.delete()
                elif obj.metadata["File Type"] == "Directory":
                    meta_data = source_obj.metadata
                    meta_data["File Path"] =  obj.metadata["File Path"]+"/"+obj.filename,
                    meta_data["Last Modification Time"] =  datetime.datetime.now(),
                    meta_data["Last Access Time"] = datetime.datetime.now()
                    FilesystemBase.save_file(filename = source_obj.filename, file_data = source_obj.file,metadata=meta_data,parent_id=obj.id)
                    source_obj.delete()
            else:
                if "." in file_or_dir and file_or_dir!= "." or file_or_dir!= "..":
                    meta_data = source_obj.metadata
                    meta_data["File Name"] = file_or_dir
                    meta_data["File Path"] =  temp_dir.metadata["File Path"]+"/"+temp_dir.filename,
                    meta_data["Last Modification Time"] =  datetime.datetime.now(),
                    meta_data["Last Access Time"] = datetime.datetime.now()
                    FilesystemBase.save_file(filename = file_or_dir, file_data = source_obj.file,metadata=meta_data,parent_id=temp_dir.id)
                    source_obj.delete()
                else:
                    meta_data = {
                    "File Name": file_or_dir,
                    "File Path": temp_dir.metadata["File Path"]+"/"+temp_dir.filename,
                    "File Size (bytes)": 4096,
                    "File Type" : "Directory",
                    "Owner": username,
                    "Group": username,
                    "Permissions": "drwxr-xr-x",  
                    "Creation Time": datetime.datetime.now(),
                    "Last Modification Time": datetime.datetime.now(),
                    "Last Access Time": datetime.datetime.now()}
                    new_dir = FilesystemBase.create_dir(dir_name=file_or_dir,metadata=meta_data,parent_id=temp_dir.id)
                    meta_data = source_obj.metadata
                    meta_data["File Path"] =  new_dir.metadata["File Path"]+"/"+new_dir.filename,
                    meta_data["Last Modification Time"] =  datetime.datetime.now(),
                    meta_data["Last Access Time"] = datetime.datetime.now()
                    FilesystemBase.save_file(filename = source_obj.filename, file_data = source_obj.file,metadata=meta_data,parent_id=new_dir.id)
                    source_obj.delete()
        else:
            obj = shell_obj.file_model.objects(filename=file_or_dir, parent_id = temp_dir.id).first()
            if obj:
                if obj.metadata["File Type"] == "Directory":
                    source_obj.parent_id = obj.id
                    source_obj.save()
            else:
                if "." not in file_or_dir:
                    meta_data = {
                    "File Name": file_or_dir,
                    "File Path": temp_dir.metadata["File Path"]+"/"+temp_dir.filename,
                    "File Size (bytes)": 4096,
                    "File Type" : "Directory",
                    "Owner": username,
                    "Group": username,
                    "Permissions": "drwxr-xr-x",  
                    "Creation Time": datetime.datetime.now(),
                    "Last Modification Time": datetime.datetime.now(),
                    "Last Access Time": datetime.datetime.now()}
                    new_dir = FilesystemBase.create_dir(dir_name=file_or_dir,metadata=meta_data,parent_id=temp_dir.id)
                    if new_dir:
                        source_obj.parent_id = new_dir.id
                        source_obj.save()
                else:
                    output_dict["error"] = "Moving folders into file is not possible: Try copying to folders."
                    return output_dict      
    
    output_dict={"output":None,"stdout":None,"error":None}
    return output_dict
