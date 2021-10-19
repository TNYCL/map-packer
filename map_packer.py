import shutil
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

project_name = ''
filepath = ''

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

def download_assets(extract_to='./assets/settings'):
    settings_url = "https://cdn.tnycl.com/map_packer/settings.zip"
    template_url = "https://cdn.tnycl.com/map_packer/template.zip"

    settings_exist = os.path.exists(os.path.join(get_assets_folder(), "settings"))
    template_exist = os.path.exists(os.path.join(get_assets_folder(), "template"))

    if settings_exist == False:
        warn('World: settings folder not exists, downloading.')
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
        warn('World: template folder not exists, downloading.')
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

def check_world_folders():
    if os.path.exists(filepath + "/arts") == False:
        error('"arts" folder not exists.')
    if os.path.exists(filepath + "/arts/ingame") == False:
        error('"arts/ingame" folder not exists.')
    if os.path.exists(filepath + "/arts/keyart.png") == False:
        error('"arts/keyart.png" file not exists.')
    if os.path.exists(filepath + "/arts/thumbnail.jpg") == False:
        error('"arts/thumbnail.jpg" file not exists.')
    if os.path.exists(filepath + "/arts/partnerart.png") == False:
        error('"arts/partnert.png" file not exists.')
    if os.path.exists(filepath + "/world.zip") == False:
        error('"world.zip" file not exists.')

def build():
    project_path = os.getcwd() + '/projects/' + project_name + '/'

    try:
        shutil.copytree('assets/settings', project_path)
    except FileExistsError:
        error('This project already exists.')
    
    #copy world folder
    try:
        world_file = ZipFile(filepath + '/world.zip', 'r')
        message('World files are started to processing.')
        world_file.extractall(path=project_path + 'Content/world_template/')
        message('World files are successfully processed.')
    except Exception:
        error("World files couldn't be processed.")

    #copy skin folder
    has_skin_pack = os.path.exists(filepath + "/skins")
    message('Skin files are processing..')
    if has_skin_pack:
        shutil.copy(filepath + '/skins', project_path + 'Content/skin_pack/')


def select_file():
    if(download_assets()):
        message('Select folder needs to be packaged.')
        filepath = fd.askdirectory(title='Select Folder')
        if filepath != '':
            message('Folder selected: Path => {path}'.format(path=str(filepath)))
            build()
        else:
            error('File not selected.')

if __name__ == "__main__":
    message('Welcome to Map:Packer v.{}'.format(VERSION))
    project_name = input(Fore.GREEN+'Project Name'+Fore.RESET+': ')
    select_file()
