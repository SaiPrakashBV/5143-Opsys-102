"""
 
  __        ___   _  ___     ____ ___  __  __ __  __    _    _   _ ____  
  \ \      / / | | |/ _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
   \ \ /\ / /| |_| | | | | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
    \ V  V / |  _  | |_| | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
     \_/\_/  |_| |_|\___/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                         
 
"""


def who(command, current_shell,output_dict):
    output = current_shell.user_model.objects(userName=current_shell.currentuser).first()
    output_dict["output"] = current_shell.currentuser + "   MongoShell  " + output.time 
    output_dict["stdout"] = current_shell.currentuser+ "   MongoShell   " + output.time
    return output_dict