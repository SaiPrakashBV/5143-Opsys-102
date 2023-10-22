"""
 
   _     _____ ____ ____     ____ ___  __  __ __  __    _    _   _ ____  
  | |   | ____/ ___/ ___|   / ___/ _ \|  \/  |  \/  |  / \  | \ | |  _ \ 
  | |   |  _| \___ \___ \  | |  | | | | |\/| | |\/| | / _ \ |  \| | | | |
  | |___| |___ ___) |__) | | |__| |_| | |  | | |  | |/ ___ \| |\  | |_| |
  |_____|_____|____/____/   \____\___/|_|  |_|_|  |_/_/   \_\_| \_|____/ 
                                                                         
 
"""

import curses,shutil
# width = shutil.get_terminal_size(fallback=(80, 24)).columns
def pager(stdscr, content):
    lines = content.split('\n')
    page_size = curses.LINES - 2  # Number of lines to display in one page
    num_pages = (len(lines) + page_size - 1) // page_size  # Calculate the total number of pages
    current_page = 0
    
    while True:
        stdscr.clear()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE)
        start = current_page * page_size
        end = start + page_size
        for i in range(start, min(end, len(lines))):
            stdscr.addstr(i - start, 0, lines[i])

        # Display page number and navigation instructions
        stdscr.addstr(curses.LINES - 1, 0, f"Page {current_page + 1}/{num_pages} | q to quit, use up/down arrows to move between pages")
        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord(' '):
            if current_page < num_pages - 1:
                current_page += 1
        elif key == curses.KEY_DOWN:
            if current_page < num_pages - 1:
                current_page += 1
        elif key == curses.KEY_UP:
            if current_page > 0:
                current_page -= 1



def less(command, shell_obj,output_dict,flag):
    content = ""
    if output_dict['output']:
        content = output_dict['output']
    else:
        for i in command['params']:
            if i:
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
                        # print(dir)
                        temp_dir = dir[0]
                    else:
                        exists = False
                if exists:
                    if temp_dir.metadata["File Type"] != "Directory":
                        content += temp_dir.file.read().decode()
    if flag:
        curses.wrapper(pager, content)
    else:
        output_dict["output"] = content
        output_dict["stdout"] = content 
    return output_dict 