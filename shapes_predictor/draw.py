import os
import pygame
import sys
import math
import string, random
import logging
from collections import Counter
from PIL import Image
from pygame.locals import *
# from model import *

#folder structure
#circles--->
# ->1circles
#   -> .png names statrwith 1circles(random_chars).png
# ->2circles
#   -> .png names statrwith 2circles(random_chars).png
# ->3circles
#   -> .png names statrwith 2circles(random_chars).png
# ..........
pygame.init()

class Draw:
    width, height = 800, 600
    white = [255,255,255]
    black = [0,0,0]
    CWD = os.getcwd()


    def __init__(self):
        self.count = Counter()
        self.circle = 'circles'
        
        self.dcount = {}
        self.set_display()

    def set_display(self):
        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill(self.white)
        self.pix_arr = pygame.PixelArray(self.display)
        self.press = False

    def mk_path(self, num, input):
        if not os.path.exists(os.path.join(self.CWD, input)):
            os.mkdir(os.path.join(CWD, input))
        PATH = os.path.join(CWD, input)
        response_path = os.path.join(PATH, f'{num}{input}')
        if not os.path.exists(response_path):
            os.mkdir(response_path)
        return response_path

    @property
    def random_chars(self):
        name = ''.join(random.sample(string.ascii_letters, len(string.ascii_letters)))
        return name

    @property
    def get_pos(self):
        self.count.update('+')
        px2, py2 = pygame.mouse.get_pos()
        print(px2,py2)
        px_vec = px2-self.px
        py_vec = py2-self.py
        return math.sqrt(math.pow(px_vec, 2)+math.pow(py_vec, 2))

    def save(self, option):
        folder_num = len(self.dcount.values())
        if folder_num > 0:
            print(self.dcount)
            print(folder_num)
            print('call')
            self.full_path = self.mk_path(folder_num, option)
            print(self.full_path)
            pygame.image.save(self.display, os.path.join(self.full_path, f'{self.random_chars}.jpeg'))
            self.dcount.clear()
            return True

    #GAME
    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.px, self.py = pygame.mouse.get_pos()
                # print('gotit')
                print(self.px, self.py)

            if pygame.mouse.get_pressed() == (1,0,0): #if want to draw smth
                rad = self.get_pos
                # print(get_pos(px,py))

            if event.type == pygame.MOUSEBUTTONUP:
                pygame.draw.circle(self.display, self.black, (self.px, self.py), rad, width=5)
                self.dcount[f'radius{rad}'] = '+'
                print(self.dcount)
                press=False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.display.fill(self.white)
                self.dcount.clear()

            # if keys[pygame.K_c]:
                # save_to_predict = self.mk_path(input)

                # self.predict()

            if keys[pygame.K_s]:
                self.save(self.circle)
                # folder_num = int(input('type cirlces number: '))

            pygame.display.update()
        return

#predictions #! Not avaliable still
class Predict(Draw):
    def __init__(self):
        super().__init__()
        self.predictions = 'predictions'
        self.class_names = ['1 circle', '2 circles', '3 circles', '4 circles', '5 circles', '6 circles']

    @property
    def last_created_img(self):
        return sorted(os.listdir(self.full_path), key=lambda x: os.stat(os.path.join(self.full_path,x)).st_mtime, reverse=True)

    def predict(self):
        if self.save(self.predictions):
            # print(self.last_created_img())
            img = tf.keras.utils.load_img(
                    os.path.join(self.full_path, self.last_created_img[0]),
                    color_mode = 'rgb',
                    target_size = (180, 180),
            )
            arr_img = tf.keras.preprocessing.image.img_to_array(img)
            arr_img = np.array([arr_img])
            print(arr_img.shape)
            probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])
            predict = probability_model.predict(arr_img)
            print(predict)
            index = np.argwhere(predict[0]==np.amax(predict[0]))[0]
            print(index)
            print(f'I predict there is/are { self.class_names[index[0]]} on screen!')
        return

        # model = predict
    #play
    #save
    #predict



if __name__ == '__main__':
    print(f'running from {__name__}')
    Draw().play()



