"""
 
   _   _ _____ _     ____     ____ ___  __  __ __  __    _    _   _ ____  
  | | | | ____| |   |  _ \   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |_| |  _| | |   | |_) | | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  |  _  | |___| |___|  __/  | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_| |_|_____|_____|_|      \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                          
 
"""


help_cmd={	"cat":
"""Usage: cat [file1] [file2] ...
Description: Concatenates and displays the content of files.""",
		"cd": 
"""Usage: cd [directory]
 Description: Changes the shell working directory to the given directory.""",
		"chmod":
"""Usage: chmod [options] [file]
          chmod [MODE] [file] \n
Description: The chmod command is used to change the permissions of a file or directory.
Options: 
    - +x: Adds executable permission.
    - -x: Removes executable permission.
    - +r: Adds read permission.
    - -r: Removes read permission.
    - +w: Adds write permission.
    - -w: Removes write permission.
Octal Modes:
    - 0: No permission.
    - 1: Execute permission.
    - 2: Write permission.
    - 3: Write and execute permissions.
    - 4: Read permission.
    - 5: Read and execute permissions.
    - 6: Read and write permissions.
    - 7: Read, write, and execute permissions. 
Examples:
    -Set specific permissions using octal representation: chmod 755 FILENAME.
    -Add executable permission for all users: chmod +x FILENAME.""",
		"clear":    
"""Usage: clear 
Description: Clears the terminal screen. """,
		"cp": 
"""Description: The cp command copies files or directories.
Usage: cp [source] [destination]
[source]: The file or directory to be copied.
[destination]: The location where the source will be copied.""",
		"exit": 
"""Description: The exit command is used to exit the shell.
Usage: exit""",
		"grep":
"""Description: The grep command searches for a pattern in files.
Usage: grep [pattern] [file]
[pattern]: The pattern to search for.
[file]: The file in which the pattern will be searched.""",
		"head": 
"""Description: Displays the beginning lines of a file.
Usage: head [file]""",
		"history":
"""Description: Displays a list of previously executed commands.
Usage: history""",
		"less": 
"""Description: Displays the content of a file one screen at a time.
Usage: less [file]""",
        "ls": 
"""Description: Lists files and directories in the current directory.
Flags:
    -l: Use a long listing format.
    -a: Include entries that begin with a dot (.).
    -h: Human-readable sizes (e.g., 1K, 234M, 2G).
Usage: ls [-l] [-a] [-h]""",

		"mkdir": 
"""Description: Creates a new directory.
Usage: mkdir [directory]""",
		"mv": 
"""Description: The mv command moves or renames files.
Usage: mv [source] [destination]
[source]: The file or directory to be moved.
[destination]: The destination location or new name.""",
		"pwd":
"""Description: Displays the current working directory.
Usage: pwd""" ,
		"rm":
"""Description: Removes files or directories.
Usage: remove [file]""" ,
		"sort":
"""Description: Sorts the contents of a file.
Usage: sort [file]""" ,
		"tail":
"""Description: Displays the ending lines of a file.
Usage: tail [file]""" ,
		"touch":
"""Description: Creates a new file.
Usage: touch [file]""",
		"wc":
"""Description: Displays the number of lines, words, and characters in a file.
Usage: wc [file]""" ,
		"who" : 
"""Description: Displays information about users who are currently logged in.
Usage: who""" 
,
		
}

shell_intro={"intro":
"""
Welcome to our custom Linux shell, a powerful and user-friendly interface designed to simplify your interactions with the system. 
Our shell offers a comprehensive set of commands that allow you to efficiently manage files, directories, and processes. 
Whether you're a beginner or an experienced user, our shell provides a seamless experience with intuitive commands and detailed help documentation. 
Navigate through your file system, manipulate files, and execute various tasks effortlessly using our reliable and versatile shell. 
Enjoy the convenience of a streamlined workflow and make the most of your Linux experience with our custom shell.

Commands and their format are mentioned as below:

cat [file1] [file2] ...
cd [directory]
chmod MODE FILE
clear
cp [source] [destination]
exit
grep [pattern] [file]
head [file]
history
less [file]
ls [-l] [-a] [-h]
mkdir [directory]
mv [source] [destination]
pwd
rm [file]
sort [file]
tail [file]
touch [file]
wc [file]
who

To know more about each command: <command> --help

"""

}

def help(command,output_dict):
    if command == "help":
        output_dict["output"] = shell_intro["intro"]
        output_dict["stdout"] = "[green] "+shell_intro["intro"]
    else:
        output_dict["output"] = help_cmd[command]
        output_dict["stdout"] = "[green] "+help_cmd[command]
    return output_dict
