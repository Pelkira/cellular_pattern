#Author : @Pelkira
# coding:utf-8
from PIL import Image
import numpy as np
import random
import os
import pix

r = 4 #画像の拡大率(計算上の1ピクセルをr*rの正方形として描画する)
m = 128 #ピクセルの1ピクセル
k = 22 #左側・上側の余白
d = [[-2,-1],[-1,0],[0,-1]] #参照ピクセル　対象のピクセルから[縦,横]だけ移動したマスを参照する 3つじゃなくても良い
#確率[%] 実数に対応してないのでより細かくしたい場合は下部(*)の100を1000とかにするなり実数乱数使うなり
#(生成ディレクトリ名にpが含まれるので実数にするときは注意)
p = 1
colors = [[255,255,220],[220,90,90]] #False(0)のRGB, True(1)のRGB

num_d = len(d)
M = m + k

img = Image.new("RGB",(r*m,r*m),(255,255,255))
img_array = np.asarray(img)
img_array.flags.writeable = True

path = './png/' + str(d) + '-' + str(p) #画像を吐く場所

if not os.path.isdir(path):
    os.makedirs(path)

for s in range(0,256): #256枚生成
    #seed : 一次元セルオートマトンでいうwolfram codeに該当するもの[rule30 <=> seed = 30]
    #参照ピクセル数(num_d)が3のときは2^(2^3)=256個全て生成する,それ以上なら256回ランダムに決定する(重複した場合上書き)
    seed = s if num_d == 3 else random.randrange(0,1 << (1 << num_d))
    pixels = pix.calc_pixels_round_trip(seed, M, d, p)
    #右下m*mマスのみを縦横r倍して描画(保存)
    for i in range(r*k, r*M):
        for j in range(r*k, r*M):
            img_array[i - r*k][j - r*k] = colors[1] if pixels[(i-k)/r][(j-k)/r] else colors[0]
    pil_img = Image.fromarray(np.uint8(img_array))
    #pil_img.show() #その場で描画
    pil_img.save(path + '/' + str(seed) + '-' + str(p) + '.png') #pathの位置に保存
