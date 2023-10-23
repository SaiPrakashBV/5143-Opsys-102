"""
 
   ____  _   _ _____ _     _       _     ___   ___  ____    __  __    _    ___ _   _  
  / ___|| | | | ____| |   | |     | |   / _ \ / _ \|  _ \  |  \/  |  / \  |_ _| \ | | 
  \___ \| |_| |  _| | |   | |     | |  | | | | | | | |_) | | |\/| | / _ \  | ||  \| | 
   ___) |  _  | |___| |___| |___  | |__| |_| | |_| |  __/  | |  | |/ ___ \ | || |\  | 
  |____/|_| |_|_____|_____|_____| |_____\___/ \___/|_|     |_|  |_/_/   \_\___|_| \_| 
                                                                                      
 
"""


import os
from shell import shell_helper as sh
import shell as cmd_helper
from Filesystem import FilesystemBase
import sys,datetime
from rich import print as rprint
import getpass
import re
import time


# Define a class named 'shell' to represent the shell environment
class shell():
    def __init__(self):
        self.current_working_dir = "/"
        self.current_path = "~/"
        self.currentuser = None
        self.current_dir_obj = None
        self.file_model= FilesystemBase.FileModel
        self.user_model = FilesystemBase.UserModel
    
     # Method to initialize the user (e.g., root) if no users exist
    def user_initialization(self):
        if not self.user_model.objects().all():
            rprint("[bold red] No User Found[/bold red]")
            rprint("[green] creating new user username(root)[black]:",end="")
            username=input()
            if not username:
                username="root"
            while True:
                rprint("Enter [green] "+username+" ",end="")
                password= getpass.getpass()
                rprint("Confirm ",end="")
                confirm_password= getpass.getpass()
                if password == confirm_password:
                    break
                else:
                    rprint("[red] password didn't match")
            self.user_model(userName=username,password=password,time=str(datetime.datetime.now())).save()

    # Method to initialize the root directory
    def initialize_root_dir(self):
        root_dir_meta_data = {
                "File Name": "",
                "File Path": "/",
                "File Size (bytes)": 4096,
                "File Type" : "Directory",
                "Owner": self.currentuser,
                "Group": self.currentuser,
                "Permissions": "drwxr-xr-x",  
                "Creation Time": datetime.datetime.now(),
                "Last Modification Time": datetime.datetime.now(),
                "Last Access Time": datetime.datetime.now()
        }
        self.current_dir_obj = FilesystemBase.initialize_root_dir(meta_data=root_dir_meta_data)

    # Method for user login
    def user_login(self):
        # self.currentuser="root"
        if self.currentuser == None:
            rprint("[red]No user logged in")
            username=""
            while True:
                rprint("Enter username to login:",end= "")
                username = input()
                rprint("Enter [green]"+username +" ", end="")
                password = getpass.getpass()
                if FilesystemBase.UserModel.objects(userName=username,password=password).first():
                    user = FilesystemBase.UserModel.objects(userName=username,password=password).first()
                    user.time = str(datetime.datetime.now())
                    user.save()
                    break
                else:
                    rprint("[red]incorrect username/password")
            self.currentuser=username
            self.current_path="/"
            self.current_working_dir="/"
            # self.current_dir_obj = FilesystemBase.initialize_root_dir()

# Create an instance of the 'shell' class
current_shell=shell()

# Initialize the user and login the user if necessary
current_shell.user_initialization()
current_shell.user_login()

# Initialize the root directory
current_shell.initialize_root_dir()

# Function to calculate the Levenshtein distance between two strings
def levenshtein_distance(s1, s2):
    if sorted(list(s1))==sorted(list(s2)):return 0
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions, deletions, substitutions = previous_row[j + 1] + 1, current_row[j] + 1, previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]

# Initialize a flag to control the shell execution
exit=False
# exit = True

# Main shell loop
while not exit:
    try:
        if current_shell.currentuser == None:
            current_shell.user_login()
        
        # Display the shell prompt
        rprint("[bold green]"+current_shell.currentuser+"[bold blue]@MongoFileSystem:",current_shell.current_path, "[black]$",end="")
        
        # Get the user's input command
        cmd = sh.get_command(current_shell)
        commands = sh.command_silcer(cmd)
        
        # rprint(commands)
        # rprint(sh.command_silcer(command))
        
        # Dictionary to maintain output and pass it to all commands in pipe
        output_dict={"output":None,"stdout":None,"error":None}
        length = len(commands)
        count = 0
          
        # Iterate through each command and execute it
        for command in commands:
            count+=1
            # Check if the command has an input file, and if so, append it to the parameters for passing as input
            if command['infile']:
                for i in command["infile"]:
                    command["params"].append(i)
                command["infile"] = None
             
            # If an error has occurred in a previous command, stop processing
            if output_dict["error"]:
                break
            
            # Calling help function if help is there in flags without checking remianing parameters
            if "--help" in command["flags"] or command['cmd'] == "help":
                output_dict = cmd_helper.help(command['cmd'],output_dict)
            
            #Calling helper functions for diffrenent commands and passing input params output from previous commands if exists 
            elif command['cmd'] == "exit":
                exit=True
            elif command['cmd'] == "clear":
                output_dict = cmd_helper.clear(command,current_shell=current_shell,output_dict= output_dict)
            elif command['cmd'] == "history" or command['cmd'][0] == "!":
                # If command started with ! adding the command with the number as prefix from history to the command list
                if command['cmd'][0] == "!":
                    for i in sh.command_silcer(cmd_helper.history_cmd(command,current_shell=current_shell,output_dict= output_dict)):
                        commands.append(i)
                else:
                    output_dict = cmd_helper.history_cmd(command,current_shell=current_shell,output_dict= output_dict)
            
            elif command['cmd'] == "upload":
                output_dict = cmd_helper.upload(command,shell_obj=current_shell,output_dict= output_dict)
            
            elif command['cmd'] == "download":
                output_dict = cmd_helper.download(command,shell_obj=current_shell,output_dict= output_dict)
            
            elif command['cmd'] == "pwd":
                output_dict = cmd_helper.pwd(command,current_shell=current_shell,output_dict= output_dict)
            
            elif command['cmd'] == "mkdir":
                output_dict = cmd_helper.mkdir(command,current_shell=current_shell,output_dict = output_dict)
            
            elif command["cmd"] == "ls" or command['cmd'] == "ll":
                if command['cmd'] == "ll":
                    command['flags'].append('la')
                output_dict = cmd_helper.ls(command,current_shell=current_shell,output_dict = output_dict)
            
            elif command['cmd'] == "show":
                output_dict =  cmd_helper.show(command, current_shell,output_dict)
            
            elif command["cmd"] == "chmod":
                command['add_flags'] = re.findall(r'[+](\w+)', cmd)
                command['remove_flags'] = re.findall(r'[-](\w+)', cmd)
                output_dict = cmd_helper.chmod(command, current_shell,output_dict)
            
            elif command['cmd'] == "cd":
                output_dict =  cmd_helper.cd(command, current_shell,output_dict)
            
            elif command['cmd'] == "wc":
                output_dict =  cmd_helper.wc(command, current_shell,output_dict)
            
            elif command['cmd'] == "cp":
                output_dict = cmd_helper.cp(command, current_shell,output_dict)
            
            elif command['cmd'] == "mv":
                output_dict = cmd_helper.mv(command, current_shell,output_dict)
            
            elif command['cmd'] == "cat":
                output_dict = cmd_helper.cat(command, current_shell,output_dict)
            
            elif command['cmd'] == "grep":
                output_dict = cmd_helper.grep(command, current_shell,output_dict)
            
            elif command['cmd'] == "head":
                output_dict = cmd_helper.head(command, current_shell,output_dict)
            
            elif command['cmd'] == "tail":
                output_dict = cmd_helper.tail(command, current_shell,output_dict)
            
            elif command['cmd'] == "less":
                output_dict = cmd_helper.less(command, current_shell,output_dict,flag = length == count)
            
            elif command['cmd'] == "rm" or command['cmd'] == "rmdir":
                output_dict = cmd_helper.remove(command, current_shell,output_dict)
            
            elif command['cmd'] == "sort":
                output_dict = cmd_helper.sort_cmd(command, current_shell,output_dict)
            
            elif command['cmd'] == "touch":
                output_dict = cmd_helper.touch(command, current_shell,output_dict)
            
            elif command['cmd'] == "who":
                output_dict = cmd_helper.who(command, current_shell,output_dict)
            
            #adding users 
            elif command['cmd'] == "add":
                if len(command["params"]):
                    username=command["params"][0]
                    if not username:
                        username="root"
                    # Infinite loop to check passowrd match
                    while True:
                        rprint("Enter [green] "+username+" ",end="")
                        password= getpass.getpass()
                        rprint("Confirm ",end="")
                        confirm_password= getpass.getpass()
                        if password == confirm_password:
                            if not current_shell.user_model.objects(userName = username).first():
                                current_shell.user_model(userName=username,password=password,time=str(datetime.datetime.now())).save()
                            else:
                                output_dict["error"] = "user already exists"
                            break
                        else:
                            rprint("[red]password didn't match")
                        
                else:
                    output_dict["error"] = "Provide Username"            
            
            elif command['cmd'] == "su":
                username = ""
                if len(command["params"]):
                    username=command["params"][0]
                if not username:
                    username = FilesystemBase.UserModel.objects().first()["userName"]
                if current_shell.user_model.objects(userName = username).first():
                    while True:
                        rprint("Enter [green]"+username +" ", end="")
                        password = getpass.getpass()
                        if FilesystemBase.UserModel.objects(userName=username,password=password).first():
                            user = FilesystemBase.UserModel.objects(userName=username,password=password).first()
                            user.time = str(datetime.datetime.now())
                            user.save()
                            break
                        else:
                            rprint("[red]incorrect username/password")
                    current_shell.currentuser=username
                    current_shell.current_path="/"
                    current_shell.current_working_dir="/"
                    
                else:
                    output_dict["error"] = "User not found"
            else:
                # Suggest similar commands if the command is not recognized
                max_distance  = 1
                cmd_word = command['cmd']
                command_list = ["exit","clear","history","show","upload","download","pwd","mkdir","ls","ll", "help","chmod","cd","wc","cp","mv","cat","grep","head","tail","less","rm","rmdir","sort","touch","who","su","add"]
                s=""
                for word in command_list:
                    if levenshtein_distance(word, cmd_word) <= max_distance:
                        s+=word + " or "
                if s:s=s[:-4]
                rprint("[red]Command [bold blue]"+command["cmd"] +"[/bold blue] [red]not found, [green]did you mean: [bold blue] "+str(s))
            
            # If there is an append file, execute the append command
            if command["append_file"]!=[] and command["append_file"]!=None:
                output_dict = cmd_helper.append(command = command,shell_obj = current_shell, output_dict = output_dict)
            
            # If there is an output file, execute the redirect command
            if command["outfile"]!=[] and command["outfile"]!=None:
                output_dict = cmd_helper.redirect(command = command,shell_obj = current_shell, output_dict = output_dict)
        
        # If output(error/stdout) is there printing it to console
        if output_dict:
            if output_dict["stdout"]:
                rprint(output_dict["stdout"])
            if output_dict["error"]:
                rprint("[bold red]"+str(output_dict["error"]))
    
    except Exception as ex:
        rprint(str(ex))