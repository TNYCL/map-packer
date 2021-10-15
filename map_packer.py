import tkinter as tk
import traceback
import sys
from tkinter import filedialog as fd
from colorama import Fore, Back, Style
import os
import ssl
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

# Project settings
root = tk.Tk()
root.withdraw()

VERSION = "0.1"
DEBUG = True

def success(message):
    print(Fore.GREEN + "+: " + Style.RESET_ALL + message + Fore.RESET)

def warning(message):
    print(Fore.YELLOW + "WARNING:" + Style.RESET_ALL + " " + message + Fore.RESET)

def warn(message):
    print(Fore.YELLOW + "+:" + Style.RESET_ALL + " " + message + Fore.RESET)

def err(message):
    print(Fore.RED + "+:" + Style.RESET_ALL + " " + message + Fore.RESET)

def error(message):
    print(Back.RED + Fore.BLACK + "ERROR:" +
          Fore.RED + Back.RESET + " " + message + Fore.RESET)

def message(message):
    print(Fore.LIGHTCYAN_EX + message)

def debug_traceback():
    if(DEBUG):
        track = traceback.format_exc()
        print(track)
        sys.exit(1)

def get_assets_folder():
    return os.path.join(os.getcwd(), "assets")

def get_file_path():
    return str(filepath)

def download_required(extract_to='./assets/settings'):
    settings_url = "https://cdn.tnycl.com/skin_packer/settings.zip"
    template_url = "https://cdn.tnycl.com/skin_packer/template.zip"

    settings_exist = os.path.exists(os.path.join(get_assets_folder(), "settings"))
    template_exist = os.path.exists(os.path.join(get_assets_folder(), "template"))

    if settings_exist == False:
        warning('Settings folder not exists, downloading.')
        try:
            context = ssl._create_unverified_context()
            http_response = urlopen(settings_url, context=context)

            message('Settings ZIP Exctracting...')
            zipfile = ZipFile(BytesIO(http_response.read()))
            zipfile.extractall(path=extract_to)
            message('Settings folder successfully created.')
        except Exception:
            error('There was a problem downloading the template folder.')
            return debug_traceback()
    if template_exist == False:
        warning('Template folder not exists, downloading.')
        try:
            context = ssl._create_unverified_context()
            http_response = urlopen(template_url, context=context)
            
            message('Template ZIP Exctracting...')
            zipfile = ZipFile(BytesIO(http_response.read()))
            zipfile.extractall(path='./assets/template')
            message('Template folder successfully created.')
        except Exception:
            error('There was a problem downloading the settings folder.')
            return debug_traceback()
    return True

def check_skin_pack():
    if os.path.exists(get_file_path(), "Content", "skin_pack"): return True
    return False

def check_folders():
    if os.path.exists(get_file_path(), "Content") == False:
        error('"Content" folder not found.')
    elif os.path.exists(get_file_path(), "Marketing Art") == False:
        error('"Marketing Art" folder not found.')
    elif os.path.exists(get_file_path(), "Store Art") == False:
        error('"Store Art" folder not found.')
    

def open_file_dialog():
    if(download_required()):
        global filepath
        message('Select folder needs to be packaged.')
        filepath = fd.askdirectory(title='Select Folder')
        if filepath != '' or filepath != None:
            success('Folder selected: Path => {path}'.format(path=str(filepath)))
            check_folders()
        else:
            error('File not selected.')

if __name__ == '__main__':
    message('Welcome to Map:Packer v.{}'.format(VERSION))
    open_file_dialog()
