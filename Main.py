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
            target = tokens[1]
            target_root, target_ext = os.path.splitext(target)
            dest = tokens[2]
            dest_root, dest_ext = os.path.splitext(dest)
            
            dest_item = None
            dest_path = f"{working_dir.name}"
            valid_dest = False
            
            for item in working_dir.children:
                item_name_root, item_name_ext = os.path.splitext(item.name)
                if item_name_root == f"{working_dir.name}/{dest_root}":
                    if isinstance(item, File):
                        print(f"{dest_root} is a File. Destination must be a Directory")
                    else:
                        valid_dest = True
                        dest_item = item
                        dest_path = f"{working_dir.name}/{dest_root}"
            
            # Move to dest Directory
            if valid_dest:
                for item in working_dir.children:
                    item_name_root, item_name_ext = os.path.splitext(item.name)
                    item_name_tokens = item_name_root.split("/")
                    if item_name_root == f"{working_dir.name}/{target_root}":
                        new_name = ""
                        if isinstance(item, File):
                            new_name = f"{dest_path}/{item_name_tokens[-1]}{item_name_ext}"
                        else:
                            new_name = f"{dest_path}/{item_name_tokens[-1]}"
                        
                        # Check if an item of the same name exists in new Directory
                        valid_move = True
                        for elem in dest_item.children:
                            if elem.name == new_name:
                                print(f"{item_name_tokens[-1]}{item_name_ext} already exists in {dest_path}")
                                valid_move = False
                                break
                        
                        if valid_move:
                            # Remove from old Directory
                            working_dir.children.remove(item)
                            
                            print(item)
                            for dex, thing in enumerate(working_dir.children):
                                print(dex+1, thing, thing.name)
                            
                            #print(f"removed {item.name} from children")
                            if isinstance(item, File):
                                os.remove(f"{item.name}")
                                #print("removed file")
                            else:
                                remove_dir(item.name)
                                #print("removed dir")
                            
                            # Update item path
                            item.name = new_name
                            
                            # Add to new Directory
                            dest_item.children.append(item)
                            
                            if isinstance(item, File):
                                make_file(f"{item_name_tokens[-1]}{item_name_ext}", item.name)
                            else:
                                os.mkdir(item.name)
                            
                            print(f"Moved {item_name_tokens[-1]}{item_name_ext} from {working_dir.name} to {dest_path}")
                            break
    
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