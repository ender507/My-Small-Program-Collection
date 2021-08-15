from PIL import Image
from PIL import ImageFilter
import random
import numpy as np
import matplotlib.pyplot as plt

# 用于查询某个片段内部的所有像素
SEG_GROUP = dict()
# 每个片段内的最大距离
INNER_WEIGHT = dict()
# 初步分块时的大小（取值是针对不同图片反复测试出来的，没有理论依据）
SEGMENT_NUM = [5000, 8000, 5000, 8000, 5000,
               3000, 10000, 12000, 10000, 7000]

def imSave(pic, title, save_path, show):
    # 展示1s的图片
    if show:
        plt.get_current_fig_manager().window.state('zoomed')
        plt.imshow(pic)
        #plt.show()
        plt.ion()
        plt.pause(1)
        plt.close()
        
    # 保存
    pic.save(save_path+str(title)+'.png')


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
    k = 100
    dist1 = INNER_WEIGHT[(coord1[0],coord1[1])] + k/len(SEG_GROUP[(coord1[0],coord1[1])])
    dist2 = INNER_WEIGHT[(coord2[0],coord2[1])] + k/len(SEG_GROUP[(coord2[0],coord2[1])])
    return min(dist1, dist2)

 
# 图像分割
def segment(img, pid):
    global INNER_WEIGHT, SEG_GROUP, SEGMENT_NUM
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
    while segment_num > SEGMENT_NUM[pid]:
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
        if segment_num%1000 == 0:
            print(segment_num)
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
    
    # 为当前分区图片上色
    color = dict()
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            coord = getSegment((i,j), segment_coord)
            coord = (coord[0],coord[1])
            if coord not in color.keys():
                color[coord] = [random.randint(0,255) for i in range(3)]
            img_array[i,j] = color[coord]
    print('【'+str(len(color.keys()))+'】')
    return img_array


# 标记前景背景
def segmentGround(ground):
    ground_array = np.array(ground).astype(np.int8)
    result = np.zeros(ground_array.shape).astype(np.int8)
    for seg in SEG_GROUP.keys():
        black = 0
        white = 0
        for pixel in SEG_GROUP[seg]:
            if ground_array[pixel[0],pixel[1]] == 1:
                white += 1
            else:
                black += 1
        if white > black:
            for pixel in SEG_GROUP[seg]:
                result[pixel[0],pixel[1]] = 255
    return result


if __name__ == '__main__':
    
    for i in range(57, 1000, 100):
        img = Image.open("data\\imgs\\"+str(i)+".png")       # 原图
        ground = Image.open("data\\gt\\"+str(i)+".png").convert('1')    # 前景背景图，转化为黑白图
        img_array = segment(img, i//100)
        imSave(Image.fromarray(img_array.astype('uint8')).convert('RGB'),
                   str(i)+"_1", "output\\ImageSegmentation\\", False)
        img_array = segmentGround(ground)
        imSave(Image.fromarray(img_array.astype('uint8')).convert('1'),
                   str(i)+"_2", "output\\ImageSegmentation\\", False)

        np.save('statistics\\SEG_GROUP_'+str(i)+'.npy',SEG_GROUP)

    
