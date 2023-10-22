"""
 
   _     ____     ____ ___  __  __ __  __    _    _   _ ____  
  | |   / ___|   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |   \___ \  | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  | |___ ___) | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_____|____/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                              
 
"""

import shutil
import pandas as pd
def ls(command,current_shell,output_dict):
    try:
        path = current_shell.current_dir_obj
        items_list = []
        flags = ""
        for i in command['flags']:
            if i not in flags:
                flags+=i
        
        # command["params"] = [x for x in command["params"] if x != "."]
        # command["params"] = [x if x != "/" else "~" for x in command["params"]]
        if command["params"]:
            for i in command["params"]:
                path_parts = i.split("/")
                # print(path_parts)
                if path_parts[0] == "":
                    temp_dir = current_shell.file_model.objects(filename="/", parent_id = None).all()[0]
                else:
                    temp_dir = current_shell.current_dir_obj
                dir = temp_dir

                exists  = True
                for my_path in path_parts:
                    if my_path == "..":
                        dir = current_shell.file_model.objects(id = temp_dir.parent_id).all()
                    elif my_path == "~":
                        dir = current_shell.file_model.objects(parent_id=None,filename="/").all()
                    elif my_path:
                        dir = current_shell.file_model.objects(filename=my_path, parent_id = temp_dir.id).all()
                    if dir and dir[0].metadata["File Type"] == "Directory":
                        # print(dir)
                        temp_dir = dir[0]
                    else:
                        exists = False
                        temp_dir = None
                        path = None
                        
                if exists:
                    items_list.append(temp_dir)
        

        width = shutil.get_terminal_size(fallback=(80, 24)).columns
        if not items_list:
            items_list.append(path)
        # print(flags)
        if 'l' not in flags:
            output = ""
            temp=''
            output2 = ""
            temp2 =''
            hidden = False
            if "a" in flags:
                hidden = True
                temp = ".     .."
                temp2 = ".     .."
            # print(items_list)
            for item in items_list:
                for i in current_shell.file_model.objects(parent_id = item.id).all():
                    if i.filename[0] != "." or (i.filename[0] == "." and hidden):
                        if len(temp) and len(temp)+len(i.filename) > width:
                            output+=temp.strip()+"\n"                
                            output2+=temp2.strip()+"\n"                
                            temp = ""
                            temp2 = ""
                        if i.metadata["File Type"] == "Directory":
                            temp2 += "     " +"[bold blue]" + i.filename + "[/bold blue]"
                        else:
                            temp2 += "     " +"[green]" + i.filename + "[/green]"
                        temp += "     " + i.filename
                if temp:
                    output+=temp.strip()+"\n"                
                    output2+=temp2.strip()+"\n"              
            if len(output)>1:output = output[:-1]
            if len(output)>1:output2 = output2[:-1]
            # print(output)
            output_dict["output"]=output
            output_dict["stdout"]=output2
            output_dict["error"]=None
        
        else:
            data = {"permisions":None, "num_links":None, "owner":None, "group":None, "size":None,"month":None,"date":None, "time":None,"filename":None}
            output = ""
            hidden = False
            human_readable = False
            data_list=[]
            if "a" in flags:
                hidden = True
            if 'h' in flags:
                human_readable = True
            total = 0
            for item in items_list:
                file_list = list(current_shell.file_model.objects(parent_id = item.id).all())
                if hidden:
                    curr_dir = current_shell.file_model.objects(id = item.id).all()[0]
                    curr_dir.filename = "."
                    file_list.append(curr_dir)
                    if item.parent_id:
                        par_dir =current_shell.file_model.objects(id = item.parent_id).all()[0]
                        par_dir.filename = ".."
                        file_list.append(par_dir)
                        

                for i in file_list:
                    data = {"p":None, "n":None, "o":None, "g":None, "s":None,"m":None,"d":None, "t":None,"f":None}
                    data["p"] = i.metadata["Permissions"]
                    data["n"] = get_link_count(i,current_shell)
                    data["o"] = i.metadata["Owner"] 
                    data["g"] = i.metadata["Group"] 
                    if human_readable:
                        val = convert_size(i.metadata["File Size (bytes)"])
                        data["s"] = str(val[0]) + val[1]
                    else:
                        data["s"] = i.metadata["File Size (bytes)"]
                    if i.metadata["File Size (bytes)"]:
                        total += i.metadata["File Size (bytes)"]
                    data["f"] = i.filename
                    date = i.metadata["Creation Time"].strftime("%b %d %H:%M").split()
                    data["m"] = date[0]
                    data["d"] = date[1]
                    data["t"] = date[2]
                    # print(data.values())
                    if i.filename[0] != "." or (i.filename[0] == "." and hidden):
                        data_list.append(data)
            
                    # output += f"{data['permissions']} {data['num_links']} {data['owner']} {data['group']} {data['size']} {data['month']} {data['date']} {data['time']} {data['filename']}\n"
            # print(data_list)
            if data_list:
                df = pd.DataFrame(data_list).sort_values(by='f',key=lambda x: x.str.lower())
            else:
                df = ""
            output= "total "+ str(total//1024) + "\n"
            if human_readable:
                val = convert_size(total)
                output= "total "+ str(int(float(val[0])))+val[1] + "\n"
            for i in str(df).split("\n")[1:]:
                index_of_first_space = i.find(' ')
                if index_of_first_space != -1:
                    result_string = i[index_of_first_space + 1:].strip()
                    output += result_string+"\n"
            if len(output)>1:
                output = output[:-1]
            output_dict["output"]=output
            output_dict["stdout"]=output
            output_dict["error"]=None
    except:
        if command["params"]:
            error=""
            for i in command["params"]:
                error += i+", "
            output_dict["error"]="[red] "+ error[:-2] + " is/are not a valid directory." 
    return output_dict

    
def get_link_count(item,current_shell):
    if item.metadata["File Type"] == "Directory":
        l = [i for i in current_shell.file_model.objects(parent_id = item.id).all() if i.metadata["File Type"] == "Directory"]
        return 2 + len(l)
    else:
        return 1
    
def convert_size(size_in_bytes):
    # List of units and their corresponding sizes
    units = ['', 'K', 'M', 'G', 'T', 'P']
    
    # Initialize the unit and index
    unit = units[0]
    unit_index = 0
    
    # Keep dividing by 1024 until the size is less than 1024 or we run out of units
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes /= 1024.0
        unit_index += 1
        unit = units[unit_index]
    if unit:
        size = f"{size_in_bytes:.1f}"
    else:
        size = int(size_in_bytes)
    # Return the formatted string
    return [str(size),unit]
