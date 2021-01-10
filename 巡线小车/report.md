# 巡线小车实验报告-第35组

| 姓名 | 学号     | 年级班级           | 工作                             |
| ---- | -------- | ------------------ | -------------------------------- |
|      | 18340055 | 18级计算机科学二班 | 地图搭建、代码改进、撰写实验报告 |
|      | 18340057 | 18级计算机科学二班 | 代码编写、测试、撰写实验报告     |

## 一、 实验原理

本次实验我们采用比例、积分、微分控制, 即 PID 控制, 来对小车的巡线功能进行调节, 更好地控制小车转向时左右两个车轮的速度。该算法的原理如下:

### 1.1比例控制 (P)

比例控制是一种最简单的控制方式。其控制器的输出与输入误差信号成比例关系, 当仅有比例控制时系统输出存在稳态误差。

### 1.2 积分控制 (I)

在积分控制中, 控制器的输出与输入误差信号的积分成正比关系。对一个自动控制系统, 如果在进入稳态后存在稳态误差, 则称这个控制系统是有稳态误差的。为了消除稳态误差, 在控制器中必须引入“积分项”。积分项对误差取决于时间的积分, 随着时间的增加, 积分项会增大。这样, 即便误差很小, 积 分项也会随着时间的增加而加大, 它推动控制器的输出增大使稳态误差进一步减小, 直到接近于零。因此, 比例+积分 (PI) 控制器, 可以使系统在进入稳态后几乎无稳态误差。

### 1.3 微分控制 (D)

在微分控制中, 控制器的输出与输入误差信号的微分（即误差的变化率）成正比关系。自动控制系统在克服误差的调节过程中可能会出现振荡甚至失稳。其原因是由于存在有较大惯性组件或有滞后组件, 具有抑制误差的作用, 其变化总是落后于误差的变化。解决的办法是使抑制误差的作用的变化“超前”, 即在误差接近零时, 抑制误差的作用就应该是零。这就是说, 在控制器中仅引入 “比例”项往往是不够的, 比例项的作用仅是放大误差的幅值, 而需要增加的是“微分项”, 它能预测误差变化的趋势, 这样, 具有比例 + 微分的控制器, 就能 够提前使抑制误差的控制作用等于零, 甚至为负值, 从而避免了被控量的严重超调。所以对有较大惯性或滞后的被控对象, 比例+微分 (PD) 控制器能改善系统在 调节过程中的动态特性。

PID 中比例控制 P 是主要的控制方法, 承担了 PID 控制中的大部分任务, 为了消除比例控制 P 留下的静态偏差, 增加了积分控制 I, 而微分控制 D 只为稳定而存在, 其稳定效果应该大于积分控制 I 的失稳效果, 在有大量噪音的系统中, 不适用微分控制 D。PID 控制器是一个完整的三项控制, 能够减少上升空间, 消除静态误差, 减少超调。

------

## 二、 代码实现

### 2.1 准备工作

本次实验我们使用了`V-REP`提供的`matlab`接口实现巡线小车。

`V-REP`会默认造在本地地址的19997端口开放。在`matlab`代码中实现对该端口的连接：

```matlab
% 初始化v-rep接口组件
vrep = remApi('remoteApi');     % using the prototype file (remoteApiProto.m)
vrep.simxFinish(-1);            % just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1',19997,true,true,5000,5);
if clientID < 0
    disp('Failed connecting to remote API server');    
```

同时将`V-REP`的接口文件`remApi.m`、`remoteApiProto.m`和动态链接库`remoteApi.dll`放置在`matlab`代码文件`LineFollowingBot.m`的同一文件夹下，则可以用`matlab`控制`V-REP`的仿真。

使用`matlab`启动仿真：

```matlab
vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot);
```

要实现巡线小车，需要获取小车前置摄像头的画面，依据画面进行速度的调整。小车有左、右两边的轮子可以控制。要先获取两边速度和摄像头的句柄，从而之后能对它们进行读取和修改：

```matlab
% 获取速度和图片的句柄
[res, motorLeft] = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_blocking);
[res, motorRight] = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_blocking);
[res, camera] = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_blocking);
```

控制小车使用PID算法，在这里，我们只考虑当前的误差比例和误差微分。先将当前误差初始化为0：

```matlab
err = 0;
```

接下来，在无限循环中，获取小车的画面并通过画面进行调整。获取画面的代码如下：

```matlab
code = 1;
while code
	[code, size, img] = vrep.simxGetVisionSensorImage2(clientID, camera, 1, vrep.simx_opmode_oneshot);
end
```

为了便于操作，调用`simxGetVisionSensorImage2`函数，使用句柄`camera`，直接返回黑白画面。如果图像获取成功，则返回值`code`为0，退出循环，否则获取失败，重新获取。

### 2.2 当前的误差分析

调用`getErr`函数获取当前误差和转向方向：

```matlab
[new_err, direct_tmp] = getErr(img);
```

当前误差`new_err`为利用PD算法控制速度的依据，而`direct_tmp`为之后的转向提供方向判断，之后会详细说明。

`getErr`的具体实现如下。函数原型为：

```matlab
function [err, direct] = getErr(img)
```

输入黑白图像`img`，返回小车当前和预期位置的误差和转向判断值`direct`。

考虑到小车的画面中会出现很多条路，而我们只期望小车走它脚下的路，因此我们希望对所有画面中的路进行一个误差分析：路的位置和小车脚下（即画面中点）的距离作为误差值，如此一来，依据路离中点的远近，就能判断它是否是小车要走的路。需要注意的是，路可能在中点位置的左边或右边，因此误差有正有负。要取误差的绝对值作为判断依据。在所有的路中，有两条路是我们值得关注的（如果画面只有一条路或者没有路，会采取单独的策略）：一是离中点最近的路，也就是误差的绝对值最小的路。期望中，小车正在走的路往往正在脚下，因此这条路就是小车在走的路，我们希望小车继续沿着这条路走。二是离中点第二近的路。试想：如果出现了急转弯（角度大于90度的转弯），在逐渐接近转弯点时，小车会看见两条路：转弯前要走的路和转完后要走的路。到达转弯点，两条路合并为一条，再往前走则会偏移当前道路。因此需要判断什么时候进行急转弯、急转弯是左转还是右转。通过分析不难得到：转弯的方向就是转完后要走的路的位置，在左边则左拐，在右边则右拐。而正在转弯前的路和转完后的路迟早会汇合，因此转弯后的路迟早会变为距离中点第二近的路，**以此就能判断急转弯的转弯方向**。

那么如何计算路到画面中点的距离呢？考虑到路是有宽度的，可以找路的最左边和最右边的点的坐标，取均值作为路的位置。而画面大小为480*640，因此取640的一半320作为画面的中点。画面中越靠下的部分离小车越近，因此依据下面画面调整小车状态的优先级更高。我们考虑从下往上一行行遍历，如果当前行找到了路则进行误差分析，否则看上一行是否有路。**这样一来就能有效处理间断路的问题。**

首先初始化以下几个变量：

```matlab
err = 1000000;
err2 = 1000000;
flag = 0;
direct = 0;
distance = 480;
```

其中`err`表示离中点最近的路的误差，`err2`表示离中点第二近的路的误差。注意误差可正可负，其绝对值表示到终点的距离。`direct`用于记录下一个急转弯预期的转向方向，为1或-1。如果没有转弯倾向则为0。因为找到一条路的当前位置，要找到路的左边和右边两个端点的坐标，`flag`用来表示下一个是寻找左边端点（值为0）还是右边端点（值为1）。`distance`表示当前遍历的画面的行号，从最后一行480行开始，依次往上遍历。

如果当前行没有找到路，则误差`err`不会更新，则需要找画面上一行，因此对`err`的值做一个循环判断：

```matlab
while err == 1000000
```

虽然路是黑色的，即预期画面中的数值为0，但可能会有些许误差，因此我将低于20的像素值认为是路。从画面最左边遍历到最右边，进行如下判断：如果找到了像素值小于20的点，即找到了路，且`flag`为0，表示正在找路的左端点，则认为找到了，更新`flag`并记录左端点位置，赋值为`l`。否则，如果找到了像素值大于20的点，表示当前位置不再是路，且`flag`为1，则认为找到了右端点。记录坐标。此时，就已经找出了画面中一条路的左端点和右端点。二者的均值减去画面中心的坐标320作为其位置误差：

```matlab
for i = 1:640
	if img(distance, i) < 20 && flag == 0
		l = i;
		flag = 1;
	end
	if img(distance, i) >20 && flag == 1
		r = i;
		flag = 0;
		dis = (r + l) / 2 - 320;
```

接下来依据误差值`dis`对`err`和`err2`进行更新。如果`dis`的绝对值小于`err`，说明新找到的路径就是离中点最近的路径。如果`err`还是初值1000000，则是找到的第一条路，还没有找到第二条最近的路，`direct`为0。

```matlab
if abs(dis) < abs(err)
	if err == 1000000
		direct = 0;
```

否则，新的路成为最近的路，原先最近的路成为第二近的路，需要对`err2`和`direct`进行更新：

```matlab
elseif err < 0
	err2 = err;
	direct = -1;
else
	err2 = err;
	direct = 1;
end
```

当然，最后还要对`err`进行更新：

```matlab
err = dis;
```

再或者，新路是当前第二近的路，则直接用新路的误差进行`err2`和`direct`的更新：

```matlab
elseif abs(dis) < abs(err2)
	err2 = dis;
	if err2 < 0
		direct = -1;
	else
		direct = 1;
	end                   
end
```

如果当前行没有找到路，则考虑画面的上一行，对`distance`进行递减。但是我们不希望对太远的地方的路进行判断，导致过远的路影响正常判断，因此到画面的上半部分则直接退出循环，不予考虑：

```matlab
distance = distance - 1;
if distance <= 320
	break
end
```

如此一来，就得到了当前的误差`err`与下次急转弯的预期转弯方向`direct`，并进行返回。

### 2.3 PD算法控制小车速度

控制速度时，我们只考虑比例和微分部分。因为路径状况不稳定，不同的位置有不同的状态，因此积分控制可能会导致错误。

如果`direct_tmp`为0，说明其不带有方向性，不更新实际的方向`direct`：

```matlab
if direct_tmp ~= 0
	direct = direct_tmp;
```

接下来就是PD算法的主体实现部分了。设定速度的基础值为`1.2`，比例和微分控制常量分别为`0.02`和`0.001`，计算速度的校正值：`delta_v = kp * new_err + kd * (new_err - err);`。考虑到误差值的正负表示转弯方向的左右，因此校正值的正负也是表示方向左右，也就是左右轮的速度差。得到矫正值后，左右轮速度分别为`v + delta_v`和`v - delta_v`。

```matlab
v = 1.2;
kp = 0.02;
kd = 0.001;
% PD算法计算速度差
delta_v = kp * new_err + kd * (new_err - err);
err = new_err;
% 更新速度
vrep.simxSetJointTargetVelocity(clientID, motorLeft, v + delta_v, vrep.simx_opmode_oneshot);
vrep.simxSetJointTargetVelocity(clientID, motorRight, v - delta_v, vrep.simx_opmode_oneshot);
```

如此一来，小车就能正常依据画面状况来控制左右轮子的速度，从而实现寻路了。

### 2.4 对急转弯的单独讨论

实现上述算法后，在急转弯时小车并不能正确运行。这是因为依据我们的算法，急转弯的尽头小车依旧会找到路从而直走而不会转弯，从而冲出赛道，到达画面中看不到路径的地方。这样一来，就应该进行原地转弯找回原来的路。原来的路的方向就是我们之前的参数`direct`指定的方向。

画面中首次出现路时，往往在画面的最边缘，这时恢复原来的算法可能导致转向速度异常。因此我们考虑重复获取画面与转向，直到画面中心的最下面出现路，可以沿直线走位为止。

具体实现代码如下：

```matlab
if min(min(img(:,:))) > 20
	% 进行旋转
	vrep.simxSetJointTargetVelocity(clientID, motorLeft, direct, vrep.simx_opmode_oneshot);
	vrep.simxSetJointTargetVelocity(clientID, motorRight, -direct, vrep.simx_opmode_oneshot);
	% 旋转到画面的中间出现出现路为止
	while img(480,320) > 20
	code = 1;
		while code
			[code, size, img] = vrep.simxGetVisionSensorImage2(clientID, camera, 1, vrep.simx_opmode_oneshot);
		end
	end
	% 更新误差
	err = 0;
	new_err = 0;
```

至此，小车的寻路算法已经基本实现。

----

## 三、 实验结果

### 3.1 地图设计

我们设计的地图如下所示：

<img src="pic\\1.png" style="zoom:50%;" />

其中，有以下几个难点：

1. 间断点

<img src="pic\\2.png" style="zoom:50%;" />

2. 迷惑路径（注意下方的圆是期望不会走的路径，小车应该沿直线前进）

<img src="pic\\3.png" style="zoom:50%;" />

3. 交叉路径

<img src="pic\\4.png" style="zoom:50%;" />

4. 连续急转弯

<img src="pic\\5.png" style="zoom:50%;" />

### 3.2 小车运行结果

首先，小车能平稳通过间断点：

<img src="pic2\\1.png" style="zoom:50%;" />

在遇到迷惑路径时，小车能够优先选择离中点进的路径，即转向要求小的路径，而不会进入中间的圆：

<img src="pic2\\2.png" style="zoom:50%;" />

<img src="pic2\\3.png" style="zoom:50%;" />

同样在交叉路径，能够正确选择路径：

<img src="pic2\\4.png" style="zoom:50%;" />

<img src="pic2\\5.png" style="zoom:50%;" />

而在连续急转弯的部分，和我们预期的一样，小车在急转弯尽头能依据之前画面得出的`direct`得到正确的转向方向，从而沿着正确的路径行走：

<img src="pic2\\6.png" style="zoom:50%;" />

最终完成整个路径，小车的用时为91秒（见下面控制台的输出值）：

![](pic2\\a.png)