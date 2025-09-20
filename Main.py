from Directory import Directory
from File import File

from datetime import datetime
import os
import shutil
import time

# TODO: pwd, date, cal (calendar), cp (-r), mv, help (h), find, tar
# TODO: for inputs that require more than 1 token --> If only 1 token is given, then say eg. Usage: rm [-rR] <dir/file>

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

running = True

curr_time = f"{datetime.now().strftime("%b")} {datetime.now().strftime("%d")} {datetime.now().strftime("%H")}:{datetime.now().strftime("%M")} {datetime.now().strftime("%S")} {datetime.now().strftime("%p")}"

def update_time():
    global curr_time
    curr_time = f"{datetime.now().strftime("%b")} {datetime.now().strftime("%d")} {datetime.now().strftime("%H")}:{datetime.now().strftime("%M")} {datetime.now().strftime("%S")} {datetime.now().strftime("%p")}"

os.system("cls")
# name = input("Name your home directory: ")
name = "home"
os.system("cls")

home = Directory(name) if name.isalpha() else Directory("home")
working_dir = home
os.mkdir(home.name)

### NOTE: Helper Functions ###

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
    global working_dir
    
    tokens = text.split(" ")
    
    ### NOTE: Main Functions ###
    
    def make_file(file_name, path=None):
        full_path = os.path.join(working_dir.name, file_name) if not path else path

        if not os.path.exists(full_path):
            open(full_path, "x")
            new_file = File(f"{working_dir.name}/{file_name}", working_dir, curr_time)
            working_dir.children.append(new_file)
        else:
            print(f"{file_name} file already exists")
    
    def open_file():
        for item in working_dir.children:
            if item.name == f"{working_dir.name}/{tokens[1]}":
                if isinstance(item, File):
                    with open(f"{item.name}") as f:
                        print(f.read())
                else:
                    print(f"{tokens[1]} is not a directory")
    
    ### NOTE: Parser Logic ###
    
    # NOTE: Make file
    if tokens[0] in ["touch", "t"]:
        if len(tokens) == 2:
            # Check if file extension was provided
            parts = tokens[1].split(".")
            if len(parts) == 2:
                make_file(tokens[1])
            elif len(parts) < 2:
                print("Please provide file extension (eg, .txt, .py)")
            else:
                print("Invalid file name (only 1 . allowed)")
    
    # NOTE: Open file
    if tokens[0] in ["nano", "n"]:
        if len(tokens) == 2:
            open_file()
            
    # NOTE: Make Directory
    if tokens[0] in ["mkdir", "mkd"]:
        if len(tokens) == 2:
            if not os.path.exists(f"{working_dir.name}/{tokens[1]}"):
                os.mkdir(f"{working_dir.name}/{tokens[1]}")
                new_dir = Directory(f"{working_dir.name}/{tokens[1]}", working_dir, curr_time)
                working_dir.children.append(new_dir)
            else:
                print(f"{tokens[1]} directory already exists")
    
    # NOTE: List Directory
    if tokens[0] == "ls":
        if len(tokens) == 1:
            if len(working_dir.children) > 0:
                for item in working_dir.children:
                    print(f"{get_dir_name(item)}\t", end="")
                print()
        elif len(tokens) == 2:
            if tokens[1] in ["-l", "-L"]:
                if len(working_dir.children) > 0:
                    for item in working_dir.children:
                        print(f"{get_dir_name(item)} : <{"DIR" if isinstance(item, Directory) else "FILE"}> [{item.time_made}]\t")
            elif tokens[1] in ["*", "**"]:
                if tokens[1] == "*":
                    if len(working_dir.children) > 0:
                        for item in working_dir.children:
                            print(f"{get_dir_name(item)}\t", end="")
                        print()
                elif tokens[1] == "**":
                    def rget_all_children(wd):
                        if len(wd.children) > 0:
                            for item in wd.children:
                                if isinstance(item, Directory):
                                    print(f"{get_dir_name(item)}\t", end="")
                                    rget_all_children(item)
                                else:
                                    print(f"{get_dir_name(item)}\t", end="")
                
                    rget_all_children(working_dir)
                    print()
    
    # NOTE: Change Directory
    if tokens[0] in ["cd", "cd.."]:
        if tokens[0] == "cd":
            if len(tokens) == 1:
                # Go to home directory
                working_dir = home
            elif len(tokens) == 2:
                # Go to parent directory
                if tokens[1] == "..":
                    if working_dir == home:
                        print("Already at home directory")
                    else:
                        working_dir = working_dir.parent
                else:
                    # Go to given directory
                    for item in working_dir.children:
                        if item.name == f"{working_dir.name}/{tokens[1]}":
                            if isinstance(item, Directory):
                                working_dir = item
                            else:
                                print(f"{tokens[1]} is not a directory")
        elif tokens[0] == "cd..":
            if working_dir == home:
                print("Already at home directory")
            else:
                working_dir = working_dir.parent
    
    # NOTE: Remove Directory / File
    if tokens[0] == "rm":
        if len(tokens) == 2:
            # Find and remove File
            found = False
            for item in working_dir.children:
                if isinstance(item, File):
                    if item.name == f"{working_dir.name}/{tokens[1]}":
                        remove_file(item.name)
                        
                        working_dir.children.remove(item)
                        found = True
                else:
                    if item.name == f"{working_dir.name}/{tokens[1]}":
                        print(f"{tokens[1]} is a directory. Please use the '-r' or '-R' alias")
                        found = True
            print("No such file or directory") if not found else None
        elif len(tokens) == 3:
            if tokens[1] in ["-r", "-R"]:
                # Find and remove Directory
                found = False
                for item in working_dir.children:
                    if item.name == f"{working_dir.name}/{tokens[2]}":
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

    # NOTE: Move Directory / File
    if tokens[0] == "mv":
        if len(tokens) == 3:
            target_name = tokens[1]
            dest_name = tokens[2]

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
    
# Main Loop
while running:
    x = input(BLUE + "PYT" + RESET + f" [C:/Users/{working_dir.name}] " + BLUE + ">" + RESET + " ")
    update_time()
    
    if x.lower() == "q":
        # os.system("cls")
        remove_dir("home")
        running = False
    elif x.lower() == "clear" or x.lower() == "cls":
        os.system("cls")
    else:
        Parser(x.strip())