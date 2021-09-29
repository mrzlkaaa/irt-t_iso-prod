from PIL import Image
import os
import random, string
import re

cwd = os.getcwd()
shape_folder = 'circles'
dir_files = os.listdir(cwd)
print(dir_files)

# navigate to shape folder
folder_path = os.path.join(cwd, shape_folder)
#loop in folders
os.chdir(folder_path)
new_dir = os.getcwd()
files = os.listdir(folder_path)
for i in files:
    print('+')
    imgs_path = os.path.join(new_dir, i)
    imgs_list = [i for i in os.listdir(imgs_path) if re.search(r'\.jpeg', i) is not None]
    if len(imgs_list) < 800:
        for j in imgs_list:
            # print(imgs_path)
            # print(next(imgs_list))
            # print(j)
            img = Image.open(os.path.join(imgs_path, j))
            # img.show()
            out = img.transpose(Image.FLIP_TOP_BOTTOM)
            out = img.rotate(45)
            # out = img.transpose(Image.ROTATE_90)
            # out = img.transpose(Image.ROTATE_180)
            name = ''.join(random.sample(string.ascii_letters, len(string.ascii_letters)))
            out.save(f'{os.path.join(imgs_path,name)}.jpeg')




# imgs = (i for i in dir_files if re.search(r'\.jpeg', i) is not None)
