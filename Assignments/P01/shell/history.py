"""
 
   _   _ ___ ____ _____ ___  ______   __   ____ ___  __  __ __  __    _    _   _ ____  
  | | | |_ _/ ___|_   _/ _ \|  _ \ \ / /  / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |_| || |\___ \ | || | | | |_) \ V /  | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  |  _  || | ___) || || |_| |  _ < | |   | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_| |_|___|____/ |_| \___/|_| \_\|_|    \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                                       
 
"""


def history_cmd(command,current_shell,output_dict):
    parent_id = current_shell.file_model.objects(parent_id=None).all()[0].id
    items = current_shell.file_model.objects(parent_id=parent_id, filename = "history.txt").all()
    output = None
    if len(items):
        if items[0].file.read() != None:
            output = items[0].file.read().decode()
        
    if command["cmd"][0]!="!":        
        output_dict={"output":output,"stdout":output,"error":None}
        return output_dict
    else:
        num = int(command['cmd'][1:])
        output = output.split("\n")
        for i in output:
            if i.startswith(str(num)):
                return i[i.index(" ")+1:]
