#Author : @Pelkira

from PIL import Image
import numpy as np
import random
import os


r = 4 #画像の拡大率(計算上の1ピクセルをr*rの正方形として描画する)
m = 128 #ピクセルの1ピクセル
k = 22 #左側・上側の余白
d = [[-2,-2],[-1,0],[0,-1]] #参照ピクセル　対象のピクセルから[縦,横]だけ移動したマスを参照する 3つじゃなくても良い
#確率[%] 実数に対応してないのでより細かくしたい場合は下部(*)の100を1000とかにするなり実数乱数使うなり
#(生成ディレクトリ名にpが含まれるので実数にするときは注意)
p = 1
colors = [[255,255,220],[220,90,90]] #False(0)のRGB, True(1)のRGB

num_d = len(d)
M = m + k

img = Image.new("RGB",(r*m,r*m),(255,255,255))
img_array = np.asarray(img)
img_array.flags.writeable = True

pix = np.full((M,M),False)

path = './png/' + str(d) + '-' + str(p) #画像を吐く場所

if not os.path.isdir(path):
    os.makedirs(path)

for s in range(0,256): #256枚生成
    #seed : 一次元セルオートマトンでいうwolfram codeに該当するもの[rule30 <=> seed = 30]
    #参照ピクセル数(num_d)が3のときは2^(2^3)=256個全て生成する,それ以上なら256回ランダムに決定する(重複した場合上書き)
    seed = s if num_d == 3 else random.randrange(0,1 << (1 << num_d))
    for i in range(0,M): # 縦方向
        for j in range(0,M): # 横方向
            x = [False] * num_d
            # state_code : 参照ピクセルの0/1により決まる何番目の規則に該当するかを表す
            state_code = 0
            for l in range(0,num_d): # state_code を計算する
                I = i + d[l][0]
                J = j + d[l][1]
                x[l] = pix[I][J] if (0 <= I and I < M and 0 <= J and J < M) else False
                state_code += (1 << l) if x[l] else 0
            #state_codeに合致する規則においてこのピクセルが0/1のどちらか判定
            pix[i][j] = True if ((seed & (1 << state_code)) != 0) else False
            #確率pで反転
            if random.randint(0,100) % 100 < p :
                pix[i][j] = not pix[i][j]

    #右下m*mマスのみを縦横r倍して描画(保存)
    for i in range(r*k, r*M):
        for j in range(r*k, r*M):
            img_array[i - r*k][j - r*k] = colors[1] if pix[(i-k)/r][(j-k)/r] else colors[0]
    pil_img = Image.fromarray(np.uint8(img_array))
    #pil_img.show() #その場で描画
    pil_img.save(path + '/' + str(seed) + '-' + str(p) + '.png') #pathの位置に保存
