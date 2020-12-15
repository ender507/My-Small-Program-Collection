clear;close all;clc;
% 设置图片裁剪范围
row_range = 96:175;
col_range = 101:160;
% 设定下采样的长和宽
row = 16; 
col = 12;

% 读入训练集，返回样本列组成的矩阵A以及全部类别class_name
[A, class_name] = LoadTrainSet(row, col);

% 读入一张测试图片，进行预处理
test_img = imread('test_set/Andre_Agassi/Andre_Agassi_0022.jpg');
subplot(2, 2, 1);
imshow(test_img);       % 展示测试图片
title('测试图片（预处理前）');
test_img = im2double(test_img); % 灰度图化
test_img = im2gray(test_img(row_range, col_range)); % 裁剪出面部     
test_img = imresize(test_img,[row, col],'bilinear');  % 二线性差值下采样
subplot(2, 2, 2);
imshow(test_img);       % 展示测试图片
title('测试图片（预处理后）')
test_img = reshape(test_img, [row * col, 1]);    % 列向量化
test_img = test_img / norm(test_img);   %向量单位化

% 解方程Ax=y，使得x的L1范数最小
x = BP_linprog(test_img, A);
subplot(2, 2, 3);
bar(x);
title('稀疏表达系数');

% 计算各个类的残差
r = zeros(50,1);
for i = 1:50
    delta_x = zeros(1000, 1);
    delta_x((i-1)*20+1 : i*20) = x((i-1)*20+1 : i*20);
    r(i) = norm(test_img - A * delta_x, 2);
end
subplot(2, 2, 4);
bar(r, 0.8);
title('类别残差');

% 打印结果
for i = 1:50
    if r(i) == min(min(r))
        res = class_name(i);
        disp(res);
        break
    end
end

% 对全部测试集图片进行分类精度测试
% TestAll(A);