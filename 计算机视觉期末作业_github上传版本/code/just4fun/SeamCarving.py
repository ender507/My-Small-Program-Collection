from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt

frame = 0   # gif的帧号

def imSave(pic, num, save_path):
    '''展示1s的图片
    plt.get_current_fig_manager().window.state('zoomed')
    plt.imshow(pic)
    plt.ion()
    plt.pause(1)
    plt.close()
    '''
    # 保存
    pic.save(save_path+str(num)+'.png')


# 选择路径，即选择三个值中最小的那一个
def choosePath(num1, num2, num3):
    if num1 == num2 and num2 == num3:
        return 0    # 三者相等优先考虑num2，防止数组越界
    if num1 == min(num1, num2, num3):
        return -1   # num1最小则返回-1
    elif num2 == min(num1, num2, num3):
        return 0    # num2最小则返回0
    else:
        return 1    # num3最小则返回1
    
  
# 删除竖缝（减小图片宽度）
def widthCarve(img, ground, new_width, save_frames, mode):
    global frame  
    while True:
        width = img.size[0]
        # 宽度达到要求则退出循环
        if width == new_width:
            break

        # 单次删除接缝的变量初始化
        img_array = np.array(img).astype(np.int16)
        ground_array = np.array(ground).astype(np.int16)
        # 使用梯度图作为能量图
        red_gradient = np.array(np.gradient(img_array[:,:,0]))
        red_gradient = np.maximum(red_gradient, -red_gradient)
        green_gradient = np.array(np.gradient(img_array[:,:,1]))
        green_gradient = np.maximum(green_gradient, -green_gradient)
        blue_gradient = np.array(np.gradient(img_array[:,:,2]))
        blue_gradient = np.maximum(blue_gradient, -blue_gradient)
        energy_map = red_gradient[0] + red_gradient[1] + green_gradient[0] + green_gradient[1]
        + blue_gradient[0] + blue_gradient[1]
        energy_map = np.array(energy_map).astype(np.int16)
        cumulate_energy = np.zeros(energy_map.shape)    # 累计能量图，使用动态规划更新的对象
        path = np.zeros(energy_map.shape).astype(np.int16)      # 路径图，记录最少能量的路径
        new_img = np.zeros((energy_map.shape[0],energy_map.shape[1]-1,3)).astype(np.int16) # 删除接缝后的图片
        new_ground = np.zeros((energy_map.shape[0],energy_map.shape[1]-1)).astype(np.int16) # 删除接缝后的前景背景图
        
        # 使用动态规划方法查找能量最少的路径
        # 第一行直接赋值
        cumulate_energy[0,:] = energy_map[0,:]  # 累计能量图和能量图的第一行相同
        path[0,:] = -1      # 第一行路径为-1表示路径终止
        # 其余位置进行动态规划求解
        for i in range(1, img.size[1]):
            for j in range(img.size[0]):
                # 计算三个方向的累计能量并记录路径
                left = right = mid = 255 * img.size[0] * img.size[1]
                if j == 0:  # 第一列不能有从左边来的路径
                    right = cumulate_energy[i-1,j+1] + energy_map[i,j]
                    mid = cumulate_energy[i-1,j] + energy_map[i,j]
                elif j == img.size[0]-1:  # 最后一列不能有从右边来的路径
                    left = cumulate_energy[i-1,j-1] + energy_map[i,j]
                    mid = cumulate_energy[i-1,j] + energy_map[i,j]
                else:
                    #这一段是backward SeamCarving
                    '''
                    left = cumulate_energy[i-1,j-1] + energy_map[i,j]
                    mid = cumulate_energy[i-1,j] + energy_map[i,j]
                    right = cumulate_energy[i-1,j+1] + energy_map[i,j]
                    '''
                    left = cumulate_energy[i-1,j-1] + abs(energy_map[i,j+1] - energy_map[i,j-1]) + abs (energy_map[i-1,j] - energy_map[i,j-1])
                    mid = cumulate_energy[i-1,j] + abs(energy_map[i,j+1] - energy_map[i,j-1])
                    right = cumulate_energy[i-1,j+1] + abs(energy_map[i,j+1] - energy_map[i,j-1]) + abs (energy_map[i-1,j] - energy_map[i,j+1])

                # 找到累计能量最小的路径，记录累计能量和路径
                p = choosePath(left, mid, right)
                cumulate_energy[i,j] = (left, mid, right)[p+1]
                # 如果当前像素是前景，则加入惩罚，即增加当前能量
                if ground_array[i,j] == 1:
                    cumulate_energy[i,j] += 2550
                path[i,j] = j+p
        
        # 找到并删除接缝（即上述路径）
        # 先找到能量最小的路径的最后一个像素点位置
        # 将原图中的接缝重新上色并保存，作为gif的一帧
        pos = pos2 = np.argmin(cumulate_energy[-1,:])
        for i in range(img.size[1]-1, -1, -1):
            img_array[i, pos2, 0] = 0
            img_array[i, pos2, 1] = 0
            img_array[i, pos2, 2] = 255
            pos2 = path[i, pos2]
        if save_frames != -1:   # 保存gif的一帧
            if mode == 1:
                imSave(Image.fromarray(img_array.astype('uint8')).convert('RGB'),
                   str(save_frames)+'_'+str(frame), "gif\\")
            else:
                imSave(Image.fromarray(img_array.astype('uint8')).convert('RGB').transpose(Image.TRANSPOSE),
                   str(save_frames)+'_'+str(frame), "gif\\")

        frame += 1
        
        # 删除接缝并赋值回原图片
        for i in range(img.size[1]-1, -1, -1):
            bias = 0
            for j in range(img.size[0]-1):
                if j == pos:
                    bias = 1
                new_img[i,j,:] = img_array[i,j+bias,:]
                new_ground[i,j] = ground_array[i,j+bias]
            pos = path[i, pos]
        img = Image.fromarray(new_img.astype('uint8')).convert('RGB')
        ground = Image.fromarray(255*new_ground.astype('uint8')).convert('1')
        if save_frames != -1:   # 保存gif的一帧
            if mode == 1:
                imSave(img, str(save_frames)+'_'+str(frame),
                       "gif\\")
            else:
                imSave(img.transpose(Image.TRANSPOSE), str(save_frames)+'_'+str(frame),
                       "gif\\")
        frame += 1
    return img, ground

def heightCarve(img, ground, new_height, save_frames):
    img = img.transpose(Image.TRANSPOSE)
    ground = ground.transpose(Image.TRANSPOSE)
    img, ground = widthCarve(img, ground, new_height, save_frames, 2)
    img = img.transpose(Image.TRANSPOSE)
    ground = ground.transpose(Image.TRANSPOSE)
    global frame
    frame = 0
    return img, ground

if __name__ == '__main__':
    # 针对不同的图片，设置不同的宽高放缩比例
    img = Image.open("1.jpg")       # 原图
    # ground = Image.open("2.jpg").convert('1')    # 前景背景图，转化为黑白图
    ground = Image.new("1", img.size, "#000000")
    # 计算输出图片的大小
    size = img.size
    back_ground = np.sum(np.array(ground) == 0)
    rate = 0.5
    pic_rate = 0.5
    new_size = (int(size[0]*(rate**pic_rate)), int(size[1]*(rate**(1-pic_rate))))
    # 先减小宽度
    img, ground = widthCarve(img, ground, new_size[0], 1, 1)
    # 再减小高度
    img, ground = heightCarve(img, ground, new_size[1], 1)
    imSave(img, 1, "")
        
    
    
