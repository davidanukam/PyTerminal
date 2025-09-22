from Directory import Directory
from File import File

from datetime import datetime
import os
import shutil
import time

# TODO: pwd, date, cal (calendar), cp (-r), help (h), find, tar
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
    
    def open_file(args):
        global working_dir
        for item in working_dir.children:
            if item.name == f"{working_dir.name}/{tokens[1]}":
                if isinstance(item, File):
                    with open(f"{item.name}") as f:
                        print(f.read())
                else:
                    print(f"{args[0]} is not a directory")
    
    ### INFO: Parser Logic ###
    
    # NOTE: Make file
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
    
    # NOTE: List Directory
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
    
    commands = {
        "ls": handle_ls,
        
        "mkdir": handle_mkdir,
        "mkd": handle_mkdir,
        
        "cd": handle_cd,
        "cd..": handle_cd,
        
        "touch": handle_touch,
        "t": handle_touch,
        
        # 'rm': handle_rm,
    }
    
    if command in commands:
        commands[command](args)
    elif command in ['q', 'clear', 'cls']:
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