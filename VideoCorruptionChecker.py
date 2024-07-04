import subprocess
import ast
import os
import configparser
good = []
corrupted = []
video_extensions = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng', 'mov', 'avi', 'qt', 'wmv', 'yuv', 'rm', 'asf', 'amv', 'mp4', 'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b', 'mod']
def RunFFmpeg(f):
    global good, corrupted
    print(f"Checking File: {os.path.basename(f)}")
    try:
        output = str(subprocess.check_output(command.replace("<threads>", str(threads)).replace("<file>", f'"{str(f)}"'), stderr=subprocess.STDOUT))
    except Exception as e:
        print(f"Something Went Wrong!: {e}")
        output = ""
    if output != "b''":
        print(f"File is Corrupted!")
        corrupted.append(f)
    else:
        print(f"File is Good!")
        good.append(f)

command = "ffprobe.exe -loglevel error -threads <threads> -i <file>"
config = configparser.ConfigParser()
config.read(f"{os.getcwd()}/config.ini")
total = 0
folder = False 
folders = [] 
file = ""
ignore = [] 
threads = 1 
stats = []


folder = ast.literal_eval(config.get("files", "Folder"))
if folder:
    folders = ast.literal_eval(config.get("files", "Folders"))
    ignore = ast.literal_eval(config.get("files", "Ignore"))
else:
    file = config.get("files", "File")

threads =  int(config.get("sys", "Threads"))

print(f"Folder: {folder}\nFolders: {folders}\nIgnore: {ignore}\nFile: {file}\nThreads: {threads}\n\nChecking Folder")


if not folder:
    RunFFmpeg(file)
else:
    for i in folders:
        print(f"Checking Folder: {os.path.basename(i)}")
        for j in os.listdir(i):
            if os.path.isfile(f"{i}\\{j}"):
                if str(os.path.splitext(j)[1]).removeprefix(".") in video_extensions:
                    RunFFmpeg(f"{i}\\{j}")
        stats.append(f"Good: {len(good)} | Bad: {len(corrupted)} | Total: {len(good)+len(corrupted)}")
    try:
        os.remove("corrupted.txt")
    except Exception as e:
        print(e)

    for i in corrupted:
        with open("corrupted.txt", "a+") as f:
            f.write(f"{i}\n")
    for i in stats:
        print(i)

    input("Press Any Key to Continue...")    
    stats = []
    good = []
    corrupted = []



