#Author : @Pelkira
# coding:utf-8

import numpy as np
import random

def calc_pixels(seed, M, d, p):
    pix = np.full((M,M),False)
    num_d = len(d)
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
    return pix

def calc_pixels_round_trip(seed, M, d, p):
    pix = np.full((M,M),False)
    num_d = len(d)
    for i in range(0,M): # 縦方向
        i_odd = False if i % 2 == 0 else True
        for _j in range(0,M): # 横方向
            j = M-1 - _j if i_odd else _j
            x = [False] * num_d
            # state_code : 参照ピクセルの0/1により決まる何番目の規則に該当するかを表す
            state_code = 0
            for l in range(0,num_d): # state_code を計算する
                I = i + d[l][0]
                J = j - d[l][1] if i_odd else j + d[l][1]
                x[l] = pix[I][J] if (0 <= I and I < M and 0 <= J and J < M) else False
                state_code += (1 << l) if x[l] else 0
            #state_codeに合致する規則においてこのピクセルが0/1のどちらか判定
            pix[i][j] = True if ((seed & (1 << state_code)) != 0) else False
            #確率pで反転
            if random.randint(0,100) % 100 < p :
                pix[i][j] = not pix[i][j]
    return pix
