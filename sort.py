import os
import re
import shutil
import sys


def normalize(name):

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    new_name = name.translate(TRANS)

    new_name = re.sub('[^a-zA-Z0-9 \n\.]', '_', new_name)

    return new_name


basepath = os.path.abspath(sys.argv[1])

img_ext = ['.jpeg', '.png', '.jpg', '.svg']
doc_ext = ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']
aud_ext = ['.mp3', '.ogg', '.wav', '.amr']
vid_ext = ['.avi', '.mp4', '.mov', '.mkv']
arc_ext = ['.zip', '.gz', '.tar']

if not os.path.exists(basepath + '/Images'):
    os.mkdir(basepath + '/Images')
if not os.path.exists(basepath + '/Documents'):
    os.mkdir(basepath + '/Documents')
if not os.path.exists(basepath + '/Audio'):
    os.mkdir(basepath + '/Audio')
if not os.path.exists(basepath + '/Video'):
    os.mkdir(basepath + '/Video')
if not os.path.exists(basepath + '/Archives'):
    os.mkdir(basepath + '/Archives')

for root, dirs, files in os.walk(basepath, topdown=False):
    for dir in dirs:
        os.rename(os.path.join(root, dir), os.path.join(root, normalize(dir)))

for root, dirs, files in os.walk(basepath):
    for file in files:
        if os.path.splitext(file)[1].lower() in img_ext:
            os.replace(f'{root}/{file}',
                       f'{basepath}/Images/{normalize(file)}')
        elif os.path.splitext(file)[1].lower() in doc_ext:
            os.replace(f'{root}/{file}',
                       f'{basepath}/Documents/{normalize(file)}')
        elif os.path.splitext(file)[1].lower() in aud_ext:
            os.replace(f'{root}/{file}', f'{basepath}/Audio/{normalize(file)}')
        elif os.path.splitext(file)[1].lower() in vid_ext:
            os.replace(f'{root}/{file}', f'{basepath}/Video/{normalize(file)}')
        elif os.path.splitext(file)[1].lower() in arc_ext:
            shutil.unpack_archive(
                f'{root}/{file}', f'{basepath}/Archives/{os.path.splitext(normalize(file))[0]}')

for root, dirs, files in os.walk(basepath, topdown=False):
    if not dirs and not files:
        os.rmdir(root)
