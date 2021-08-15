from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt

def IOU(ground, output):
    ground_array = np.array(ground)
    output_array = np.array(output)
    intersection = 0    # 前景交集
    union = 0           # 前景并集
    for i in range(ground_array.shape[0]):
        for j in range(ground_array.shape[1]):
            if ground_array[i,j] == 1 and output_array[i,j] == 1:
                intersection += 1
            if ground_array[i,j] == 1 or output_array[i,j] == 1:
                union += 1
    return intersection / union

    

if __name__ == '__main__':
    for i in range(57, 1000, 100):
        ground = Image.open("data\\gt\\"+str(i)+".png").convert('1')
        output = Image.open("output\\ImageSegmentation\\"+str(i)+"_2.png").convert('1')
        res = IOU(ground, output)
        print('【'+str(i)+'号图片的IOU】',res)
