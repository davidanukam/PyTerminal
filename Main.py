from Directory import Directory
from File import File

from datetime import datetime
import os
import time

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

def Parser(text):
    global working_dir
    
    tokens = text.split(" ")
    
    def get_dir_name(dir):
        dir_tokens = dir.name.split("/")
        dir_name = dir_tokens[-1]
        return dir_name
    
    # TODO: pwd, date, cal (calendar), cp (-r), mv, help (h), find, tar
    # TODO: for inputs that require more than 1 token --> If only 1 token is given, then say eg. Usage: rm [-rR] <dir/file>
    
    # NOTE: Make file
    if tokens[0] in ["touch", "t"]:
        if len(tokens) == 2:
            new_file = File(f"{working_dir.name}/{tokens[1]}", working_dir, curr_time)
            working_dir.children.append(new_file)
    
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
                        print(f"{get_dir_name(item)} : <{"DIR" if type(item).__name__ == "Directory" else "FILE"}> [{item.time_made}]\t")
    
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
    
    # NOTE: Make Directory
    if tokens[0] in ["mkdir", "mkd"]:
        if len(tokens) == 2:
            new_dir = Directory(f"{working_dir.name}/{tokens[1]}", working_dir, curr_time)
            working_dir.children.append(new_dir)
    
    # NOTE: Remove Directory / File
    if tokens[0] == "rm":
        if len(tokens) == 2:
            # Find and remove File
            found = False
            for item in working_dir.children:
                if item.name == f"{working_dir.name}/{tokens[1]}":
                    if isinstance(item, File):
                        working_dir.children.remove(item)
                        found = True
                    else:
                        print(f"{tokens[1]} is a directory. Please use the '-r' or '-R' alias")
                        found = True
            print("No such file or directory") if not found else None
        elif len(tokens) == 3:
            if tokens[1] in ["-r", "-R"]:
                found = False
                for item in working_dir.children:
                    if item.name == f"{working_dir.name}/{tokens[2]}" and (isinstance(item, Directory) or isinstance(item, File)):
                        working_dir.children.remove(item)
                        found = True
                print("No such file or directory") if not found else None
    
# Main Loop
while running:
    x = input(BLUE + "PYT" + RESET + f" [C:/Users/{working_dir.name}] " + BLUE + ">" + RESET + " ")
    update_time()
    
    if x.lower() == "q":
        # os.system("cls")
        running = False
    elif x.lower() == "clear" or x.lower() == "cls":
        os.system("cls")
    elif x.lower() == "m":
        print(f"[]")
    else:
        Parser(x.strip())