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

def check_folders():
    if os.path.exists(filepath + "/arts") == False:
        error('"arts" folder not exists.')
    elif os.path.exists(filepath + "/arts/ingame") == False:
        error('"arts/ingame" folder not exists.')
    elif os.path.exists(filepath + "/arts/ingame/panorama.jpg") == False:
        error('"arts/ingame/panorama.jpg" file not exists.')
    elif os.path.exists(filepath + "/arts/ingame/packicon.jpg") == False:
        error('"arts/ingame/packicon.jpg" file not exists.')
    elif os.path.exists(filepath + "/arts/keyart.png") == False:
        error('"arts/keyart.png" file not exists.')
    elif os.path.exists(filepath + "/arts/thumbnail.jpg") == False:
        error('"arts/thumbnail.jpg" file not exists.')
    elif os.path.exists(filepath + "/arts/partnerart.png") == False:
        error('"arts/partnerart.png" file not exists.')
    elif os.path.exists(filepath + "/world.zip") == False:
        error('"world.zip" file not exists.')
    else:
        build_project()

def build_project():
    project_path = os.getcwd() + '/projects/' + project_name + '/'

    try:
        shutil.copytree('assets/settings', project_path)
    except FileExistsError:
        error('This project already exists.')
        sys.exit(1)

    #world folder
    try:
        world_file = ZipFile(filepath + '/world.zip', 'r')
        world_file.extractall(path=project_path + 'Content/world_template/')
        message('World files are successfully processed.')
    except Exception:
        error("World files couldn't be processed.")
    worldtemplate_path = project_path + "Content/world_template/"
    
    #skin folder
    has_skin_pack = os.path.exists(filepath + "/skins")
    if has_skin_pack:
        try:
            shutil.copytree(filepath + '/skins', project_path + 'Content/skin_pack/', dirs_exist_ok=True)
            message('Skin files are successfully processed.')
        except Exception as ex:
            error(ex)
    
    #marketing art
    photo_count = 0
    marketingart_path = project_path + "Marketing Art/"
    for file in os.listdir(filepath + '/arts/ingame'):
        if file == "packicon.jpg": continue
        if file == "panorama.jpg": continue
        shutil.copy(filepath + "/arts/ingame/" + file, marketingart_path + project_name + "_MarketingScreenshot_" + str(photo_count) + ".jpg")
        photo_count+=1
    shutil.copy(filepath + "/arts/keyart.png", marketingart_path + project_name + "_MarketingKeyArt.png")
    shutil.copy(filepath + "/arts/partnerart.png", marketingart_path + project_name + "_MarketingPartnerArt.png")

    #store art
    photo_count = 0
    storeart_path = project_path + "Store Art/"
    for file in os.listdir(filepath + '/arts/ingame'):
        if file == "packicon.jpg":
            shutil.copy(filepath + "/arts/ingame/" + file, storeart_path)
            os.rename(project_path + "Store Art/" + file, storeart_path + project_name + "_packicont_0.jpg")
            continue
        if file == "panorama.jpg":
            shutil.copy(filepath + "/arts/ingame/" + file, storeart_path)
            os.rename(project_path + "Store Art/" + file, storeart_path + project_name + "_panorama_0.jpg")
            continue
        shutil.copy(filepath + "/arts/ingame/" + file, storeart_path)
        os.rename(project_path + "Store Art/" + file, storeart_path + project_name + "_MarketingScreenshot_" + str(photo_count) + ".jpg")
        photo_count+=1
    shutil.copy(filepath + "/arts/thumbnail.jpg", storeart_path)
    os.rename(project_path + "Store Art/thumbnail.jpg", storeart_path + project_name + "_Thumbnail_0.jpg")

def select_file():
    if(download_assets()):
        message('Select folder needs to be packaged.')
        global filepath
        filepath = fd.askdirectory(title='Select Folder')
        if filepath != '':
            message('Folder selected: Path => {path}'.format(path=str(filepath)))
            check_folders()
        else:
            error('File not selected.')

if __name__ == "__main__":
    message('Welcome to Map:Packer v.{}'.format(VERSION))
    global project_name
    global shorted_project_name
    project_name = input(Fore.GREEN+'Normal Project Name'+Fore.RESET+': ')
    shorted_project_name = input(Fore.GREEN+'Shorted Project Name'+Fore.RESET+': ')
    project_name.replace(" ", "")
    select_file()
