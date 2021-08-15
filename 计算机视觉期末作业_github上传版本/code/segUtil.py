from PIL import Image
from PIL import ImageFilter
import random
import numpy as np


# 用于查询某个片段内部的所有像素
SEG_GROUP = dict()
# 每个片段内的最大距离
INNER_WEIGHT = dict()


# 计算两个相邻像素在特征空间(x,y,r,g,b)的欧式距离
def distance(coord1,coord2,img_array):
    vec1 = np.array([coord1[0],coord1[1],img_array[coord1[0]][coord1[1]][0],
            img_array[coord1[0]][coord1[1]][1],img_array[coord1[0]][coord1[1]][2]])
    vec2 = np.array([coord2[0],coord2[1],img_array[coord2[0]][coord2[1]][0],
            img_array[coord2[0]][coord2[1]][1],img_array[coord2[0]][coord2[1]][2]])
    return np.linalg.norm(vec1-vec2)


# 查询一个像素所属的区域
def getSegment(coord, segment_coord):
    coord = np.array(coord)
    tmp = coord.copy()
    while (segment_coord[coord[0]][coord[1]] != coord).any():
        coord = segment_coord[coord[0]][coord[1]]
    segment_coord[tmp[0]][tmp[1]] = coord   # 更新区域信息以加速之后查找
    return np.array((coord[0], coord[1]))


# 判断两个像素是否属于同一个区域
def isSameSegment(coord1, coord2, segment_coord):
    coord1 = getSegment(coord1, segment_coord)
    coord2 = getSegment(coord2, segment_coord)
    return (coord1 == coord2).all()


# 合并两个区域
def mergeSegment(coord1, coord2, img_array, segment_coord, flag=True):
    global INNER_WEIGHT, SEG_GROUP
    coord1 = getSegment(coord1, segment_coord)
    coord2 = getSegment(coord2, segment_coord)
    # 更新区域代表
    segment_coord[coord2[0]][coord2[1]] = coord1
    # 更新区域内部最大距离
    if flag:
        if (coord2[0],coord2[1]) in INNER_WEIGHT.keys():
            del INNER_WEIGHT[(coord2[0],coord2[1])]
        for vi in SEG_GROUP[(coord1[0],coord1[1])]:
            for vj in SEG_GROUP[(coord2[0],coord2[1])]:
                tmp = distance(vi,vj,img_array)
                if tmp > INNER_WEIGHT[(coord1[0],coord1[1])]:
                    INNER_WEIGHT[(coord1[0],coord1[1])] = tmp
    # 更新区域内部像素
    SEG_GROUP[(coord1[0],coord1[1])] += SEG_GROUP[(coord2[0],coord2[1])]
    del SEG_GROUP[(coord2[0],coord2[1])]
    return


# 计算两个片段的片段内距离
def internalDif(coord1, coord2, img_array, segment_coord):
    global INNER_WEIGHT, SEG_GROUP
    coord1 = getSegment(coord1, segment_coord)
    coord2 = getSegment(coord2, segment_coord)
    k = 1000
    dist1 = INNER_WEIGHT[(coord1[0],coord1[1])] + k/len(SEG_GROUP[(coord1[0],coord1[1])])
    dist2 = INNER_WEIGHT[(coord2[0],coord2[1])] + k/len(SEG_GROUP[(coord2[0],coord2[1])])
    return min(dist1, dist2)

 
# 图像分割
def segment(img, ground):
    global INNER_WEIGHT, SEG_GROUP
    INNER_WEIGHT = dict()
    SEG_GROUP = dict()
    img_array = np.array(img).astype(np.int8)
    # 初始时，区域数等于像素数
    segment_num = img.size[0] * img.size[1]
    # segment_coord[i][j]表示i,j位置的像素属于的区域，用一个统一的坐标表示
    segment_coord = np.zeros((img_array.shape[0], img_array.shape[1],2)).astype(np.int16)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            # 初始时，每个像素属于自己所在的区域
            segment_coord[i][j] = [i,j]
            SEG_GROUP[(i,j)] = [(i,j)]
            INNER_WEIGHT[(i,j)] = 0
            
    # 计算所有边的权重并按大小排序
    weight = []
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            # 每个像素只计算四个方向的边，防止重复
            if j < img_array.shape[1]-1:    # 右边的邻居
                weight.append([(i,j),(i,j+1),distance((i,j),(i,j+1),img_array)])
                if i < img_array.shape[0]-1:# 右下的邻居
                    weight.append([(i,j),(i+1,j+1),distance((i,j),(i+1,j+1),img_array)])
            if i < img_array.shape[0]-1:    # 下边的邻居
                weight.append([(i,j),(i+1,j),distance((i,j),(i+1,j),img_array)])
                if j > 0:
                    weight.append([(i,j),(i+1,j-1),distance((i,j),(i+1,j-1),img_array)])
    weight.sort(key = lambda x:x[2])
    
    t = 0
    # 当分割区域小于等于某个值则退出（初步划分保证区域小于该值）
    while segment_num > 1e4:
        # 每次挑选一条距离最小的边
        if t>=len(weight):
            break
        coord1 = weight[t][0]
        coord2 = weight[t][1]
        # 如果该边的两个顶点属于同一区域则跳过
        if isSameSegment(coord1, coord2, segment_coord):
            t += 1
            continue
        # 如果两个顶点属于两个不同的区域则依据条件合并
        if weight[t][2] < internalDif(coord1, coord2, img_array, segment_coord):
            mergeSegment(coord1, coord2, img_array, segment_coord)
            segment_num -= 1
        t += 1
        
    
    # 清除所有像素少于50个的区域（第二次划分去除小区域）
    flag = False
    flag2 = True
    while flag or flag2:
        flag = False
        flag2 = False
        for seg in SEG_GROUP.keys():
            if len(SEG_GROUP[seg]) < 50:
                flag = True
                for pixel in SEG_GROUP[seg]:
                    if pixel[0]!=0 and (not isSameSegment(pixel,(pixel[0]-1,pixel[1]), segment_coord)):
                        mergeSegment(pixel,(pixel[0]-1,pixel[1]), img_array, segment_coord, False)
                        break
                    if pixel[1]!=0 and (not isSameSegment(pixel,(pixel[0],pixel[1]-1), segment_coord)):
                        mergeSegment(pixel,(pixel[0],pixel[1]-1), img_array, segment_coord, False)
                        break
                    if pixel[0]!=img_array.shape[0]-1 and (not isSameSegment(pixel,(pixel[0]+1,pixel[1]), segment_coord)):
                        mergeSegment(pixel,(pixel[0]+1,pixel[1]), img_array, segment_coord, False)
                        break
                    if pixel[1]!=img_array.shape[1]-1 and (not isSameSegment(pixel,(pixel[0],pixel[1]+1), segment_coord)):
                        mergeSegment(pixel,(pixel[0],pixel[1]+1), img_array, segment_coord, False)
                        break
                break
            
    # 标记前景背景
    ground_array = np.array(ground).astype(np.int8)
    histograms = np.zeros((len(SEG_GROUP.keys()),8,8,8))
    labels = np.zeros(len(SEG_GROUP.keys())).astype(np.int8)
    num = 0
    for seg in SEG_GROUP.keys():
        black = 0
        white = 0
        for pixel in SEG_GROUP[seg]:
            if ground_array[pixel[0],pixel[1]] == 1:
                white += 1
            else:
                black += 1
            histograms[num,img_array[pixel[0],pixel[1],0]//32,
                       img_array[pixel[0],pixel[1],1]//32,img_array[pixel[0],pixel[1],2]//32] += 1
        histograms[num] /= np.sum(histograms[num])  # 直方图归一化
        # 给当前区域打标签
        if white > black:
            labels[num] = 1
        num += 1
    return histograms, labels




    
