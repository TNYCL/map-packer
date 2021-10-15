import shutil
import json
import os
import uuid
import codecs
import map_packer as main

class Create:
    def __init__(self):
        self.path = os.getcwd() + '/projects/' + main.project_name + '/Content'

    def copyfile(self):
        try:
            shutil.copytree('assets/skin/settings', self.path)
        except FileExistsError:
            main.error('This project already created.')

createdpath = Create().path
skinpath = createdpath + 'Content/skin_pack/'

def manifest():
    try:
        manifest = createdpath + 'Content/skin_pack/manifest.json'
        with open(manifest) as file:
            data = json.load(file)
            header = uuid.uuid4()
            modules = uuid.uuid4()
            data['header']['uuid'] = str(header)
            data['modules'][0]['uuid'] = str(modules)
            json.dump(data, open(manifest, 'w'), indent=4)
    except:
        main.error("manifest.json files couldn't be processed.")

def text_pname():
    try:
        text = skinpath + 'texts/en_US.lang'
        with codecs.open(text, 'a', 'utf-8') as file:
            data = file
            data.write('skinpack.CR={}\n'.format(main.project_name))
            data.close()
    except:
        main.error("texts/en_US.lang(Project Name) files couldn't be processed.")

def text_skin(name):
    try:
        text = skinpath + 'texts/en_US.lang'
        with codecs.open(text, 'a', 'utf-8') as file:
            data = file
            data.write('skin.CR.{}={}\n'.format(name, name))
            data.close()
    except:
        main.error("texts/en_US.lang(Skin) files couldn't be processed.")

def jsonparse_skin(name, geometry, texture, type):
    try:
        manifest = createdpath + 'Content/skin_pack/skins.json'
        with open(manifest) as file:
            data = json.load(file)
            data['skins'].append({"localization_name": name, "geometry": geometry, "texture": texture, "type": type})
            json.dump(data, open(manifest, 'w'), indent=4)
    except:
        main.error("skins.json couldn't be processed.")

def getskincount(): return len(steve) + len(slim)

def createproject():
    manifest()
    text_pname()

def build():
    global directory
    directory = main.filepath + '/skin/{}'
    if os.path.exists(directory.format('/skins')) == False:
        main.error('"skins" folder not exists.')
    elif os.path.exists(directory.format('/skins/slim')) == False:
        main.error('"skins/slim" folder not exists.')
    elif os.path.exists(directory.format('/skins/slim/free')) == False:
        main.error('"skins/slim/free" folder not exists.')
    elif os.path.exists(directory.format('/skins/slim/paid')) == False:
        main.error('"skins/slim/paid" folder not exists.')
    elif os.path.exists(directory.format('/skins/steve')) == False:
        main.error('"skins/steve" folder not exists.')
    elif os.path.exists(directory.format('/skins/steve/free')) == False:
        main.error('"skins/steve/free" folder not exists.')
    elif os.path.exists(directory.format('/skins/steve/paid')) == False:
        main.error('"skins/steve/paid" folder not exists.')
    else:
        main.message('Skin folder are verified, progressing.')
        global createdfile
        global skinfolder
        createdfile = Create()
        createdfile.copyfile()
        skinfolder = createdfile.path  + 'Content/skin_pack'
        steve()
        slim()
        main.message('{} skin included.'.format(getskincount()))
        createproject()
        main.success('Skin pack has been successfully packaged.'.format(main.project_name))

def slim(names=[]):
    free = directory.format('/Skins/Slim/Free')
    paid = directory.format('/Skins/Slim/Paid')
    for name in os.listdir(free):
        realname = name.replace('.png', '')
        names.append(realname)
        shutil.copy(free + '/' + name, skinfolder)
        os.rename(skinfolder + '/' + name, skinfolder + '/' + realname + '_customSlim.png')
        text_skin(realname)
        jsonparse_skin(realname, 'geometry.humanoid.customSlim', realname + '_customSlim.png', 'free')
        main.success('Including (Slim -> Free): {}'.format(realname))
    for name in os.listdir(paid):
        realname = name.replace('.png', '')
        names.append(realname)
        shutil.copy(paid + '/' + name, skinfolder)
        os.rename(skinfolder + '/' + name, skinfolder + '/' + realname + '_customSlim.png')
        text_skin(realname)
        jsonparse_skin(realname, 'geometry.humanoid.customSlim', realname + '_customSlim.png', 'paid')
        main.success('Including (Slim -> Paid): {}'.format(realname))
    return names

def steve(names=[]):
    free = directory.format('/Skins/Steve/Free')
    paid = directory.format('/Skins/Steve/Paid')
    for name in os.listdir(free):
        realname = name.replace('.png', '')
        names.append(realname)
        shutil.copy(free + '/' + name, skinfolder)
        os.rename(skinfolder + '/' + name, skinfolder + '/' + realname + '_custom.png')
        text_skin(realname)
        jsonparse_skin(realname, 'geometry.humanoid.custom', realname + '_custom.png', 'free')
        main.success('Including (Steve -> Free): {}'.format(realname))
    for name in os.listdir(paid):
        realname = name.replace('.png', '')
        names.append(realname)
        shutil.copy(paid + '/' + name, skinfolder)
        os.rename(skinfolder + '/' + name, skinfolder + '/' + realname + '_custom.png')
        text_skin(realname)
        jsonparse_skin(realname, 'geometry.humanoid.custom', realname + '_custom.png', 'paid')
        main.success('Including (Steve -> Paid): {}'.format(realname))
    return names

