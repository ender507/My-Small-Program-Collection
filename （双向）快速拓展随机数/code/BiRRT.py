import random
import math
from PIL import Image
import numpy as np

def show_tree():
    n = points_sampled1.shape[0]
    mapimg_tree_array = mapimg_array.copy()
    for i in range(n):
        for j in range(i + 1, n):
            if graph1[i][j]:
                points_line = get_line(points_sampled1[i], points_sampled1[j])
                for y, x in points_line:
                    mapimg_tree_array[y][x] = np.array(color_sample)
    n = points_sampled2.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if graph2[i][j]:
                points_line = get_line(points_sampled2[i], points_sampled2[j])
                for y, x in points_line:
                    mapimg_tree_array[y][x] = np.array(color_sample)
    y_start, x_start = point_start
    y_end, x_end = point_end
    mapimg_tree_array[y_start][x_start] = np.array(color_start)
    mapimg_tree_array[y_end][x_end] = np.array(color_end)
    mapimg_tree = Image.fromarray(mapimg_tree_array)
    mapimg_tree.show()
    return

def show_path(p_cross):
    node_set = np.array([[0,0]]).astype(int)
    n = points_sampled1.shape[0]
    mapimg_path_array = mapimg_array.copy()
    p1 = p_cross
    while p1.tolist() != point_start.tolist():
        node_set = np.append(node_set, np.array([p1]), axis=0)
        idx = points_sampled1.tolist().index(p1.tolist())
        idx = graph1[idx].tolist().index(2)
        p2 = points_sampled1[idx]
        points_line = get_line(p1, p2)
        for y, x in points_line:
            mapimg_path_array[y][x] = np.array(color_sample)
        p1 = p2
    n = points_sampled2.shape[0]
    p1 = p_cross
    node_set = np.append(node_set, np.array([point_start]), axis=0)
    node_set = node_set[1:]
    node_set = node_set[::-1]
    while p1.tolist() != point_end.tolist():
        idx = points_sampled2.tolist().index(p1.tolist())
        idx = graph2[idx].tolist().index(2)
        p2 = points_sampled2[idx]
        points_line = get_line(p1, p2)
        for y, x in points_line:
            mapimg_path_array[y][x] = np.array(color_sample)
        p1 = p2
        node_set = np.append(node_set, np.array([p1]), axis=0)
    mapimg_path = Image.fromarray(mapimg_path_array)
    mapimg_path.show()
    # 简化路径
    pathSmooth(node_set)
    return

def pathSmooth(node_set):
    mapimg_path_array = mapimg_array.copy()
    n = node_set.shape[0]
    p1 = 0	# 第一个节点
    p2 = 1	# p1 能到达的下一个位置
    while p2 != n-1:
        # 若 p2 能继续往后取且路径无障碍，则继续取
        points_line = get_line(node_set[p1], node_set[p2+1])
        if is_safe(points_line):
            p2 += 1
            continue
        # 否则将p1到p2作为新的路径，输出在图上
        points_line = get_line(node_set[p1], node_set[p2])
        for y, x in points_line:
            mapimg_path_array[y][x] = np.array(color_sample)
        # 更新p1和p2，继续简化之后的路径
        p1 = p2
        p2 += 1
    # 退出上述循环时还没有进行终点的连线，在循环外进行
    points_line = get_line(node_set[p1], node_set[p2])
    for y, x in points_line:
        mapimg_path_array[y][x] = np.array(color_sample)
    # 打印结果
    mapimg_path = Image.fromarray(mapimg_path_array)
    mapimg_path.show()
    return
    
def is_safe(points_line):
    for y, x in points_line:
        if mapimg_status[y][x] > 0:
            return False
    return True

def get_line(p1, p2):
    points_line = np.array([p1])
    delta = p2 - p1
    # 填充点的数量由两点之间的距离决定
    num_interpolate = math.ceil(np.linalg.norm(delta))
    for i in range(1, num_interpolate):
        point = np.trunc(p1 + i / num_interpolate * delta)
        points_line = np.vstack([points_line, point])
    return points_line.astype(int)
    

def expand1(p_rand, points_sampled):
    points_sampled_list = points_sampled.tolist()
    points_sampled_list.sort(key = lambda x:np.linalg.norm(x - p_rand))
    if p_rand.tolist() == points_sampled_list[0]:       # 随机点不能是已经采样过的点
        return points_sampled, None
    p_new = (points_sampled_list[0] + deltaq * (p_rand -\
    points_sampled_list[0])/np.linalg.norm(p_rand - points_sampled_list[0])).astype(int)
    if p_new.tolist() in points_sampled_list:           # 新点不能是已经采样过的点
        return points_sampled, None
    points_line = get_line(points_sampled_list[0], p_new)   
    if is_safe(points_line) is False:
        return points_sampled, None
    idx = points_sampled.tolist().index(points_sampled_list[0])
    points_sampled = np.append(points_sampled, np.array([p_new]), axis=0)
    graph1[idx, points_sampled.shape[0]-1] = 1
    graph1[points_sampled.shape[0]-1, idx] = 2
    return points_sampled, p_new

def expand2(p_rand, points_sampled, flag):
    points_sampled_list = points_sampled.tolist()
    points_sampled_list.sort(key = lambda x:np.linalg.norm(x - p_rand))
    if p_rand.tolist() == points_sampled_list[0]:       # 随机点不能是已经采样过的点
        return points_sampled2, False
    p_new = (points_sampled_list[0] + deltaq * (p_rand -\
        points_sampled_list[0])/np.linalg.norm(p_rand - points_sampled_list[0])).astype(int)
    while 1:
        if p_new.tolist() in points_sampled_list:           # 新点不能是已经采样过的点
            return points_sampled, False
        points_line = get_line(points_sampled_list[0], p_new)
        if is_safe(points_line) is False:
            return points_sampled, False
        idx = points_sampled.tolist().index(points_sampled_list[0])
        points_sampled = np.append(points_sampled, np.array([p_new]), axis=0)
        graph2[idx, points_sampled.shape[0]-1] = 1
        graph2[points_sampled.shape[0]-1, idx] = 2
        points_sampled_list1_tmp = points_sampled1.tolist()
        points_sampled_list1_tmp.sort(key = lambda x:np.linalg.norm(x - p_new))
        if np.linalg.norm(points_sampled_list1_tmp[0] - p_new) <= deltaq:
            points_sampled = np.append(points_sampled, np.array([points_sampled_list1_tmp[0]]), axis=0)
            graph2[points_sampled.shape[0]-2, points_sampled.shape[0]-1] = 1
            graph2[points_sampled.shape[0]-1, points_sampled.shape[0]-2] = 2
            return points_sampled, True
        if flag is False:
            return points_sampled, False
        p_new = (p_new + deltaq * (p_rand -\
            points_sampled_list[0])/np.linalg.norm(p_rand - points_sampled_list[0])).astype(int)
        
        
mapimg = Image.open('map1.png')
mapimg_array = np.array(mapimg)
wid, hei = mapimg.size
robot_radius = 5
deltaq = 10
n = 10000
color_start = (236, 28, 36)
color_end = (63, 72, 204)
color_sample = (139, 129, 76)

# 获取起点、终点
lst_point_start = []
lst_point_end = []
for y in range(mapimg_array.shape[0]):
    for x in range(mapimg_array.shape[1]):
        # 找到是红色的所有点，它们的坐标平均值是起点中心
        if (mapimg_array[y][x] == color_start).all() == True:
            lst_point_start.append([y, x])
        # 找到是蓝色的所有点，它们的坐标平均值是终点中心
        elif (mapimg_array[y][x] == color_end).all() == True:
            lst_point_end.append([y, x])
np_point_start = np.array(lst_point_start)
np_point_end = np.array(lst_point_end)
point_start = np_point_start.mean(axis = 0).astype(int)
point_end = np_point_end.mean(axis = 0).astype(int)


# 转换成灰度图
mapimg_grey_array = mapimg_array.copy()
mapimg_grey_array[mapimg_grey_array>0] = 255
mapimg_grey_array = mapimg_grey_array[:,:,0]
mapimg_grey = Image.fromarray(mapimg_grey_array)
mapimg_grey.show()
# 转换成逻辑图且进行障碍的拓展
mapimg_status = np.where(mapimg_grey_array == 0, 1, 0)
for y in range(mapimg_status.shape[0]):
    for x in range(mapimg_status.shape[1]):
        if mapimg_status[y][x] != 1:
            continue
        for y_new in range(max(y - robot_radius, 0), min(y + robot_radius + 1, hei), 1):
            for x_new in range(max(x - robot_radius, 0), min(x + robot_radius + 1, wid), 1):
                if mapimg_status[y_new][x_new] == 0:
                    mapimg_status[y_new][x_new] = 2 
mapimg_grey_extanded_array = mapimg_grey_array.copy()
# 0: 可走，1: 原障碍，2: 扩展障碍
mapimg_grey_extanded_array[mapimg_status == 2] = 0    # 扩展点是黑色
mapimg_grey_extanded = Image.fromarray(mapimg_grey_extanded_array)
mapimg_grey_extanded.show()

# RRT算法部分
points_sample = np.argwhere(mapimg_status == 0)      # 可走点
# 添加起点
points_sampled1 = np.array([point_start])		# 从起点开始的RRT树
points_sampled2 = np.array([point_end])			# 从终点开始的RRT树
graph1 = np.zeros([n, n]).astype(int)			# 起点RRT树的邻接矩阵
graph2 = np.zeros([n, n]).astype(int)			# 终点RRT树的邻接矩阵
p_cross = np.array([])				    	# 记录两棵树相交的点
while True:
    if points_sampled1.shape[0] <= points_sampled2.shape[0]:
        if random.randint(0,100) <= 80:
            idx = np.random.choice(np.arange(points_sample.shape[0]), 1)
            p_rand = points_sample[idx][0]
        else:
            p_rand = np.array(point_end)
        points_sampled1,p_new = expand1(p_rand, points_sampled1)
        # 只有拓展成功才进行判断
        if p_new is not None:
            # 找到第二棵树离新节点最近的节点
            points_sampled_list2_tmp = points_sampled2.tolist()
            points_sampled_list2_tmp.sort(key = lambda x:np.linalg.norm(x - p_new))
            # 若两点之间的距离小于deltaq，则连接两点，得到结果
            if np.linalg.norm(points_sampled_list2_tmp[0] - p_new) <= deltaq:
                # 进一步拓展，并更新邻接矩阵
                points_sampled1 = np.append(points_sampled1, np.array([points_sampled_list2_tmp[0]]), axis=0)
                graph1[points_sampled1.shape[0]-2, points_sampled1.shape[0]-1] = 1
                graph1[points_sampled1.shape[0]-1, points_sampled1.shape[0]-2] = 2
                # 记录相交的节点
                p_cross = np.array(points_sampled_list2_tmp[0])
                break	# 找到解，退出循环
    else:
        flag = False			# 记录第一棵树上次拓展是否成功
        if p_new is not None:
            flag = True
            p_rand = p_new		# 若成功，随机点直接取上次拓展节点
        else:					# 否则进行随机取点
            if random.randint(0,100) <= 80:
                idx = np.random.choice(np.arange(points_sample.shape[0]), 1)
                p_rand = points_sample[idx][0]
            else:
                p_rand = np.array(point_start)
        points_sampled2, find_ans = expand2(p_rand, points_sampled2, flag)
        p_new = None
        if find_ans:
            p_cross = np.array(points_sampled2[-1])
            break

show_tree()
show_path(p_cross)    
