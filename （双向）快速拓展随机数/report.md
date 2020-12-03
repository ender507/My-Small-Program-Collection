# 机器人导论作业：RRT与双向RRT

经典上课教造板凳，下课作业布置造飞机

甚至操作过程中图片处理部分比算法实现更难

## 1. 算法概述

### 1.1 RRT快速拓展随机数算法

RRT 的思想是快速扩张一群像树一样的路径以探索（填充）空间的大部分区域，伺机找到可行的路径。虽然不知道出路在哪里，但是通过随机的反复试探还是能碰对的，而且碰对的概率随着试探次数的增多越来越大，只要探索次数足够，对于有解的问题最终必然能得到结果。

RRT算法通过对状态空间中的采样点进行碰撞检测，避免了对空间的建模，能够有效地解决高维空间和复杂约束的路径规划问题。该方法的特点是能够快速有效地搜索高维空间，通过状态空间的随机采样点，把搜索导向空白区域，从而寻找到一条从起始点到目标点的规划路径，适合解决多自由度机器人在复杂环境下和动态环境中的路径规划。该方法是概率完备但不最优的。

在机器人探索迷宫的情景下，RRT算法的基本步骤是： 

1. 将起点$x_{init}$加入树的节点集合$X_{free}$
2. 在空间上随机取点$x_{random}$，在集合$X_{free}$中找到距离随机点最近的节点$x_{near}$
3. 将$x_{near}$向$x_{random}$的方向延伸$\Delta q$的距离，得到新的点$x_{new}$
4. 若$x_{near}$到$x_{new}$的路径不碰到障碍，则将$x_{near}$作为$x_{near}$的子节点加入$X_{free}$，否则重复2、3步
5. 重复2~4步，直到第四步生成的$x_{new}$和终点$x_{goal}$差距小于$\Delta q$，此时直接将终点作为$x_{new}$的子节点，就得到了从起点到终点的路径

需要注意的是，完全随机的取点会导致拓展方向完全随机，没有方向性，有可能使得探索到终点的时间极大。因此可以考虑随机点$x_{rand}$有一定的概率直接取终点$x_{goal}$，使得拓展有一定的方向性，同时又不失随机性。

在实际解决问题时，有可能问题无解，则可以设置拓展节点的个数上限，到达上限仍未达到终点后则判定为路径查找失败。

在找到满足要求的路径后，还需要对路径进行简化。通过贪心算法，从起点开始作为$p1$，依次找下一个节点$p2$，直到当前$p1$和$p2$能无碰撞连接，但$p2$再往后一个就会发生碰撞位置。$p1$到$p2$就是简化的子路径。然后再将$p2$赋值给$p1$，$p2$继续往后找路径节点，直到$p2$到达终点并成功生成全部路径。

### 1.2 双向RRT算法

RRT算法是一种纯粹的随机搜索算 法，对环境类型不敏感。为了改进RRT搜索空间的盲目性、节点拓展环节缺乏记忆性的缺点，提高空间搜索速度，在RRT算法的基础上，又有双向RRT算法。双向RRT算法有两棵树，具有双向搜索的引导策略，并且在生长方式的 基础上加上了贪婪策略加快了搜索速度，并且减少空白区域的无用搜索，节省搜索时间。

双向RRT算法的其中一棵树以另一棵树最后生成的节点作为新的拓展方向。如果拓展成功则继续往该方向拓展，直到不能拓展为止。下面的说明以从终点开始拓展的树作为例子。

需要说明的是，由持续拓展直到不能拓展的算法，可能会得到两棵树的节点数不平衡的状态。因此，当一棵树拓展完时，到下一次拓展前进行判断，哪棵树的节点数较小就拓展哪棵树，从而保证两棵树的节点数尽量相等。

双向RRT的基本算法如下：

1.  将起点$x_{init}$加入树的节点集合$X_1$，将终点$x_{goal}$加入第二棵树的节点集合$X_2$
2. 判断$X_1$和$X_2$的节点数，哪棵树的节点数小则拓展哪棵树。
3. 拓展树：
   - 若拓展$X_1$，则和RRT的拓展方法相同
   - 若拓展$X_2$则进行判断：
     - 若$X_1$最后拓展节点的方向至少能让$X_2$成功拓展一次，则向该方向拓展直到不能拓展
     - 若$X_1$最后拓展节点的方向一次都不能让$X_2$拓展成功，则取随机方向拓展
4. 重复2、3步，直到$X_1$和$X_2$最近的两个节点相距小于等于$\Delta q$，则连接这两个节点，得到最终路径

同样，得到路径后将路径通过贪心算法进行简化，得到最后的结果。

## 2. 代码实现

### 2.1 场景地图的构建

本次实验我通过`python3.7`实现。

首先配置需要的参数：

```python
mapimg = Image.open('map1.png')			# 读入地图图片
mapimg_array = np.array(mapimg)			# 将地图图片转换为矩阵
wid, hei = mapimg.size					# 获取地图大小
robot_radius = 5						# 设置机器人半径
deltaq = 20								# 节点拓展距离
n = 10000								# 最大迭代次数
color_start = (236, 28, 36)				# 起点颜色（由地图图片决定）
color_end = (63, 72, 204)				# 终点颜色（由地图图片决定）
color_sample = (139, 129, 76)			# 最终展示路径的颜色
```

考虑到地图图片上，起点和终点的都是一个圆而不是一个像素点，我们首先需要将起点和终点简化成一个点。考虑取起点颜色的所有点，取平均值得到起点的具体位置，终点同理：

```python
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
point_start = np_point_start.mean(axis = 0).astype(int)		# 取均值得到起点坐标
point_end = np_point_end.mean(axis = 0).astype(int)			# 取均值得到终点坐标
```

读入的图片是彩色图像，具有RGB三个通道，具有数据冗余，不利于路径的查找。在起点和终点已经确定的前提下，地图只需要简单地表示可以通行的部分和障碍的部分。因此，考虑将地图转换为单通道的黑白图像，以便于之后的工作。

```python
# 转换成灰度图
mapimg_grey_array = mapimg_array.copy()
mapimg_grey_array[mapimg_grey_array>0] = 255		# 将所有不为障碍的地方改为通路（全白），即消除起点和终点
mapimg_grey_array = mapimg_grey_array[:,:,0]		# 取一个通道，从而去掉冗余部分
mapimg_grey = Image.fromarray(mapimg_grey_array)
mapimg_grey.show()									# 打印初始地图
```

在实际场景中，机器人有自身的大小，而不是一个简单的点。要防止机器人碰到障碍，除了不将机器人看做一个点外，还能反过来考虑，将障碍拓展变大，从而形成限制更大的一张新的地图。将机器人看做一个圆，则通过半径延伸障碍，就能简单地将机器人看做一个点解决之后的问题了。拓展障碍的方法如下：

```python
# 转换成逻辑图且进行障碍的拓展
mapimg_status = np.where(mapimg_grey_array == 0, 1, 0)		# 转换灰度图，各个位置0为通路，1为障碍
# 搜索地图的每一个位置
for y in range(mapimg_status.shape[0]):
    for x in range(mapimg_status.shape[1]):
        if mapimg_status[y][x] != 1:
            continue
        # 如果当前位置为障碍，则向上下左右进行拓展
        for y_new in range(max(y - robot_radius, 0), min(y + robot_radius + 1, hei), 1):
            for x_new in range(max(x - robot_radius, 0), min(x + robot_radius + 1, wid), 1):
                if mapimg_status[y_new][x_new] == 0:
                    mapimg_status[y_new][x_new] = 2 	# 拓展的障碍为2
mapimg_grey_extanded_array = mapimg_grey_array.copy()
mapimg_grey_extanded_array[mapimg_status == 2] = 0    # 扩展点是黑色
mapimg_grey_extanded = Image.fromarray(mapimg_grey_extanded_array)
mapimg_grey_extanded.show()					# 打印拓展后的地图
```

取一张图片作为地图，如下所示：

<img src="pic\\1.png" style="zoom:50%;" />

场景地图部分代码的运行结果如下：

拓展前：

<img src="pic\\2.png" style="zoom:50%;" />

拓展后：

<img src="pic\\3.png" style="zoom:50%;" />

可以明显看出，场景地图被正确读入并拓展了，场景地图构建完成。

### 2.2 RRT算法的实现

创建`points_sample`为所有`mapimg_status == 0`的点的集合，也就是说，`points_sample`是所有通路的点。之后取随机点可以在该集合中取。`points_sampled`为构造的树的节点集合，初始化时只有起点。` graph`为邻接矩阵，横纵坐标表示`points_sampled`的点，矩阵值为 0 表示两个节点不连通，为 1 表示前一个节点是后一个节点的父节点，为 2 表示前一个节点是后一个节点的子节点。由此，不仅记录了树的连接关系，同时也提供了从叶子节点到根节点的回溯方法，便于之后得到路径。

```python
points_sample = np.argwhere(mapimg_status == 0) 	# 通路点的集合
points_sampled = np.array([point_start])			# RRT树的所有节点
graph = np.zeros([n, n]).astype(int)				# 邻接矩阵
```

接下来就是拓展过程了。若拓展节点数没有到最大节点数，进行以下的循环：

取随机点进行拓展。`random.randint(0,100)`生成一定范围内的随机数，通过参数调整能控制取到的$x_{rand}$是终点还是随机点。下面的代码有 80% 的几率取随机点， 20% 取终点。

```python
    if random.randint(0,100) <= 80:
        idx = np.random.choice(np.arange(points_sample.shape[0]), 1)
        p_rand = points_sample[idx][0]		# 在通路点中随机取一个
    else:
        p_rand = np.array(point_end)		# 取终点
    points_sampled = expand(p_rand, points_sampled)	# 进行拓展
```

拓展的具体方案如下：

```python
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
```

`np.linalg.norm(x - p_rand)`计算所有节点到随机点的欧几里得距离，并进行排序，从而得到离生成的随机点最近的节点。需要注意的是，如果随机点已经采样过，也就是说出现在树的节点中，则直接返回。否则计算新的节点。两点相减得到向量，除以自身的长度就能得到拓展方向。该方向乘以`deltaq`，就是最近节点拓展的方向与距离，从而能够计算得到新的节点`p_new`。若该节点已经在节点集合中，或是最近点和新节点之间的路径会遇到障碍，则直接返回。否则，拓展成功，将新节点加入节点集合，并更新邻接矩阵。

由两点得到两点连线上所有的点的方法如下：

```python
def get_line(p1, p2):
    points_line = np.array([p1])
    delta = p2 - p1
    num_interpolate = math.ceil(np.linalg.norm(delta))	# 计算两点的距离
    # 通过线性差值的方法，得到路径上的所有点（取整数）
    for i in range(1, num_interpolate):
        point = np.trunc(p1 + i / num_interpolate * delta)
        points_line = np.vstack([points_line, point])
    return points_line.astype(int)
```

最终返回连线上所有点的集合。

判断连线上是否有障碍，只要依次判断各个点是否碰到障碍即可：

```python
def is_safe(points_line):
    for y, x in points_line:
        if mapimg_status[y][x] > 0:	# 1为原有障碍，2为拓展障碍
            return False
    return True
```

每次拓展完后，判断最新的拓展节点是否与终点的距离小于等于`deltaq`。若是，则说明下一步能直接拓展到终点。将终点加入节点集合，并更新相应的邻接矩阵：

```python
    if np.linalg.norm(point_end - points_sampled[-1]) <= deltaq:
        points_sampled = np.append(points_sampled, np.array([point_end]), axis=0)
        graph[points_sampled.shape[0]-2, points_sampled.shape[0]-1] = 1
        graph[points_sampled.shape[0]-1, points_sampled.shape[0]-2] = 2
        break
```

得到结果后，打印结果，包括拓展的整棵树和找到的路径：

```python
show_tree(points_sampled, graph)
show_path(points_sampled, graph)
```

打印树的过程较为简单。遍历一遍邻接矩阵，将所有连通的点的路径打印出来即可：

```python
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
```

打印路径需要从根节点回溯到叶节点，通过邻接矩阵为 2 的值，依次向上找父节点，直到找到根节点。路径上所有的连线进行打印即可。注意下面代码中的`node_set`记录了路径上所有的节点，便于之后的路径简化。

```python
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
```

之后就是路径的平滑。从起点开始，依次查看后面的节点，将起点一次性能够到达的最远的节点作为新的路径，将该节点作为新的起点，往后循环，直到达到终点位置。

```python
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
```

### 2.3 双向RRT

双向RRT的基本算法与RRT有一定的重合之处，下面只说明不同的地方，完整的代码附在最后。

双向RRT树要对两棵树进行拓展，在两棵树相交时得到通路。定义以下变量：

```python
points_sampled1 = np.array([point_start])		# 从起点开始的RRT树
points_sampled2 = np.array([point_end])			# 从终点开始的RRT树
graph1 = np.zeros([n, n]).astype(int)			# 起点RRT树的邻接矩阵
graph2 = np.zeros([n, n]).astype(int)			# 终点RRT树的邻接矩阵
p_cross = np.array([])							# 记录两棵树相交的点
```

接着进入循环，若没得到结果则进行拓展。拓展前先进行判断：

```python
if points_sampled1.shape[0] <= points_sampled2.shape[0]:
```

哪棵树的节点少则拓展哪棵树，依次维持两棵树的节点数基本平衡。

如果是**拓展从起点开始的RRT树**，则向单向的RRT算法一样，随机生成节点进行拓展：

```python
if random.randint(0,100) <= 80:
    idx = np.random.choice(np.arange(points_sample.shape[0]), 1)
    p_rand = points_sample[idx][0]
else:
    p_rand = np.array(point_end)
points_sampled1,p_new = expand1(p_rand, points_sampled1)
```

其中，随机节点有 20% 的几率直接取终点，使得节点拓展方向总体向终点延伸。进行拓展的函数`expand1`和之前的RRT算法基本一致，只是还会返回拓展后的新节点`p_new`。若拓展失败（随机点、新点在点集中或到新节点的路径出现障碍则拓展失败），`p_new`为`None`。保存`p_new`的原因是，拓展从终点发出的RRT树时，要以此为拓展方向。

需要注意的是，在拓展完后就要进行判断，是否出现了重复节点或节点间的距离小于`deltaq`，若是则找到解：

```python
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
```

若是**拓展从终点开始的RRT树**，则先要进行判断：上一次第一棵树的拓展是否成功。若成功，则将第一棵树拓展的节点作为第二棵树的拓展方向，否则也进行随机选取，有 20% 的几率选到起点。

```python
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
```

接着进行拓展。拓展完后无论是否拓展的方向是原先的`q_new`的方向，都将`q_new`改为`None`，从而表示已经拓展过。

```python
points_sampled2, find_ans = expand2(p_rand, points_sampled2, flag)
p_new = None
```

`find_ans`表示是否找到结果。因为第二棵树拓展时可能会进行多次拓展，因此每次拓展后都要查询是否和第一棵树的节点的距离小于`deltaq`。若是，则找到答案，返回`find_ans`为`True`。若为`True`，则将最后的拓展节点记录为相交节点并退出循环。

```python
if find_ans:
    p_cross = np.array(points_sampled2[-1])
    break
```

具体的拓展过程的实现如下：

```python
def expand2(p_rand, points_sampled, flag):
    # 找出离随机节点最近的点
    points_sampled_list = points_sampled.tolist()
    points_sampled_list.sort(key = lambda x:np.linalg.norm(x - p_rand))
    if p_rand.tolist() == points_sampled_list[0]:       # 随机点不能是已经采样过的点
        return points_sampled2, False
    # 计算新节点的位置
    p_new = (points_sampled_list[0] + deltaq * (p_rand -\
        points_sampled_list[0])/np.linalg.norm(p_rand - points_sampled_list[0])).astype(int)
    # 在循环中多次拓展节点
    while 1:
        if p_new.tolist() in points_sampled_list:           # 新点不能是已经采样过的点
            return points_sampled, False
        # 若到新节点的路上有障碍则拓展失败直接返回
        points_line = get_line(points_sampled_list[0], p_new)
        if is_safe(points_line) is False:
            return points_sampled, False
        # 拓展成功，新节点加入节点列表并更新邻接矩阵
        idx = points_sampled.tolist().index(points_sampled_list[0])
        points_sampled = np.append(points_sampled, np.array([p_new]), axis=0)
        graph2[idx, points_sampled.shape[0]-1] = 1
        graph2[points_sampled.shape[0]-1, idx] = 2
        # 判断新节点到第一棵树节点的距离
        points_sampled_list1_tmp = points_sampled1.tolist()
        points_sampled_list1_tmp.sort(key = lambda x:np.linalg.norm(x - p_new))
        # 若新节点到第一棵树的某节点距离小于deltaq，则再次拓展到相交，得到答案，返回
        if np.linalg.norm(points_sampled_list1_tmp[0] - p_new) <= deltaq:
            points_sampled = np.append(points_sampled, np.array([points_sampled_list1_tmp[0]]), axis=0)
            graph2[points_sampled.shape[0]-2, points_sampled.shape[0]-1] = 1
            graph2[points_sampled.shape[0]-1, points_sampled.shape[0]-2] = 2
            return points_sampled, True
        # 若flag为False则说明第一棵树上次拓展失败了，没必要多次拓展，直接返回
        if flag is False:
            return points_sampled, False
        # 否则将继续拓展，计算新的拓展节点位置
        p_new = (p_new + deltaq * (p_rand -\
            points_sampled_list[0])/np.linalg.norm(p_rand - points_sampled_list[0])).astype(int)
```

之后展示结果需要做一些简单的调整。显示路径和树只需要将两棵树的结果都显示出来即可，和单向RRT基本相同。路径简化时，考虑到从起点发起的树为正向，从终点发起的树为逆向，需要先依次记录从相交节点到起点的路径，反向后加上从相交节点到终点的距离。这样一来，简化函数就能和之前的单向RRT算法完全一致。展示结果部分的代码都和第一部分基本相同，这里不再赘述。

## 3. 实验结果

配置机器人半径为5，单次移动距离`deltaq`为10，对第一张地图的拓展前后的结果为：

<img src="pic\\4.png" style="zoom:50%;" />

<img src="pic\\5.png" style="zoom:50%;" />

可以看出，地图成功地拓展了。

使用RRT算法，得到的树图、找到的路径和简化路径如下图所示：

<img src="pic\\6.png" style="zoom: 67%;" />

<img src="pic\\7.png" style="zoom: 67%;" />

<img src="pic\\8.png" style="zoom: 67%;" />

可以看出，在树的拓展前期，因为被大片的障碍阻碍，进行了大量的重复拓展。而在有节点和终点之间的通路基本上无障碍时，能够较为顺利地拓展到终点。

使用双向RRT算法，得到的树图、找到的路径和简化路径如下图所示：

<img src="pic\\9.png" style="zoom: 67%;" />

<img src="pic\\10.png" style="zoom: 67%;" />

<img src="pic\\11.png" style="zoom: 67%;" />

双向RRT的拓展节点数明显比RRT少了很多。实际上，仔细观察找到的路径不难发现，路径出现了几条很长的直线。这其实是沿着一个方向拓展的一系列节点。终点向起点的新拓展节点方向进行拓展大幅缩短了两棵树之间的差距，在进行少量随机拓展后，很容易就能绕过障碍，连接两棵树的节点。

下面再来看另一张地图。配置机器人半径为5，单次移动距离`deltaq`为10，对第二张地图的拓展前后的结果为：

<img src="pic\\12.png" style="zoom:50%;" />

<img src="pic\\13.png" style="zoom:50%;" />

使用RRT算法，得到的树图、找到的路径和简化路径如下图所示：

<img src="pic\\14.png" style="zoom: 67%;" />

<img src="pic\\15.png" style="zoom: 67%;" />

<img src="pic\\16.png" style="zoom: 67%;" />

在这张地图中，起点到终点要进行多次的迂回。在RRT算法中，只能通过随机生成节点，以碰运气的方式进行迂回，可以看出在需要多次迂回的场景下需要进行大量拓展，效果不佳。

使用双向RRT算法，得到的树图、找到的路径和简化路径如下图所示：

<img src="pic\\17.png" style="zoom: 67%;" />

<img src="pic\\18.png" style="zoom: 67%;" />

<img src="pic\\19.png" style="zoom: 67%;" />

在起点和终点附近，双向RRT算法也进行了大量的拓展。而且在这种反复迂回的场景下，终点树的多次拓展几乎只在最后起到作用。总的来说比单纯的RRT算法要好，但也存在明显的缺点。

最后是第三张地图。配置机器人半径为5，单次移动距离`deltaq`为10，对第三张地图的拓展前后的结果为：

<img src="pic\\20.png" style="zoom:50%;" />

<img src="pic\\21.png" style="zoom:50%;" />

使用RRT算法，得到的树图、找到的路径和简化路径如下图所示：

<img src="pic\\d.png" style="zoom: 67%;" />

<img src="pic\\e.png" style="zoom: 67%;" />

<img src="pic\\f.png" style="zoom: 67%;" />

本地图到终点有个狭窄的通路。RRT没有策略性，向无头苍蝇一样四处拓展，进行了大量的无意义拓展。从树图可以看出，整张地图几乎被拓展的节点铺满，而终点却仍然没能拓展到。这很能暴露了RRT面对狭窄通道时的缺点。

使用双向RRT算法，得到的树图、找到的路径和简化路径如下图所示：

<img src="pic\\a.png" style="zoom: 67%;" />

<img src="pic\\b.png" style="zoom: 67%;" />

<img src="pic\\c.png" style="zoom: 67%;" />

考虑到终点发起的随机拓展，在这种场景下能较快从狭窄通道中拓展出来。双向RRT比RRT的优势较好地体现了出来。

## 4. 总结

RRT 的思想是快速扩张一群像树一样的路径以探索（填充）空间的大部分区域，伺机找到可行的路径。虽然不知道出路在哪里，但是通过随机的反复试探还是能碰对的，而且碰对的概率随着试探次数的增多越来越大，只要探索次数足够，对于有解的问题最终必然能得到结果。RRT算法通过对状态空间中的采样点进行碰撞检测，避免了对空间的建模，能够有效地解决高维空间和复杂约束的路径规划问题。该方法的特点是能够快速有效地搜索高维空间，通过状态空间的随机采样点，把搜索导向空白区域，从而寻找到一条从起始点到目标点的规划路径，适合解决多自由度机器人在复杂环境下和动态环境中的路径规划。

然而，RRT算法是一种纯粹的随机搜索算 法，对环境类型不敏感。RRT具有盲目性、节点拓展环节缺乏记忆性的缺点。再此基础上提出的双向RRT算法从两端共同进行随机拓展，引入的连续拓展思想相当程度地克服了RRT的上述缺点。在一些场景下，双向RRT的效率远远超过RRT算法。

## 5. 完整代码

### 5.1 RRT

```python
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
```

### 5.2 双向RRT

```python
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
n = 1000
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
```