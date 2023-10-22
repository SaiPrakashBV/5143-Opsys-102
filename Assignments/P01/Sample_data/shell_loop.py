import curses

curses.initscr()
curses.curs_set(0)  # Hide the cursor

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()

    user_input = ""
    
    while True:
        key = stdscr.getch()
        if key == ord('\n'):
            # Handle Enter key
            if user_input.lower() == "exit":
                break
            else:
                stdscr.addstr("\nYou entered: " + user_input)
                user_input = ""
        elif key == curses.KEY_BACKSPACE:
            # Handle Backspace key
            user_input = user_input[:-1]
            stdscr.addch(key)
            stdscr.delch()
        elif key >= 0 and key <= 127:
            # Handle other printable characters
            user_input += chr(key)
            stdscr.addch(key)
if "__name__" == "__main__":
    curses.wrapper(main)
