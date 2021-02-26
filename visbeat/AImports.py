# AImports
from . import ADefines as defines
import os
import os.path
import errno
import json
import glob
import subprocess
from operator import truediv
import shutil
import time
from time import gmtime, strftime, localtime
import random
from . import fileui
from pathlib import Path

try:
    from termcolor import colored

    def AWARN(message):
        if defines.AD_DEBUG:
            print(colored(message, "red"))

    def AINFORM(message):
        if defines.AD_DEBUG:
            print(colored(message, "blue"))


except ImportError:
    if defines.AD_DEBUG:
        print(
            "You do not have termcolor installed (pip install termcolor). AWARN will just show as plain print statements when defines.AD_DEBUG==True..."
        )

    def AWARN(message):
        if defines.AD_DEBUG:
            print(message)

    def AINFORM(message):
        if defines.AD_DEBUG:
            print(message)


def local_time_string():
    return strftime("%Y-%m-%d_%H:%M:%S", localtime())


def get_temp_file_path(final_file_path="TEMP", temp_dir_path=None):
    final_file_path = Path(final_file_path)
    destfolder = final_file_path.parent
    tempdir = Path(temp_dir_path)
    if tempdir is None:
        tempdir = Path(".")

    tempname = f"TEMP_{final_file_path.name}"
    temptry = 0
    while os.path.isfile(tempdir / tempname):
        temptry = temptry + 1
        tempname = f"TEMP{temptry}_{final_file_path.name}"
    return tempdir / tempname


def runningInNotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def getshellname():
    try:
        shell = get_ipython().__class__.__name__
        return shell
    except NameError:
        return False  # Probably standard Python interpreter


def runningInSpyder():
    return "SpyderKernel" in str(get_ipython().kernel.__class__)


def pickleToPath(d, path):
    # assert(False)
    print("pickling")
    f = open(path, "wb")
    pickle.dump(d, f, protocol=2)
    f.close()
    return True


def unpickleFromPath(path):
    f = open(path, "rb")
    d = pickle.load(f)
    f.close()
    return d


def make_sure_path_exists(path):
    os.makedirs(path, exist_ok=True)


def make_sure_dir_exists(path):
    p = Path(path)
    os.makedirs(p.parent, exist_ok=True)


def safe_file_name(input_string):
    return "".join([i if ord(i) < 128 else "_" for i in input_string])


def pathstring(path):
    return path.replace(os.sep + os.sep, os.sep)


def is_interactive():
    import __main__ as main

    return not hasattr(main, "__file__")


def printOb(obj):
    for attr in dir(obj):
        print("#### Obj.{} = {}\n".format(attr, getattr(obj, attr)))


# def get_prepended_name_file_path(original_file_path, string_to_prepend):
#     pparts = os.path.split(original_file_path)
#     destfolder = pparts[0] + os.sep
#     pname = string_to_prepend + pparts[1]
#     return pathstring(destfolder + pname)


def safe_file_name(input_string):
    return "".join([i if ord(i) < 128 else "_" for i in input_string])


def change_extension(input_path, new_ext):
    nameparts = os.path.splitext(input_path)
    return nameparts[0] + new_ext


def printDictionary(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, "__iter__"):
                print(k)
                printDictionary(v)
            else:
                print("{} : {}").format(k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, "__iter__"):
                printDictionary(v)
            else:
                print(v)
    else:
        print(obj)


def spotgt_shift_bit_length(x):
    # smallest power of two greater than
    return 1 << (x - 1).bit_length()


def get_file_name_from_path(pth):
    return os.path.split(pth)[1]


def get_dir_from_path(pth):
    return os.path.split(pth)[0] + os.sep


def get_file_names_from_paths(pths):
    r = []
    for p in pths:
        r.append(get_file_name_from_path(p))
    return r


def writeDictionaryToJSON(d, json_path=None):
    if json_path:
        with open(json_path, "w") as outfile:
            json.dump(d, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def vtt_to_srt(fileContents):
    replacement = re.sub(r"([\d]+)\.([\d]+)", r"\1,\2", fileContents)
    replacement = re.sub(r"WEBVTT\n\n", "", replacement)
    replacement = re.sub(r"^\d+\n", "", replacement)
    replacement = re.sub(r"\n\d+\n", "\n", replacement)
    return replacement
