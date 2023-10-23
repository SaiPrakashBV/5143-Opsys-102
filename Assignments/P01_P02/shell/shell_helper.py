"""
 
   ____  _   _ _____ _     _       _   _ _____ _     ____  _____ ____  
  / ___|| | | | ____| |   | |     | | | | ____| |   |  _ \| ____|  _ \ 
  \___ \| |_| |  _| | |   | |     | |_| |  _| | |   | |_) |  _| | |_) |
   ___) |  _  | |___| |___| |___  |  _  | |___| |___|  __/| |___|  _ < 
  |____/|_| |_|_____|_____|_____| |_| |_|_____|_____|_|   |_____|_| \_\
                                                                       
 
"""


import sys
import tty
import termios
import re
from Filesystem import FilesystemBase
import datetime

history = []

def get_command(current_shell):
    cmd=''
    suggestions = []
    count = 0
    arrow_count = 0
    history = retrieve_history(current_shell,[])
    print(">",end="",flush=True)
    while 1:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch != "\x1b" and arrow_count>0:
            arrow_count=0
        if ch != "\t":
            suggestions = []
        if ch == "\x7f" : # backslash
            if count > 0:
                print('\b \b',end='',flush=True)
                count-=1
            if cmd:
                cmd=cmd[:-1]
        elif ch == "\x03": # ctrl+c
            cmd = "exit" 
            break
        elif ch == "\r":
            break
        elif ch == "\t":
            if suggestions == []:
                
                if "|" in cmd:
                    temp_cmd = cmd.split("|")[-1]
                else:
                    temp_cmd = cmd
                if len(temp_cmd.split())<2 and len(temp_cmd.split())>0:
                    cmd_list= ["exit","clear","history","show","upload","download","pwd","mkdir","ls","ll", "help","chmod","cd","wc","cp","mv","cat","grep","head","tail","less","rm","rmdir","sort","touch","who"]
                    for i in cmd_list:
                        if i.startswith(temp_cmd.split()[-1].strip()):
                            suggestions.append(i)
                for item in FilesystemBase.FileModel.objects(parent_id = current_shell.current_dir_obj.id):
                    if len(cmd.split())>1:
                        if item.filename.startswith(cmd.split()[-1].strip()):
                            suggestions.append(item.filename)
            if suggestions != []:
                lastwordlen = len(cmd.split()[-1])
                for i in range(count):
                    print('\b \b',end='',flush=True)
                    count=0
                cmd = cmd[:-lastwordlen]+suggestions[0]
                if len(suggestions)>0:
                    suggestions = suggestions[1:]
                else:
                    suggestions = []
                print(cmd,end='',flush=True)
            
                count=len(cmd)
            # print(cmd)
        elif ch == "\x1b":  # Arrow keys generate escape sequences
            escape_sequence = sys.stdin.read(2)  # Read the next two characters
            if escape_sequence == "[C" or escape_sequence == "[D":  #  # Right arrow  && Left arrow:
                ch = ""
                ch =""
            else:
                for i in range(count):
                    print('\b \b',end='',flush=True)
                    count=0
                    cmd=""
                if escape_sequence == "[A":  # Up arrow
                    
                    if arrow_count < len(history):
                        arrow_count += 1
                        if len(history) >= arrow_count:
                            cmd = history[-arrow_count] 
                    for i in range(count):
                        print('\b \b',end='',flush=True)
                        count=0
                        # print("Up arrow pressed")
                    if arrow_count == 0:
                        cmd=''
                elif escape_sequence == "[B":  # Down arrow
                    if arrow_count > 1:
                        arrow_count -= 1
                        if len(history) >= arrow_count:
                            cmd = history[-arrow_count]
                        # print("Down arrow pressed")
                    if arrow_count == 0:
                        cmd=''
                # print("Left arrow pressed")
                print(cmd,end='',flush=True)
                count=len(cmd)
        else:
            print(ch,end='',flush=True)
            cmd+=ch
            count+=1
    print()
    history.append(cmd)
    add_history(current_shell,cmd)
    return cmd

def retrieve_history(current_shell,history):
    parent_id = current_shell.file_model.objects(parent_id=None).all()[0].id
    items = current_shell.file_model.objects(parent_id=parent_id, filename = "history.txt").all()
    output = history
    if len(items):
        if items[0].file.read() != None:
            content = items[0].file.read().decode().split("\n")
            for i in content:
                index_of_first_space = i.find(' ')
                if index_of_first_space != -1:
                    result_string = i[index_of_first_space + 1:].strip()
                    output.append(result_string)
        return output
    else:
        file_details = {
            "File Name": "history.txt",
            "File Path": "/",
            "File Size (bytes)": len(history),
            "File Type" : "text",
            "Owner": current_shell.currentuser,
            "Group": current_shell.currentuser,
            "Permissions": "-r-xr-xr-x",  
            "Creation Time": datetime.datetime.now(),
            "Last Modification Time": datetime.datetime.now(),
            "Last Access Time": datetime.datetime.now()
        }
        parent_id = current_shell.file_model.objects(parent_id=None).all()[0].id
        FilesystemBase.save_file(filename='history.txt',file_data=None,metadata=file_details,parent_id = parent_id)
        return output

def add_history(current_shell, cmd):
    parent_id = current_shell.file_model.objects(parent_id=None).all()[0].id
    filename="history.txt"
    objs = current_shell.file_model.objects(parent_id=parent_id, filename=filename).all()
    
    if len(objs):
        content = ""
        obj = objs[0]
        if obj and obj.file:
            content= obj.file.read().decode()
            updated_content =( content+ str(len(content.split("\n"))) + " " + cmd +"\n").encode('utf-8')
            # Replace the file's content with the updated content
            obj.file.delete()
            obj.file.put(updated_content,filename = obj.filename)
            obj.metadata["File Size (bytes)"]= len(updated_content)
            obj.save()
        else:
            content= ""
            updated_content =("1 " + cmd +"\n").encode('utf-8')
            # Replace the file's content with the updated content
            obj.file.put(updated_content,filename = obj.filename)
            obj.metadata["File Size (bytes)"]= len(updated_content)
            obj.save()
        # items[0].update()


def command_silcer(cmd):
    cmds=cmd.split("|")
    cmds_parsed=[]
    for command in cmds:
        command = command.strip()
        flags = []
        params = []
        infile = None
        outfile = None
        append_file = None
        if '<' in command or '>' in command:
            infile = re.findall(r'<\s*([\w._]+)', command)
            command = re.sub(r'<\s*([\w._]+)', '', command)
            append_file = re.findall(r'>>\s*([\w._]+)', command)            
            command = re.sub(r'>>\s*([\w._]+)', '', command)
            outfile = re.findall(r'>\s*([\w._]+)', command)
            command = re.sub(r'>\s*([\w._]+)', '', command)
        parts = command.split(" ")
        for word in parts[1:]:
            if word:
                if '-' in word:
                    flags.append(word)
                else:
                    params.append(word.strip('"').strip("'"))
        
        cmds_parsed.append({'cmd':parts[0],"params": params, "flags": flags,"infile":infile, "outfile" :outfile,"append_file":append_file})

    return cmds_parsed