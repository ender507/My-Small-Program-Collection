#import pywinio
import time
#import atexit
from util2 import *
import os

H = [None,0x10,0x11,0x12,0x13,0x14,0x15,0x16]
M = [None,0x1E,0x1F,0x20,0x21,0x22,0x23,0x24]
L = [None,0x2C,0x2D,0x2E,0x2F,0x30,0x31,0x32]
'''
H = [None,'q','w','e','r','t','y','u']
M = [None,'a','s','d','f','g','h','j']
L = [None,'z','x','c','v','b','n','m']
'''
INT_STD = -1


if __name__ == '__main__':
    lst = os.listdir('乐谱/')
    i = 1
    for each in lst:
        print('【',i,'】',lst[i-1])
        i+=1
    music = lst[int(input())-1]
    time.sleep(3)
    with open('乐谱/'+music) as f:
        flag = True
        for eachLine in f:
            # 读取曲速
            if flag:
                flag = False
                INT_STD = float(eachLine[:-1])
                continue
            # 读取乐谱
            eachLine = eachLine[:-1]
            int_now = INT_STD
            lvl = 0
            play_list = []
            mult = False
            for c in eachLine:
                if c == '_':
                    int_now /= 2
                elif c == ' ':
                    continue
                elif c == '#':
                    break
                elif c == '!':
                    int_now /= 3
                elif c == '+':
                    lvl = 1
                elif c == '-':
                    lvl = -1
                elif c == '0':
                    time.sleep(int_now)
                    int_now = INT_STD
                elif c == '(':
                    mult = True
                elif c == ')':
                    mult = False
                    for each in play_list:
                        key_press(each)
                    time.sleep(int_now)
                    play_list = []
                    int_now = INT_STD
                    lvl = 0
                else:
                    if mult == False:
                        if lvl == 1:
                            key_press(H[int(c)])
                        elif lvl == -1:
                            key_press(L[int(c)])
                        else:
                            key_press(M[int(c)])
                        time.sleep(int_now)
                        int_now = INT_STD
                        lvl = 0
                    else:
                        if lvl == 1:
                            play_list.append(H[int(c)])
                        elif lvl == -1:
                            play_list.append(L[int(c)])
                        else:
                            play_list.append(M[int(c)])
                        lvl = 0
                    
            
            
