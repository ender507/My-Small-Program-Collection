# 计算机视觉期末大作业实验报告

> 姓名：507		学号：18340057		班级：18级计算机科学二班



## 一、 Seam Carving

### 1.1 问题描述

结合 “Lecture 6 Resizing“ 的 Seam Carving 算法，设计并实现前景保持的图像缩放，前景由 gt 文件夹中对应的标注给定。要求使用“Forward Seam Removing”机制， X， Y 方向均要进行压缩。压缩比例视图像内容自行决定（接近1-2*前景区域面积/图像面积 即可）。需要从测试子集中任选两张代表图，将每一步的 seam removing 的删除过程记录， 做成 gif 动画格式，测试子集的其余图像展示压缩后的图像结果。 

### 1.2 求解过程与算法

Seam Carving的基本思想是移除图像中不重要的像素，也就是能量更少的像素。能量高一般来说有较强的轮廓。人类的视觉对边缘更敏感，所以试着从平滑的区域移除内容。则可以使用能量函数：
$$
E_1(I)=|\frac\part{\part x}I|+|\frac\part{\part y}I|
$$
也就是以梯度的绝对值作为能量函数，对图像进行处理，可以得到一张关于图像的能量图。对于多通道的图片，对不同通道进行梯度计算然后将多通道的能量进行简单加和即可。能量越大的地方表明该处的梯度更大，因此更加重要。考虑优先删除更不重要的地方，也就是能量图中能量更少的地方。图像需要保证方正，因此考虑每次移除每一行中能量最低的像素。而且这些像素必须相邻才不会破坏图像内容。看上去，每次移除的一组像素就是从图像顶上到底下的一条曲线。

这样一来，删除的应该是能量最低的一条曲线。从上到下、从左往右遍历图片，计算到达当前位置的接缝最小的累计能量，遍历完图片后就能依据累计能量最少的路径来决定删除哪条接缝。其中，累计能量可以用动态规划计算，其动态转移方程为：
$$
M(i,j)=E(i,j)+\min(M(i-1,j-1),M(i-1,j),M(i-1,j+1))
$$
上述方法称为Backward Seam Moving。对于某些图像，采用该方法会产生断层。考虑不移除能量最少的接缝，而是移除插入能量最少的接缝，换句话说，就是去掉接缝后，希望接缝两端像素的差值最小，就能改进该不足，这样就能得到改进的Forward Seam Moving机制。上述的动态转移方程改为：
$$
M(i,j)=\min\left\{\begin{matrix}{}
M(i-1,j-1)+|I(i,j+1)-I(i,j-1)|+|I(i-1,j)-I(i,j-1)|\\
M(i-1,j)+|I(i,j+1)-I(i,j-1)|\\
M(i-1,j+1)+|I(i,j+1)-I(i,j-1)|+|I(i-1,j)-I(i,j+1)|
\end{matrix}\right.
$$
对于某些图片，我们不希望图中的某些部分被删改，因此才需要本题中的前景背景图像，确定前景位置保证前景尽可能不被删除。既然希望前景不被删除，那么就意味着前景部分有着更多的能量，因此，我们只需要将前景所在部分的能量加上一个常数即可。这个常数可以由自己设置，其值越大，表明前景越重要，被删除的优先级越低。即新能量函数为：
$$
E_2(I)=\left\{\begin{matrix}{E_1(I),当前位置为背景\\E_1(I)+k,当前位置为前景}\end{matrix}\right.
$$
因此，算法实现的步骤为：

1. 计算原图的能量图：
   - 先计算梯度图
   - 在梯度图的基础上，在前景像素对应的位置加上一个常数
2. 依据上述动态转移方程，通过动态规划方法找出能量最少的接缝并删除
3. 重复以上两步，直到图片大小被裁剪到规定的大小

### 1.3 代码实现与说明

我使用3.7版本的`python`对该算法进行了实现。本实验涉及到图片存取与删改，因此用到了图像处理库`PIL`，为了方便处理，将图像转换为矩阵进行处理，还用到了`numpy`库，为了预览中间结果，还使用了`matplotlib`库。缺少上述组件会导致程序报错。

#### 1.3.1 预处理与参数设置和说明

首先读入图片，考虑到背景图为RGB图像，但色彩只有黑白，我直接将其转换成了黑白图表示：

```python
for i in range(57, 1000, 100):
        img = Image.open("data\\imgs\\"+str(i)+".png")
        ground = Image.open("data\\gt\\"+str(i)+".png").convert('1')
```

对于每一张图片，我们首先应该要确定其缩放比例。依据题目要求，图片的应该要缩放到原来的$1-(2*前景面积)/总面积$，但据我观察，如果等比例缩放，有时最终图片不能达到较好的效果，这是因为有的图片在竖直方向上前景比例更小，有的在水平方向上前景比例更小。因此我手动设置了适合每张图片的宽度缩放比例：

```python
pic_rate = [0.5, 0.8, 0.4, 0.5, 0.7, 0.6, 0.7, 0.7, 0.5, 0.2]
```

假设当前图片对应的`pic_rate`大小为$\alpha$在计算新图像大小时，在原来的缩放比例`rate`基础上，宽度的缩放比例变为$rate^\alpha$，而高度的缩放比例变为$rate^{1-\alpha}$，这样一来可以保证图片压缩率的同时，针对图片内容进行效果更优的缩小。代码实现如下：

```python
size = img.size
front_ground = np.sum(np.array(ground) == 1)		# 统计前景面积
rate = 1 - (2*front_ground / (size[0]*size[1]))		# 计算缩小比例
new_size = (int(size[0]*(rate**pic_rate[i//100])), int(size[1]*(rate**(1-pic_rate[i//100]))))	# 进一步计算宽度和高度分别的缩小比例
```

#### 1.3.2  对高度和宽度裁剪的说明

针对宽和高的Seam Carving过程，我设计了以下两个函数：

```python
def widthCarve(img, ground, new_width, save_frames, mode)
def heightCarve(img, ground, new_height, save_frames)
```

其中，`img`为原图，`ground`为前景图，`new_width`和`new_height`为最终输出图像的宽或高，`save_frames`为保存每次中间结果的选项，如果为`True`则会保存每一帧以便之后制作gif图像。`mode`表示保存`gif`的一帧时是否要转置图片。两个函数都返回最终得到的图片和对应的前景图。

需要说明的是，对宽度的裁剪和对高度的裁剪具有高度相似性：二者执行算法的流程是一致的，只是接缝的方向不同。因此，代码很大程度上可以重用。实际上，删除图片的横向接缝，相当于将图片转置后删除图片的竖向接缝，因此，在实现高度裁剪时，只需要转置图片再调用宽度裁剪即可。得到图片后，再转置回来，从而得到最终结果：

```python
# 高度裁剪
def heightCarve(img, ground, new_height, save_frames):
    # 转置
    img = img.transpose(Image.TRANSPOSE)
    ground = ground.transpose(Image.TRANSPOSE)
    # 调用宽度裁剪
    img, ground = widthCarve(img, ground, new_height, save_frames, 2)
    # 转置回来
    img = img.transpose(Image.TRANSPOSE)
    ground = ground.transpose(Image.TRANSPOSE)
    # 将帧号变为0
    global frame
    frame = 0
    return img, ground
```

我的算法是先进行宽度裁剪再进行高度裁剪，因此高度裁剪完成意味着当前图片处理完成，全局变量`frame`表示帧号，应重新置为0。

#### 1.3.3 算法实现主体

下面的内容在函数`widthCarve`中实现。在实现对图片的裁剪时，要一直修剪到图片和预期大小相同为止，因此所有的算法在一个大循环中：

```python
while True:
    width = img.size[0]
    # 宽度达到要求则退出循环
    if width == new_width:
        break
```

为了方便计算，先将图片对象转换为`numpy`的数组对象：

```python
img_array = np.array(img).astype(np.int8)
ground_array = np.array(ground).astype(np.int8)
```

然后计算能量图，即梯度图。对于RGB三通道图片来说，只需要分别计算三个通道的梯度图然后进行相加即可，注意梯度要取绝对值：

```python
red_gradient = np.array(np.gradient(img_array[:,:,0]))
red_gradient = np.maximum(red_gradient, -red_gradient)
green_gradient = np.array(np.gradient(img_array[:,:,1]))
green_gradient = np.maximum(green_gradient, -green_gradient)
blue_gradient = np.array(np.gradient(img_array[:,:,2]))
blue_gradient = np.maximum(blue_gradient, -blue_gradient)
energy_map = red_gradient[0] + red_gradient[1] + green_gradient[0] +
	green_gradient[1]+ blue_gradient[0] + blue_gradient[1]
energy_map = np.array(energy_map).astype(np.int16)
```

将前景部分增加能量的部分，我在之后的计算累计能量时进行了实现，而没有直接加在能量图上。

还需要初始化以下变量：

```python
cumulate_energy = np.zeros(energy_map.shape)# 累计能量图，使用动态规划更新的对象
path = np.zeros(energy_map.shape).astype(np.int16)# 路径图，记录最少能量的路径
new_img = np.zeros((energy_map.shape[0],energy_map.shape[1]-1,3)).astype(np.int8) # 删除接缝后的图片
new_ground = np.zeros((energy_map.shape[0],energy_map.shape[1]-1)).astype(np.int8) # 删除接缝后的前景背景图
```

`cumulate_energy`即为累计能量图，`cumulate_energy[i,j]`表示从图片顶部到达`[i,j]`位置的接缝所需的最少能量，而`path`用于记录该能量最少接缝的实际路径。如：到达`[i,j]`处能量最少的接缝的上一处位置为`[i-1,j-1]`，则`path[i,j]=j-1`。因为从上往下的接缝其行坐标依次增加，很容易得知，所以只需要保存列坐标即可。

对于第一行，直接进行赋值：

```python
cumulate_energy[0,:] = energy_map[0,:]  # 累计能量图和能量图的第一行相同
path[0,:] = -1      # 第一行路径为-1表示路径终止
```

之后的内容，依次遍历图像的每个像素并通过动态规划方法更新即可。遍历到位置`[i,j]`时，计算从左、中、右来的三条接缝分别的累计能量：

```python
left = cumulate_energy[i-1,j-1] + abs(energy_map[i,j+1] - energy_map[i,j-1]) + abs (energy_map[i-1,j] - energy_map[i,j-1])
mid = cumulate_energy[i-1,j] + abs(energy_map[i,j+1] - energy_map[i,j-1])
right = cumulate_energy[i-1,j+1] + abs(energy_map[i,j+1] - energy_map[i,j-1]) + abs (energy_map[i-1,j] - energy_map[i,j+1])
```

需要说明的是，如果在边界处，即`j`为0或`img.size[0]-1`时，上述接缝只有两条且下标会出界，因此在边界处按照Backward方法计算能量即可，即：

```python
if j == 0:  # 第一列不能有从左边来的路径
    right = cumulate_energy[i-1,j+1] + energy_map[i,j]
    mid = cumulate_energy[i-1,j] + energy_map[i,j]
elif j == img.size[0]-1:  # 最后一列不能有从右边来的路径
    left = cumulate_energy[i-1,j-1] + energy_map[i,j]
    mid = cumulate_energy[i-1,j] + energy_map[i,j]
```

只需要将`left`、`right`、`mid`初始化为一个很大的值，就能在有边界条件时也不会选到非法位置。得到三条不同接缝的累计能量后，选择最小的，并更新对应的累计能量图和路径即可。`choosePath`函数用于找出累计能量最小的路径，当`left`、`mid`、`right`分别为最小值时会分别返回-1、0、1。另外，如果当前位置是前景则额外再加上一个常数，我设置的是2550。

```python
# 找到累计能量最小的路径，记录累计能量和路径
p = choosePath(left, mid, right)
cumulate_energy[i,j] = (left, mid, right)[p+1]
# 如果当前像素是前景，则加入惩罚，即增加当前能量
if ground_array[i,j] == 1:
    cumulate_energy[i,j] += 2550
path[i,j] = j+p
```

当整张图遍历后，`cumulate_energy`的最后一行最小的值对应的接缝就是整张图中能量最少的接缝。我们只需要从下往上通过之前保存好的`path`找出该路径即可。从下往上遍历的同时，一行行将删除当前行接缝像素后的图片赋值给新图片：

```python
for i in range(img.size[1]-1, -1, -1):
    bias = 0	# 遇到删除点前，偏移为0
    for j in range(img.size[0]-1):
        if j == pos:	# 遇到删除点，偏移加一
            bias = 1
        # 将该行除了删除点外的像素赋值给新图片
        new_img[i,j,:] = img_array[i,j+bias,:]
        new_ground[i,j] = ground_array[i,j+bias]
    # 通过path查询上一行删除的像素点所在列
    pos = path[i, pos]
```

如果需要保存gif，在将上述路径删除前先赋值上色再保存即可，代码基本一致，不再赘述。需要注意的是，在高度裁剪时，使用的是转置的图片，因此保存的图片需要再进行一次转置才能恢复原来的形状。转移与否是通过之前提到的函数参数列表中的`mode`控制的。

### 1.4 结果展示与分析

我的学号尾号是57，因此使用的图片为57、157、257、...、957一共十张图。最终生成的图片在我提交的文件中下面的文件夹里，包含10张图片的结果、编号为57和557这两张图片的gif以及gif的每一帧：

> output\SeamCarving

我在提交的文件中，为了便于查看，将`output`文件夹放在了根目录下，但在实际运行代码时，需要将`output`文件夹放在`code`文件夹下，否则程序运行时会报错。

十张图片处理前后的结果分别如下，分别为原图和处理后的图片：

<div align="center"><img src="code\\data\\imgs\\57.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\57.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\157.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\157.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\257.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\257.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\357.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\357.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\457.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\457.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\557.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\557.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\657.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\657.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\757.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\757.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\857.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\857.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\957.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\957.png"  /></div>

我将图片缩放比例作为中间结果输出，得到了如下结果：

<img src="pic\\1.png" style="zoom:50%;" />

可以看到，第5张图片按照题目要求的公式，需要缩放到原来的1/5，图片缩的过小，因此效果并不太好，但其他图片相对原图都有较优的效果，特别是第7、8张图片，在长宽缩小程度超过原图的情况下仍然有较好的效果。

选取两张图的中间图片生成gif，我选择了编号为57和557的两张图，因为这两张图中，有多个前景主体，且在图片中的位置相对分散，其压缩过程更能体现Seam Carving算法的有效性：

<div align="center"><img src="code\\data\\imgs\\57.png" style="zoom:100%;" /><img src="code\\output\\SeamCarving\\557.png"  /></div>

生成的gif和gif的每一帧结果都在上述的文件夹下。下面是选取的其中几帧的中间过程作为示例：

<div align="center"><img src="code\\output\\SeamCarving\\57_frames\\57_20.png"  /><img src="code\\output\\SeamCarving\\57_frames\\57_40.png"  /><img src="code\\output\\SeamCarving\\57_frames\\57_60.png"  /></div>

<div align="center"><img src="code\\output\\SeamCarving\\557_frames\\557_20.png"  /><img src="code\\output\\SeamCarving\\557_frames\\557_40.png"  /><img src="code\\output\\SeamCarving\\557_frames\\557_80.png"  /></div>

总之，Seam Carving算法是基于内容感知的图像缩放算法，通过上述实验不难发现，在图片缩小的过程中，图片主体部分得到了较好的保留，从而使得图片内容与信息得到了更好的保留。



-----------

## 二、 Graph-based image segmentation  

### 2.1 问题描述

结合“Lecture 7 Segmentation”内容及参考文献[1]，实现基于 Graph-based image segmentation 方法（可以参考开源代码，建议自己实现） ，通过设定恰当的阈值将每张图分割为 50~70 个区域，同时修改算法要求任一分割区域的像素个数不能少于 50 个（即面积太小的区域需与周围相近区域合并） 。结合GT 中给定的前景 mask，将每一个分割区域标记为前景（区域 50%以上的像素
在 GT 中标为 255）或背景（50%以上的像素被标为 0） 。区域标记的意思为将该区域内所有像素置为 0 或 255。要求对测试图像子集生成相应处理图像的前景标注并计算生成的前景 mask 和 GT 前景 mask 的 IOU 比例。假设生成的前景区域为 R1， 该图像的 GT 前景区域为 R2， 则IOU = (𝑅1∩𝑅2)/(𝑅1∪𝑅2)

### 2.2 求解过程与算法

假设有无向图$G=(V,E)$，每条边有权重$w(v_i,v_j)$表示距离，$S$是原图的子图，有：$S=G'=(V,E')\quad E'\sub E$，且将$G$分到成了不同的集群。使用谓词$D$决定是否存在分段边界，也就是说，使用$D$作为标准判断不同集群的相似性，如果两个集群的集群间相似性小于集群内的相似性，则进行合并：
$$
Merge(C_1,C_2)=\left\{\begin{matrix}
True,dif(C_1,C_2)<in(C_1,C_2)\\
False,otherwise
\end{matrix}\right.\\
dif(C_1,C_2)=\min_{v_i\in C_1,v_j\in C_2,(C_1,C_2)\in E}w(v_i,v_j)\\
in(C_1,C_2)=\min_{C\in\{C_1,C_2\}}[\max_{v_i,v_j\in C}[w(v_i,v_j)+\frac k{|C|}]]
$$
也就是说，如果两个集群中点的距离的最小值小于两个集群内的点的距离最大值更小的那一个则进行合并。其中$k/|C|$设置了内部节点的差异性。如果$k$较大，则集群规模往往更大，否则更小。

对于一张图像，我们可以将每个像素投影到特征空间$(x,y,r,g,b)$上，也就是坐标和颜色通道组成的特征空间。每个像素在八领域内与八个像素相邻，即具有边。边的距离由特征向量计算得出，一般用欧氏距离。

由此，我实现基于图的图像分割方法流程如下：

1. 将图片的每个像素按照坐标和颜色投影到$(x,y,r,g,b)$特征空间上，初始时每个像素自身属于单独一个区域
2. 计算所有边的权重大小，即八领域内像素的特征向量的欧式距离，并按照距离大小排序
3. 按距离从小到大的顺序，依次将这些边两端的像素合并到同一个区域。能否合并依据上述的$Merge(C_1,C_2)$的公式判断
4. 重复第3步，直到剩余区域数到达设置的下界
5. 遍历剩下的区域，将像素数少于50个的区域和相邻的区域直接合并

由此就能得到划分好区域的图片。我们只需要记录每个区域所含的全部像素的坐标，由这些坐标找到前景图的相应位置，统计前景像素数和背景像素数就能确定该区域应该被判定为前景还是背景。

### 2.3 代码实现与说明

该部分的代码全部由自己实现。

#### 2.3.1 一些功能模块的实现

在实现算法主体流程前，可以预见到，程序需要用多种方式刻画像素和像素、像素和区域之间的关系。为了之后代码的简洁性，我先实现了部分功能模块方便多次调用。首先需要两个全局变量：

```python
# 用于查询某个片段内部的所有像素
SEG_GROUP = dict()
# 每个片段内的最大距离
INNER_WEIGHT = dict()
```

其中`SEG_GROUP`是字典，用于表示区域以及查询区域内的全部像素。如果像素坐标为`[x,y]​`，则表示某个区域时，使用该区域中所有像素的`x`值最小的那个作为“代表”表示该区域。如果有多个`x`相同的像素，则找`y`值最小的。因此，`SEG_GROUP[(x1,y1)]=[(x1,y1),(x2,y2),...]`表示以`(x1,y1)`这个像素点为代表的区域中包含着`(x1,y1)`、`(x2,y2)`......这些像素点。该区域的键值只能用`(x1,y1)`表示，而不能用`(x2,y2)`等其他的像素点表示。因此`SEG_GROUP`的键值数量就表示了区域的数量。初始化时，该字典中包含所有像素坐标，且每个像素坐标对应的区域中只含有自己这一个像素。

而每个集合中需要计算集合内部的最大距离，即上述的$in(C_1,C_2)$中的$max(w(v_i,v_j))$，该值用`INNER_WEIGHT`表示，其键值也和上述的一样，用该区域的坐标最小的像素表示。实际的$in(C_1,C_2)$通过下面的函数实现：

```python
# 计算两个片段的片段内距离
def internalDif(coord1, coord2, img_array, segment_coord):
    global INNER_WEIGHT, SEG_GROUP
    coord1 = getSegment(coord1, segment_coord)
    coord2 = getSegment(coord2, segment_coord)
    k = 100
    dist1 = INNER_WEIGHT[(coord1[0],coord1[1])] + k/len(SEG_GROUP[(coord1[0],coord1[1])])
    dist2 = INNER_WEIGHT[(coord2[0],coord2[1])] + k/len(SEG_GROUP[(coord2[0],coord2[1])])
    return min(dist1, dist2)
```

上述关系描述了如何用一个“代表像素”找到其对应的区域，然后区域就能用`SEG_GROUP`来查询该区域中所有的像素了。然而这只能由区域查询到像素，并不能直接知道某个像素属于哪个区域，因此我们还需要另一个字典`segment_coord`表示像素的所属区域。`segment_coord[(x1,y1)]=(x2,y2)`表示像素`(x1,y1)`的区域和`(x2,y2)`相同。每个像素的`segment_coord`初始化为自己，当两个区域合并时，只需要将一个区域的代表像素的`segment_coord`指向另一个区域的任一像素即可。这样一来，对于合并的两个区域，总有一个区域的代表像素是不变的，因此其`segment_coord`值总是指向自身。如此一来，当一个像素满足`segment_coord[(xi,yi)]=(xi,yi)`时，我们就能知道：该像素为代表像素，从而找到了该区域。如果不是，则可以查询上一个像素的`segment_coord`，直到键值和所指向的值相同。通过上述的合并规则不难发现，像素查询其实是一个树状结构，我们总能通过`segment_coord`查询到一个像素所在区域的代表像素，即：

```python
# 查询一个像素所属的区域
def getSegment(coord, segment_coord):
    coord = np.array(coord)
    tmp = coord.copy()
    # 一直向上查询，直到找到代表像素
    while (segment_coord[coord[0]][coord[1]] != coord).any():
        coord = segment_coord[coord[0]][coord[1]]
    # 直接将上一个像素指向代表像素以加速之后查找
    segment_coord[tmp[0]][tmp[1]] = coord   
    return np.array((coord[0], coord[1]))
```

合并的代码如下，需要提供合并的两个区域分别的任一像素。`flag`用于控制是否更新区域内最大距离。在合并不足50个像素的区域时，因为之后不需要用到区域内最大距离，因此不进行计算，可以进行一定的加速。

```python
# 合并两个区域
def mergeSegment(coord1, coord2, img_array, segment_coord, flag=True):
    global INNER_WEIGHT, SEG_GROUP
    # 查询这两个像素所在区域的代表像素
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
    # 合并区域，删除原来的区域
    SEG_GROUP[(coord1[0],coord1[1])] += SEG_GROUP[(coord2[0],coord2[1])]
    del SEG_GROUP[(coord2[0],coord2[1])]
    return
```

有了上述操作后，我们可以通过查询两个像素所属区域的代表像素，通过二者的代表像素是否相同，来判断二者是否在同一个区域中。如果当前检索到的两个顶点属于同一个区域，则不需要进行合并操作。判断像素是否属于同一区域的代码如下：

```python
# 判断两个像素是否属于同一个区域
def isSameSegment(coord1, coord2, segment_coord):
    coord1 = getSegment(coord1, segment_coord)
    coord2 = getSegment(coord2, segment_coord)
    return (coord1 == coord2).all()
```

除此之外，还需要计算任意两个像素距离的函数。依据这两个像素的坐标和RGB颜色值，将二者转换到$(x,y,r,g,b)$空间，再计算欧氏距离，即特征向量各个分量相减后求平方和再开根即可，可以通过调用`numpy`模块中的范式功能实现，代码如下：

```python
# 计算两个相邻像素在特征空间(x,y,r,g,b)的欧式距离
def distance(coord1,coord2,img_array):
    vec1 = np.array([coord1[0],coord1[1],img_array[coord1[0]][coord1[1]][0],
            img_array[coord1[0]][coord1[1]][1],img_array[coord1[0]][coord1[1]][2]])
    vec2 = np.array([coord2[0],coord2[1],img_array[coord2[0]][coord2[1]][0],
            img_array[coord2[0]][coord2[1]][1],img_array[coord2[0]][coord2[1]][2]])
    return np.linalg.norm(vec1-vec2)
```

#### 2.3.2 分区算法实现的主体部分

算法实现的主体部分由函数`segment`实现。首先，对各个变量进行初始化操作，包括将区域数量初始化为总的像素数、将`segment_coord`字典初始化为各个像素自身的坐标、每个区域内部的距离为0：

```python
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
```

每次合并时，我们需要找到权值最小的边，将边两边的像素所属的区域进行合并。为了防止繁琐的权重计算和排序，我考虑一开始将所有的边的权重都计算出来，并且进行从小到大的排序，从而就能由小到大的权值依次遍历各个边，对像素区域进行合并：

```python
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
```

需要注意的是，所谓的“边”只能出现在某个像素的八邻域内，也就是说，如果不出界的话，每个像素只能和它左上、上、右上、左、右、左下、下、右下这八个相邻的像素连接。当遍历每个像素，将像素延伸出去的这八条边都考虑进去的话，每条边会计算两次，从而产生重复。考虑到每个条的表示方法为`[(顶点1坐标),(顶点2坐标),边的权重]`，遍历每个像素时只考虑它右边的和下面一排的共四个像素产生的边，这样可以保证每条边只计入一次，且顶点1和顶点2的坐标是按照升序顺序排列的。当然，边界情况要另外讨论。

然后就能开始进行图片的区域合并了。因为事先实现了上面的功能模块，这里基本只需要进行简单的调用即可。从小到大依次遍历各个边，如果该边的两端的顶点像素不属于同一个区域，且满足在理论部分提及的$Merge(C_1,C_2)$条件的话，就对二者进行合并。因为之后还要合并像素少于50个的区域，所以这里是对整个图片区域的初步划分，当区域数量小于一定值就退出循环。该值我对不同的图片进行了不同的设置，即代码中的` SEGMENT_NUM`变量：

```python
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
    t += 1
```

如此一来，就实现了区域的初步划分。然后需要将小于50个像素的区域进行合并操作。考虑到50个像素对于原图来说相当小，我选择将这类像素与相邻的区域进行随机合并。具体做法是，遍历该区域内的全部像素，如果当前像素的上、下、左、右相邻的像素与当前像素不属于同一个区域，则将二者的区域进行合并。具体实现如下：

```python
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
```

这里`flag`和`flag2`变量分别用于表示当前是否有小于50个像素的区域和循环是否是第一次启动。当像素所属区域合并时，遍历的字典`SEG_GROUP`的键值会改变，继续迭代访问键值会报错，因此合并后不能继续找下一个区域，而是需要重新遍历全部的区域。

到目前为止，整张图片的区域就已经划分完成了。在字典`SEG_GROUP`里记录了所有的区域（用代表像素表示），通过代表像素，也可以查询到每个区域内全部的像素。我将不同区域上了不同的颜色作为中间结果输出，此部分比较简单且与算法无关，就不在报告中赘述。

#### 2.3.3 依据分区和前景图给区域打标签

标记部分由下面的`segmentGround`函数实现。通过`SEG_GROUP`遍历每个区域，对于每个区域，遍历每个像素，查找这个像素在给出的前景图中的位置，为黑则`black`加一，为白则`white`加一，如果黑色更多则该区域全部划为黑色，否则为白色：

```python
# 标记前景背景
def segmentGround(ground):
    ground_array = np.array(ground).astype(np.int8)
    result = np.zeros(ground_array.shape).astype(np.int8)
    # 遍历每个区域
    for seg in SEG_GROUP.keys():
        black = 0
        white = 0
        # 统计该区域像素在前景图中的颜色
        for pixel in SEG_GROUP[seg]:
            if ground_array[pixel[0],pixel[1]] == 1:
                white += 1
            else:
                black += 1
        if white > black:
            for pixel in SEG_GROUP[seg]:
                result[pixel[0],pixel[1]] = 255
    return result
```

#### 2.3.4 计算IOU

该部分的代码被我在`IOUcalc.py`文件中实现了，和上面的代码不在同一份代码中。计算IOU，即利用上面的代码得到的前景图和实际的前景图，计算二者前景的交集和并集，再用交集大小除以并集大小。只需要遍历整张图片的全部位置，如果当前像素在两张图中全为白，则交集大小加一；如果当前像素在两张图中至少有一个为白，则并集大小加一，最终计算二者的商即可。代码实现如下：

```python
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
```

### 2.4 结果展示与分析

本题的IOU结果可以运行`IOUcalc.py`得到，图片结果放在下面的文件夹中：

> output\ImageSegmentation

结果展示如下，分别为原图、区域图、最终的前景图：

<div align="center"><img src="code\\data\\imgs\\57.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\57_1.png"  /><img src="code\\output\\ImageSegmentation\\57_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\157.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\157_1.png"  /><img src="code\\output\\ImageSegmentation\\157_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\257.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\257_1.png"  /><img src="code\\output\\ImageSegmentation\\257_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\357.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\357_1.png"  /><img src="code\\output\\ImageSegmentation\\357_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\457.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\457_1.png"  /><img src="code\\output\\ImageSegmentation\\457_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\557.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\557_1.png"  /><img src="code\\output\\ImageSegmentation\\557_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\657.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\657_1.png"  /><img src="code\\output\\ImageSegmentation\\657_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\757.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\757_1.png"  /><img src="code\\output\\ImageSegmentation\\757_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\857.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\857_1.png"  /><img src="code\\output\\ImageSegmentation\\857_2.png"  /></div>

<div align="center"><img src="code\\data\\imgs\\957.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\957_1.png"  /><img src="code\\output\\ImageSegmentation\\957_2.png"  /></div>

最终计算得到的IOU结果如下：

<img src="pic\\2.png" style="zoom: 50%;" />

总的来说，结果有好有坏。对于较好的结果，如下图所示（编号657的图片），可以看出，前景部分，即图片中的主体，拥有大块的相同颜色的区域，且能够和背景区分开来。消防栓为大片的白色，两边的手套为天蓝色，而背景确实大片的绿地和后面的灰色地板：

<div align="center"><img src="code\\data\\imgs\\657.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\657_2.png"  /></div>

而对于下面的效果较差的图片（编号957的图），图中的动物和所在的树枝颜色极为相近，很容易混淆。相对来说，右下的树叶和右上的墙体颜色区分更加明显，也就更容易被划分出来：

<div align="center"><img src="code\\data\\imgs\\957.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\957_2.png"  /></div>

而对于下面的图（编号为57的图），还可以发现一点：图中左边的黑猫、两只鹅因为全身颜色相近，猫为黑，鹅为白，且与背景有明显区别，因此被区分出来，效果较好。而下方的花猫，身上的花纹颜色多变，容易在分区时被分成许多小块，然后在像素数少于50个的区域进行合并时，合并到背景所属的区域中，因此效果较差。

<div align="center"><img src="code\\data\\imgs\\57.png" style="zoom:100%;" /><img src="code\\output\\ImageSegmentation\\57_2.png"  /></div>

从上面三张图片的分析，不难看出，该基于图的图片分区算法的确能有效对图片内容进行划分，但总的来说，更加适合图片主体颜色较为单一、且主体与背景颜色有明显不同的情况。



## 三、Visual Bag of Words  

### 3.1 问题描述

从训练集中随机选择 200 张图用以训练，对每一张图提取归一化 RGB颜色直方图（8\*8\*8=512 维），同时执行问题 2 对其进行图像分割，（分割为 50~70个区域） ，对得到的每一个分割区域提取归一化 RGB 颜色直方图特征（维度为8\*8\*8=512），将每一个区域的颜色对比度特征定义为区域颜色直方图和全图颜色直方图的拼接，因此区域颜色区域对比度特征的维度为 2\*512=1024 维，采用PCA 算法对特征进行降维取前 20 维。 利用选择的 200 张图的所有区域（每个区域 20 维特征） 构建 visual bag of words dictionary （参考 Lecture 12. Visual Bag of Words 内容），单词数（聚类数）设置为 50 个， visual word 的特征设置为聚簇样本的平均特征，每个区域降维后颜色对比度特征（20 维） 和各个 visual word的特征算点积相似性得到 50 个相似性值形成 50 维。将得到的 50 维特征和前面的 20 维颜色对比度特征拼接得到每个区域的 70 维特征表示。 根据问题 2，每个区域可以被标注为类别 1（前景：该区域 50%以上像素为前景）或 0（背景：该区域 50%以上像素为背景）， 选用任意分类算法（SVM， Softmax，随机森林， KNN等）进行学习得到分类模型。最后在测试集上对每一张图的每个区域进行测试（将图像分割为 50~70 个区域，对每个区域提取同样特征并分类） ， 根据测试图像的GT， 分析测试集区域预测的准确率。  

### 3.2 求解过程与算法

首先需要将所有图片提取RGB颜色直方图。对于每张图片，统计其不同RGB色彩值像素的个数，最后将结果除以像素的总个数即可归一化。然后将这些图片分区，分区的方法和第二题相同。再统计每个区域的RGB颜色直方图。将每个分区的结果拼接上整张图的结果，共1024维。同时，在分区操作时，我们也能得到每个区域属于前景还是背景，即训练样本的标签。这也是已经通过第二题实现了的部分。

对于上面得到的1024维特征向量，需要通过PCA降维来提取前20维。将所有特征向量作为列向量，横向拼接形成矩阵，记为矩阵$A$。对其进行奇异值分解，有：
$$
\bold A=\bold U\bold \Sigma\bold V^T
$$
其中$\bold U=[\bold u_1,...,\bold u_M]$，$\bold V=[\bold v_1,...,\bold v_N]$。满足：$\bold u_i$和$\bold v_i$是$\bold A\bold A^T$和$\bold A^T\bold A$的第$i$个特征向量，$\bold u^T_i\bold u_j=\bold v_i^T\bold v_j=\delta_{ij}$。$\bold \Sigma$是对角矩阵，对角线上的值为$\bold A\bold A^T$和$\bold A^T\bold A$的特征值开根号，称为奇异值，按降序排列。因为它是对角矩阵，所以：
$$
\bold A=\bold U\bold \Sigma\bold V^T=\sum^r_{i=1}\Sigma_{ii}\bold u_i\bold v_i^T
$$
其中$r$是该对角矩阵的对角线元素个数。

如果将样本中心化$\tilde X=[\bold x^{(1)}-\overline x,\bold x^{(N)}-\overline x]$则有：$\tilde X\tilde X^T=NS$，它和矩阵S含有相同特征向量。因此，对$\tilde X$做奇异值分解，可以得到样本的主要方向。如果只取特征值矩阵的前20个特征值，最后$\sum^{20}_{i=1}\Sigma_{ii}\bold u_i\bold v_i^T$得到的结果就是PCA降维后的特征值矩阵。

通过上述的PCA操作，我们可以将1024维的特征向量降维到20维。然后，我们对这些向量进行K平均聚类，即K-means操作，从而可以得到一个聚类模型。模型的聚类数量为50。具体实现方法为：在样本集中，随机选取K个点作为中心$\bold \mu_k$，计算每个样本到中心点的距离，并将样本划分到离它最近的那个点的集群中。使用变量$r_{nk}$表示数据样本$\bold x^{(n)}$是否属于集群k：
$$
r_{nk}=\left\{\begin{matrix}1,k=arg\min_j||\bold x^{(n)}-\mu_j||^2\\0,otherwise\end{matrix}\right.
$$
对于每个集群，用所有样本的平均位置更新中心点的位置：
$$
\mu_k=\frac{\sum^N_{n=1}r_{nk}\bold x_n}{\sum^N_{n=1}r_{nk}}
$$
重复上面的样本分配和中心更新过程，最终就能得到这50个聚类中心。

将上述的聚类中心和每个特征向量计算点积相似性，可以得到50个值。将这50个值加到原来的2维特征向量后，形成了新的70维特征向量，然后用这些向量训练一个KNN模型，即K近邻模型：将测试数据的特征与训练集数据的特征进行比较，找到K个最相似的数据，用这K个数据的标签决定测试数据的标签。

同样将测试数据通过上述计算归一化RGB直方图的操作、用相同的PCA模型进行降维、和上面已经得到的K平均聚类中心点计算点积相似度，最后在KNN模型中就能预测测试样本的标签了。

### 3.3 代码实现与说明

对于上面所述的PCA模型、K-means模型、KNN模型，我使用了python的`sklearn`库实现。如果没有该库程序运行会报错。

#### 3.3.1 归一化RGB直方图的计算

首先随机选择200张图片，每张图片计算整体的归一化RGB直方图，再分区后计算每个区域的归一化RGB直方图。因此，需要实现两个功能：给定图片，直接计算直方图，以及给定用像素集合表示的区域，计算这个像素集合的直方图。

计算图片的归一化RGB直方图时，只需要遍历图片的每一处，统计该位置的像素的RGB值，该值对应的RGB值计数加一，即可得到RGB直方图。最后，将所有计数再除以像素总数以归一化：

```python
# 计算图片的归一化RGB直方图
def getPictureHistogram(img):
    img_array = np.array(img)
    histogram = np.zeros((8,8,8))
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            histogram[img_array[i][j][0]//32,img_array[i][j][1]//32,img_array[i][j][2]//32] += 1
    histogram /= np.sum(histogram)  # 归一化
    return histogram.reshape(-1)
```

计算像素集合的归一化RGB直方图大同小异，只是遍历方式由图片的坐标遍历改为了对集合的遍历：

```python
num = 0
for seg in SEG_GROUP.keys():
    black = 0
    white = 0
    for pixel in SEG_GROUP[seg]:
        if ground_array[pixel[0],pixel[1]] == 1:
            white += 1
        else:
            black += 1
            histograms[num,img_array[pixel[0],pixel[1],0]//32,            img_array[pixel[0],pixel[1],1]//32,img_array[pixel[0],pixel[1],2]//32] += 1
    histograms[num] /= np.sum(histograms[num])  # 直方图归一化
```

#### 3.3.2 初始数据的生成

生成初始数据即将200张图，并分区，计算整张图与各个区域的归一化RGB直方图并进行变形和拼接，得到初始的训练样本与标签。这里需要花费大量的时间，因此我在程序入口处加入了一个变量控制数据生成：

```python
gen_new_data = False    # 是否新生成训练数据
```

该变量为`True`时，会进行数据的生成，并且在最后保存生成的初始数据：

```python
np.save('statistics\\histograms_total.npy',histograms_total)
np.save('statistics\\labels_total.npy',labels_total)
```

该变量为`False`时，可以直接读入之前运行程序生成好的训练数据，从而加速运行：

```python
histograms_total = np.load('statistics\\histograms_total.npy')
labels_total = np.load('statistics\\labels_total.npy')
```

整个程序的运行过程，有两个矩阵存储数据。`histograms_total`用于存储训练数据，其维度为$num*1024$，其中`num`为训练样本数，即这200张图分区后的区域总数，`1024`为每个样本的维数。`labels_total`用于存储训练样本对应的标签，第一维的下标与`histograms_total`一一对应，每个样本对应一个一维的标签，标签为1表示前景，否则为0，表示背景。

对于每张图，通过调用下面的函数分别得到整张图的直方图和该图各个分区的直方图与标签：

```python
img = Image.open("data\\imgs\\"+str(pic_id)+".png")       # 原图
ground = Image.open("data\\gt\\"+str(pic_id)+".png").convert('1')    # 前景背景图，转化为黑白图
histogram = getPictureHistogram(img)   # 获取整幅图的归一颜色直方图
histograms, labels = segment(img, ground)   # 分区并获取各个区域的颜色直方图和标签
```

其中`segment`函数和第二题基本一致，只是后面加上了对区域求RGB直方图和标签的代码，不再赘述。变量`histogram`和`labels`分别表示当前图片得到的训练样本和标签。将二者进行变形后，就可以加入总的样本矩阵中：

```python
# 将直方图转换为特征向量
for i in range(histograms.shape[0]):
    tmp = np.hstack((histograms[i].reshape(-1),histogram))
    histograms_total = np.vstack((histograms_total,tmp))
labels_total = np.vstack((labels_total,labels.reshape(-1,1)))
```

#### 3.3.2 PCA、K-means和KNN模型的建立

这里的模型都通过调用`sklearn`库建立与训练。

首先是PCA操作，通过`fit_transform`能同时进行PCA模型的训练和将训练数据转换成降维结果，将原本的1024维降维到20维：

```python
pca = decomposition.PCA(n_components=20)
histograms_total = pca.fit_transform(histograms_total)
```

然后通过K-means模型，将样本分为50类：

```python
# 使用K-means将样本分为50类
kmeans = KMeans(n_clusters=50)
kmeans.fit(histograms_total)
cluster_centers = kmeans.cluster_centers_.copy()# 获取分类中心
```

计算每个样本和分类中心的点积相似性，即余弦相似度，得到50维结果，加到原本的20维特征向量中，形成70维特征向量：

```python
# 计算余弦相似度
cosine_sim = np.dot(histograms_total, cluster_centers.reshape(20,50)) / \
np.dot(np.linalg.norm(histograms_total, axis=1).reshape(-1,1), np.linalg.norm(cluster_centers, axis=1).reshape(1,-1))
# 将50维余弦相似度加到20维对比度后，形成70维特征
histograms_total = np.hstack((histograms_total, cosine_sim))    
    
```

最后，用这些特征向量与它们对应的标签，训练KNN模型：

```python
# 将50维余弦相似度加到20维对比度后，形成70维特征
histograms_total = np.hstack((histograms_total, cosine_sim))    
# 用这些样本与标签建立KNN模型
knn = KNeighborsClassifier()
knn.fit(histograms_total, labels_total.reshape(-1))
```

#### 3.3.3 测试样本的处理与测试

为了方便程序执行，我在做第二问的时候，将每一张图片的`SEG_GROUP`结果都保存下来了，只需要将分区结果读入就能很快进行RGB直方图的计算而不需要重新分区：

```python
seg_group=np.load('statistics\\SEG_GROUP_'+str(i)+'.npy',allow_pickle=True).item()      
```

测试图片获取RGB直方图特征的方法与训练图片一致，不再赘述。测试样本与标签分别被存储在矩阵`test_samples`和`test_labels`中，格式与上面的测试样本与标签一致。

因为模型都已经训练好，我们只需要用这些模型依次处理测试样本，就能得到最终的预测结果：

```python
# 用训练好的pca模型降维
test_samples = pca.transform(test_samples)
# 计算余弦相似度
cosine_sim = np.dot(test_samples, cluster_centers.reshape(20,50)) / \
np.dot(np.linalg.norm(test_samples, axis=1).reshape(-1,1), np.linalg.norm(cluster_centers, axis=1).reshape(1,-1))
# 将50维余弦相似度加到20维对比度后，形成70维特征
test_samples = np.hstack((test_samples, cosine_sim))
# 用训练好的knn模型预测结果
predict_labels = knn.predict(test_samples)
```

最后比较预测结果与实际标签即可：

```python
total = predict_labels.shape[0]
right = np.sum(test_labels.reshape(-1) == predict_labels)
print('总计有'+str(total)+'个区域，其中前景背景预测正确的有'+str(right)+'个')
print('准确率为：',right/total)
```

### 3.4 结果展示与分析

最终得到的结果如下：

<img src="pic\\3.png" style="zoom:67%;" />

需要说明的是，如果要让每张图片划分的区域为50~70个的话需要针对不同的图片对第一次分区的区域数目与判断区域是否能够合并时公式中的$k$值进行调参，但为了使得整个过程统一化，对整个200张图片的样本，我使用了同一套参数，可能会导致部分图片最终的区域数不在50~70个内。

总的来说，最终结果的准确率到达了79.54%，说明这套方法对图片前景背景的预测的确有较好的效果。本题在视觉词袋的框架下，涉及到了降维处理、聚类算法与分类决策算法，是一道综合性较强的题目。通过PCA降维将1024维的特征向量直接降至20维，通过K-means算法将不同的数据进行分类，将这些特征集合作为词袋，最终通过KNN算法找出和测试数据最相近的训练数据，通过训练数据的标签反推测试数据的标签，一套流程下来，仍有较好的结果，充分说明了这些模型和算法的有效性。