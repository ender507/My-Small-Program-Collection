clc;clear;close all;
%% 图片预处理
img = im2double(imread("1.jpg"));   % 读入图片，从0~255的整形映射到0~1的浮点型
[hei1, wid1, dep1] = size(img);     % 获取图片大小（高度、宽度、深度）
% 打印原图片
imshow(img);
figure;
% 假定要求输出的图片的宽度变为原来的3/4
wid2 = round(wid1/2);
wid_now = wid1;
% 使用插值方法实现图片缩小
tmp_pic = img(:,1:2:wid1,:);
subplot(1,2,1)
imshow(tmp_pic);
%% Seam Carving 方法处理图片
while wid_now ~= wid2
    % 计算能量图
    [gx1, gy1] = gradient(img(:,:,1));
    [gx2, gy2] = gradient(img(:,:,2));
    [gx3, gy3] = gradient(img(:,:,3));
    E = abs(gx1) + abs(gy1)...
        + abs(gx2) + abs(gy2)...
        + abs(gx3) + abs(gy3);
    EC = zeros(hei1, wid_now);        % 累计能量
    PM = zeros(hei1,wid_now);         % 记录每一条路径
    EC(1,:) = E(1,:);
    for i = 2:hei1      % 依次遍历每一行
        % 依次遍历每一行的每一个元素
        % 单独讨论第一个元素
        tmp1 = EC(i-1, 1);
        tmp2 = EC(i-1, 2);
        if tmp1 < tmp2
            EC(i, 1) = tmp1 + E(i, 1);
            PM(i, 1) = 1;
        else
            EC(i, 1) = tmp2 + E(i, 1);
            PM(i, 1) = 2;
        end
        % 讨论中间的元素
        for j = 2: wid_now-1
            tmp1 = EC(i-1, j-1);
            tmp2 = EC(i-1, j);
            tmp3 = EC(i-1, j+1);
            if tmp1 < tmp2 && tmp1 < tmp3
                EC(i, j) = tmp1 + E(i, j);
                PM(i, j) = j-1;
            elseif tmp2 < tmp1 && tmp2 < tmp3
                EC(i, j) = tmp2 + E(i, j);
                PM(i, j) = j;
            else
                EC(i, j) = tmp3 + E(i, j);
                PM(i, j) = j+1;
            end
        end
        % 讨论最后一个元素
        tmp1 = EC(i-1, wid_now-1);
        tmp2 = EC(i-1, wid_now);
        if tmp1 < tmp2
            EC(i, wid_now) = tmp1 + E(i, wid_now);
            PM(i, wid_now) = wid_now-1;
        else
            EC(i, wid_now) = tmp2 + E(i, wid_now);
            PM(i, wid_now) = wid_now;
        end
    end
    % 依据累计能量函数，删去能量最少的缝
    energy_min = min(EC(hei1, :));
    min_pos = find(EC(hei1, :)==energy_min);
    tmp_pic = zeros(hei1, wid_now-1, dep1);
    for i = hei1:-1:2
        tmp = img(i,:,:);
        tmp_pic(i,:,:) = tmp(:,[1:min_pos-1,min_pos+1:wid_now],:);
        min_pos = PM(i, min_pos);
    end
    tmp = img(1,:,:);
    tmp_pic(1,:,:) = tmp(:,[1:min_pos-1,min_pos+1:wid_now],:);
    img = tmp_pic;
    wid_now = wid_now - 1;
end
% 打印最后结果
subplot(1,2,2);
imshow(img);


