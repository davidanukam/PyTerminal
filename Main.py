from Directory import Directory
from File import File

from datetime import datetime
import os, shutil, calendar, copy, time

# TODO: help (h), find, tar
# TODO: for inputs that require more than 1 token --> If only 1 token is given, then say eg. Usage: rm [-rR] <dir/file>

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

running = True

curr_time = f"{datetime.now().strftime("%b")} {datetime.now().strftime("%d")} {datetime.now().strftime("%H")}:{datetime.now().strftime("%M")}:{datetime.now().strftime("%S")} {datetime.now().strftime("%p")}"

def update_time():
    global curr_time
    curr_time = f"{datetime.now().strftime("%b")} {datetime.now().strftime("%d")} {datetime.now().strftime("%H")}:{datetime.now().strftime("%M")}:{datetime.now().strftime("%S")} {datetime.now().strftime("%p")}"

os.system("cls")
# name = input("Name your home directory: ")
name = "home"
os.system("cls")

home = Directory(name) if name.isalpha() else Directory("home")
working_dir = home
if not os.path.exists("home"):
    os.mkdir(home.name)

### INFO: Helper Functions ###

def get_dir_name(dir):
    dir_tokens = dir.name.split("/")
    dir_name = dir_tokens[-1]
    return dir_name

def remove_dir(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    os.removedirs(folder_path)

def remove_file(file_path):
    os.remove(file_path)
    
def Parser(text):
    global running
    
    tokens = text.split(" ")
    command = tokens[0].lower()
    args = tokens[1:]
    
    ### INFO: Main Functions ###
    
    def make_file(file_name, path=None):
        global working_dir
        full_path = os.path.join(working_dir.name, file_name) if not path else path

        if not os.path.exists(full_path):
            open(full_path, "x")
            new_file = File(f"{working_dir.name}/{file_name}", working_dir, curr_time)
            working_dir.children.append(new_file)
        else:
            print(f"{file_name} file already exists")
    
    ### INFO: Parser Logic ###
    
    # NOTE: Print Working Directory
    def handle_pwd(args):
        global working_dir
        if not args:
            print(f"{get_dir_name(working_dir)}\t")
            
    # NOTE: Print Date
    def handle_date(args):
        print(f"{datetime.now().strftime("%a")} {datetime.now().strftime("%b")} {datetime.now().strftime("%d")} {datetime.now().strftime("%Y")} {datetime.now().strftime("%H")}:{datetime.now().strftime("%M")}:{datetime.now().strftime("%S")} {datetime.now().strftime("%p")}")
        
    # NOTE: Print Calendar
    def handle_cal(args):
        cal = calendar.TextCalendar(calendar.SUNDAY)
        print(cal.formatmonth(int(datetime.now().strftime("%Y")), int(datetime.now().strftime("%m")[1]) if datetime.now().strftime("%m")[0] != 1 else int(datetime.now().strftime("%m"))))
        
    # NOTE: Make File
    def handle_touch(args):
        global working_dir
        if len(tokens) == 2:
            # Check if file extension was provided
            parts = args[0].split(".")
            if len(parts) == 2:
                make_file(args[0])
            elif len(parts) < 2:
                print("Please provide file extension (eg, .txt, .py)")
            else:
                print("Invalid file name (only 1 . allowed)")
    
    # NOTE: Open file
    def handle_nano(args):
        if len(args) == 1:
            for item in working_dir.children:
                if item.name == f"{working_dir.name}/{args[0]}":
                    if isinstance(item, File):
                        with open(f"{item.name}") as f:
                            print(f.read())
                    else:
                        print(f"{args[0]} is not a directory")
    
    # NOTE: List Directory / File
    def handle_ls(args):
        global working_dir
        if not args:
            if len(working_dir.children) > 0:
                for item in working_dir.children:
                    print(f"{get_dir_name(item)}\t", end="")
                print()
            
        elif args[0] in ["-l", "-L"]:
            if len(working_dir.children) > 0:
                for item in working_dir.children:
                    print(f"{get_dir_name(item)} : <{"DIR" if isinstance(item, Directory) else "FILE"}> [{item.time_made}]\t")

        elif args[0] == "*":
            if len(working_dir.children) > 0:
                for item in working_dir.children:
                    print(f"{get_dir_name(item)}\t", end="")
                print()
        
        elif args[0] == "**":
            def rget_all_children(wd):
                if len(wd.children) > 0:
                    for item in wd.children:
                        if isinstance(item, Directory):
                            print(f"{get_dir_name(item)}\t", end="")
                            rget_all_children(item)
                        else:
                            print(f"{get_dir_name(item)}\t", end="")
            if len(working_dir.children) > 0:
                rget_all_children(working_dir)
                print()

    # NOTE: Make Directory
    def handle_mkdir(args):
        global working_dir
        if len(args) == 1:
            if not os.path.exists(f"{working_dir.name}/{args[0]}"):
                os.mkdir(f"{working_dir.name}/{args[0]}")
                new_dir = Directory(f"{working_dir.name}/{args[0]}", working_dir, curr_time)
                working_dir.children.append(new_dir)
            else:
                print(f"{args[0]} directory already exists")
        else:
            print("Usage: mkdir/mkd <directory_name>")

    # NOTE: Remove Directory / File
    def handle_rm(args):
        global working_dir
        if not args:
            print("Usage: rmdir/rm [-r/-R] <directory_name/file_name>")
        if len(args) == 1:
            # Find and remove File
            found = False
            for item in working_dir.children:
                if isinstance(item, File):
                    if item.name == f"{working_dir.name}/{args[0]}":
                        remove_file(item.name)
                        
                        working_dir.children.remove(item)
                        found = True
                else:
                    if item.name == f"{working_dir.name}/{args[0]}":
                        print(f"{tokens[1]} is a directory. Please use the '-r' or '-R' alias")
                        found = True
            print("No such file or directory") if not found else None
        elif len(args) == 2:
            if args[0] in ["-r", "-R"]:
                # Find and remove Directory or File
                found = False
                for item in working_dir.children:
                    if item.name == f"{working_dir.name}/{args[1]}":
                        if isinstance(item, Directory):
                            remove_dir(item.name)
                        else:
                            remove_file(item.name)
                        
                        working_dir.children.remove(item)
                        
                        # Check if home Directory still exists -> Make a new one if it does NOT exist
                        if not os.path.exists("home"):
                            os.mkdir("home")
                            
                        found = True
                print("No such file or directory") if not found else None
    
    # NOTE: Change Directory
    def handle_cd(args):
        global working_dir
        if not args:
            if command == "cd":
                working_dir = home
            elif command == "cd..":
                if working_dir == home:
                    print("Already at home directory")
                else:
                    working_dir = working_dir.parent
        elif args[0] == "..":
            if working_dir == home:
                print("Already at home directory")
            else:
                working_dir = working_dir.parent
        elif args and command != "cd..":
            # Try to go to given directory
            for item in working_dir.children:
                if item.name == f"{working_dir.name}/{args[0]}":
                    if isinstance(item, Directory):
                        working_dir = item
                    else:
                        print(f"{args[0]} is not a directory")
        else:
            print("Usage: cd <directory_name>")
    
    # NOTE: Move Directory / File
    def handle_mv(args):
        global working_dir
        if len(args) == 2:
            target_name = args[0]
            dest_name = args[1]

            target_path = os.path.join(working_dir.name, target_name)
            dest_path = os.path.join(working_dir.name, dest_name)

            if not os.path.exists(target_path):
                print(f"No such file or directory: {target_name}")
                return None

            if not os.path.isdir(dest_path):
                print(f"{dest_name} is not a directory. Destination must be a directory.")
                return None

            try:
                # Check if the destination already contains an item with the same name
                final_path = os.path.join(dest_path, target_name)
                if os.path.exists(final_path):
                    print(f"{target_name} already exists in {dest_name}.")
                    return None

                shutil.move(target_path, dest_path)

                # Now, update the internal data structures
                moved_item = None
                for i, item in enumerate(working_dir.children):
                    if get_dir_name(item) == target_name:
                        moved_item = working_dir.children.pop(i)
                        break

                if moved_item:
                    # Find the destination Directory object
                    dest_dir_obj = None
                    for item in working_dir.children:
                        if get_dir_name(item) == dest_name:
                            dest_dir_obj = item
                            break
                        
                    if dest_dir_obj:
                        # Update the moved item's name and parent
                        moved_item.name = f"{dest_dir_obj.name}/{target_name}"
                        moved_item.parent = dest_dir_obj
                        dest_dir_obj.children.append(moved_item)
                    else:
                        print("Error: Destination directory object not found.")
                else:
                    print("Error: Item to be moved not found in current directory's children.")
            except Exception as e:
                print(f"Error moving file/directory: {e}")
        else:
            print("Usage: mv <source> <destination>")
    
    # NOTE: Copy Directory / File
    def handle_cp(args):
        global working_dir
        if len(args) == 2:
            target_name = args[0]
            dest_name = args[1]
            
            target_path = os.path.join(working_dir.name, target_name)
            dest_path = os.path.join(working_dir.name, dest_name)

            if not os.path.exists(target_path):
                print(f"No such file or directory: {target_name}")
                return None

            if not os.path.isdir(dest_path):
                print(f"{dest_name} is not a directory. Destination must be a directory.")
                return None

            try:
                # Check if the destination already contains an item with the same name
                final_path = os.path.join(dest_path, target_name)
                if os.path.exists(final_path):
                    print(f"{target_name} already exists in {dest_name}.")
                    return None

                shutil.copy(target_path, dest_path)

                # Now, update the internal data structures
                copied_item = None
                for i, item in enumerate(working_dir.children):
                    if get_dir_name(item) == target_name:
                        copied_item = copy.deepcopy(working_dir.children[i])
                        break

                if copied_item:
                    # Find the destination Directory object
                    dest_dir_obj = None
                    for item in working_dir.children:
                        if get_dir_name(item) == dest_name:
                            dest_dir_obj = item
                            break
                        
                    if dest_dir_obj:
                        # Update the copied item's name and parent
                        copied_item.name = f"{dest_dir_obj.name}/{target_name}"
                        copied_item.parent = dest_dir_obj
                        dest_dir_obj.children.append(copied_item)
                    else:
                        print("Error: Destination directory object not found.")
                else:
                    print("Error: Item to be moved not found in current directory's children.")
            except Exception as e:
                print(f"Error moving file/directory: {e}")
        else:
            print("Usage: mv <source> <destination>")
    
    def handle_help(args):
        print("For more information on a specific command, type: help <command-name>")
        past_func = None
        for command, function in commands.items():
            if function != past_func:
                print("")
                past_func = function
            print(command)
    
    commands = {
        "pwd": handle_pwd,
        
        "help": handle_help,
        "h": handle_help,
        
        "date": handle_date,
        "cal" : handle_cal,
        
        "ls": handle_ls,
        
        "cd": handle_cd,
        "cd..": handle_cd,
        
        "touch": handle_touch,
        "t": handle_touch,
        
        "mkdir": handle_mkdir,
        "mkd": handle_mkdir,
        
        "rmdir": handle_rm,
        "rm": handle_rm,
        
        "mv": handle_mv,
        "cp": handle_cp,
        
        "nano": handle_nano,
        "n": handle_nano,
    }
    
    if command in commands:
        commands[command](args)
    elif command in ['q', "clear", "cls", "c"]:
        if command == 'q':
            running = False
            remove_dir("home")
        else:
            os.system("cls")
    else:
        print(f"Unknown command: {command}")
    
# Main Loop
while running:
    x = input(BLUE + "PYT" + RESET + f" [C:/Users/{working_dir.name}] " + BLUE + ">" + RESET + " ")
    update_time()
    Parser(x.strip())