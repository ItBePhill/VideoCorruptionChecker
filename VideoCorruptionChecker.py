import subprocess
import ast
import os
import configparser
command = "ffprobe -show_entries stream=r_frame_rate,nb_read_frames,duration -select_streams v -count_frames -of compact=p=1:nk=1 -threads <threads> -v 0 <file>"
config = configparser.ConfigParser()
config.read(f"{os.getcwd()}/config.ini")


folder = False 
folders = [] 
file = ""
ignore = [] 
threads = 1 


print(config.sections())


folder = ast.literal_eval(config.get("files", "Folder"))
if folder:
    folders = ast.literal_eval(config.get("files", "Folders"))
    ignore = ast.literal_eval(config.get("files", "Ignore"))
else:
    file = config.get("files", "File")

threads =  int(config.get("sys", "Threads"))

print(f"Folder: {folder}\nFolders: {folders}\nIgnore: {ignore}\nFile: {file}\nThreads: {threads}")
if not folder:
    print(command.replace("<threads>", str(threads)).replace("<file>", str(file)))
    print(subprocess.check_output(command.replace("<threads>", str(threads)).replace("<file>", str(file)), shell=True))




