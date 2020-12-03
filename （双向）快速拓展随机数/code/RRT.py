import random
import math
from PIL import Image
import numpy as np

def show_tree(points_sampled, graph):
    n = points_sampled.shape[0]			# 拓展节点总数
    mapimg_tree_array = mapimg_array.copy()
    # 遍历邻接矩阵（因为连通的对称性，只需要考虑半边）
    for i in range(n):
        for j in range(i + 1, n):
            # 若当前两点连通，则获取连线并改为color_sample颜色
            if graph[i][j]:
                points_line = get_line(points_sampled[i], points_sampled[j])
                for y, x in points_line:
                    mapimg_tree_array[y][x] = np.array(color_sample)
    # 加入起点和终点，并改为相应的颜色
    y_start, x_start = point_start
    y_end, x_end = point_end
    mapimg_tree_array[y_start][x_start] = np.array(color_start)
    mapimg_tree_array[y_end][x_end] = np.array(color_end)
    # 打印结果
    mapimg_tree = Image.fromarray(mapimg_tree_array)
    mapimg_tree.show()
    return

def show_path(points_sampled, graph):
    node_set = np.array([[0,0]]).astype(int)		# 记录路径上所有节点
    mapimg_path_array = mapimg_array.copy()
    p1 = point_end		# 从终点往前回溯
    while p1.tolist() != point_start.tolist():		# 回溯到起点为止
        node_set = np.append(node_set, np.array([p1]), axis=0)
        # 找到 p1 在邻接矩阵中对应为 2 的位置，从而找到父节点 p2
        idx = points_sampled.tolist().index(p1.tolist())
        idx = graph[idx].tolist().index(2)
        p2 = points_sampled[idx]
        # 将 p1 和 p2 的连线显示在图上
        points_line = get_line(p1, p2)
        for y, x in points_line:
            mapimg_path_array[y][x] = np.array(color_sample)
        # p1 = p2并继续向前回溯
        p1 = p2
    # 打印结果
    node_set = np.append(node_set, np.array([p1]), axis=0)
    mapimg_path = Image.fromarray(mapimg_path_array)
    mapimg_path.show()
    # 简化路径
    node_set = node_set[1:]
    pathSmooth(node_set[::-1])
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
    num_interpolate = math.ceil(np.linalg.norm(delta))	# 计算两点的距离
    # 通过线性差值的方法，得到路径上的所有点（取整数）
    for i in range(1, num_interpolate):
        point = np.trunc(p1 + i / num_interpolate * delta)
        points_line = np.vstack([points_line, point])
    return points_line.astype(int)
    

def expand(p_rand, points_sampled):
    points_sampled_list = points_sampled.tolist()
    # 找到离随机点最近的节点
    points_sampled_list.sort(key = lambda x:np.linalg.norm(x - p_rand))
    # 随机点不能是已经采样过的点
    if p_rand.tolist() == points_sampled_list[0]:       
        return points_sampled
    # 计算新点
    p_new = (points_sampled_list[0] + deltaq * (p_rand -\
    points_sampled_list[0])/np.linalg.norm(p_rand - points_sampled_list[0])).astype(int)
    # 新点不能是已经采样过的点
    if p_new.tolist() in points_sampled_list:           
        return points_sampled
    # 进行节点到新点的连接，如果路径无障碍则拓展
    points_line = get_line(points_sampled_list[0], p_new)   
    if is_safe(points_line) is False:
        return points_sampled
    idx = points_sampled.tolist().index(points_sampled_list[0])
    # 更新RRT树的节点和邻接矩阵
    points_sampled = np.append(points_sampled, np.array([p_new]), axis=0)
    graph[idx, points_sampled.shape[0]-1] = 1
    graph[points_sampled.shape[0]-1, idx] = 2
    return points_sampled

        
mapimg = Image.open('map1.png')		# 读入地图图片
mapimg_array = np.array(mapimg)		# 将地图转换为矩阵
wid, hei = mapimg.size			# 获取地图大小
robot_radius = 5			# 设置机器人半径
deltaq = 10				# 节点拓展距离
n = 10000				# 最大迭代次数
color_start = (236, 28, 36)		# 起点颜色（由地图图片决定）
color_end = (63, 72, 204)		# 终点颜色（由地图图片决定）
color_sample = (139, 129, 76)		# 最终展示路径的颜色

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
point_start = np_point_start.mean(axis = 0).astype(int)	# 取均值得到起点坐标
point_end = np_point_end.mean(axis = 0).astype(int)	# 取均值得到终点坐标


# 转换成灰度图
mapimg_grey_array = mapimg_array.copy()
mapimg_grey_array[mapimg_grey_array>0] = 255		# 将所有不为障碍的地方改为通路（全白），即消除起点和终点
mapimg_grey_array = mapimg_grey_array[:,:,0]		# 取一个通道，从而去掉冗余部分
mapimg_grey = Image.fromarray(mapimg_grey_array)
mapimg_grey.show()					# 打印初始地图
# 转换成逻辑图且进行障碍的拓展
mapimg_status = np.where(mapimg_grey_array == 0, 1, 0)  # 转换灰度图，各个位置0为通路，1为障碍
# 搜索地图的每一个位置
for y in range(mapimg_status.shape[0]):
    for x in range(mapimg_status.shape[1]):
        if mapimg_status[y][x] != 1:
            continue
        # 如果当前位置为障碍，则向上下左右进行拓展
        for y_new in range(max(y - robot_radius, 0), min(y + robot_radius + 1, hei), 1):
            for x_new in range(max(x - robot_radius, 0), min(x + robot_radius + 1, wid), 1):
                if mapimg_status[y_new][x_new] == 0:
                    mapimg_status[y_new][x_new] = 2     # 拓展的障碍为2
mapimg_grey_extanded_array = mapimg_grey_array.copy()
mapimg_grey_extanded_array[mapimg_status == 2] = 0    # 扩展点是黑色
mapimg_grey_extanded = Image.fromarray(mapimg_grey_extanded_array)
mapimg_grey_extanded.show() # 打印拓展后的地图

# RRT算法部分
points_sample = np.argwhere(mapimg_status == 0) 	# 通路点的集合
points_sampled = np.array([point_start])			# RRT树的所有节点
graph = np.zeros([n, n]).astype(int)				# 邻接矩阵
while True:
    if random.randint(0,100) <= 80:
        idx = np.random.choice(np.arange(points_sample.shape[0]), 1)
        p_rand = points_sample[idx][0]
    else:
        p_rand = np.array(point_end)
    points_sampled = expand(p_rand, points_sampled)
    
    if np.linalg.norm(point_end - points_sampled[-1]) <= deltaq:
        points_sampled = np.append(points_sampled, np.array([point_end]), axis=0)
        graph[points_sampled.shape[0]-2, points_sampled.shape[0]-1] = 1
        graph[points_sampled.shape[0]-1, points_sampled.shape[0]-2] = 2
        break

show_tree(points_sampled, graph)
show_path(points_sampled, graph)    
