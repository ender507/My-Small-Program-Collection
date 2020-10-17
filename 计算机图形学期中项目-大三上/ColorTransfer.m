%% 读入图片文件
img1 = 'a.jpg';
img2 = 'b.png';
img1 = imread(img1);
img2 = imread(img2);
% 将像素值改为浮点数
img1 = im2double(img1);
img2 = im2double(img2);
% 显示两张原图
figure(1);
imshow(img1);
figure(2);
imshow(img2);

%% 将img1从RGB空间映射到l-alpha-beta空间 
[wid1, hei1, dep1] = size(img1);
for i = 1:wid1
   for j = 1:hei1 
       % RGB -> LMS
       tmp = [0.3811 0.5783 0.0402;0.1967 0.7244 0.0782;0.0241 0.1228 0.8444] * ...
       [img1(i,j,1);img1(i,j,2);img1(i,j,3)];
       % LMS -> lab
       tmp = [sqrt(1/3) 0 0;0 sqrt(1/6) 0;0 0 sqrt(1/2)] * ...
       [1 1 1;1 1 -2;1 -1 0] * ...
       [log10(tmp(1));log10(tmp(2));log10(tmp(3))];
       img1(i,j,1) = tmp(1);
       img1(i,j,2) = tmp(2);
       img1(i,j,3) = tmp(3);
   end
end

%% 将img2从RGB空间映射到l-alpha-beta空间
[wid2, hei2, dep2] = size(img2);
for i = 1:wid2
   for j = 1:hei2 
       % RGB -> LMS
       tmp = [0.3811 0.5783 0.0402;0.1967 0.7244 0.0782;0.0241 0.1228 0.8444] * ...
       [img2(i,j,1);img2(i,j,2);img2(i,j,3)];
       % LMS -> lab
       tmp = [sqrt(1/3) 0 0;0 sqrt(1/6) 0;0 0 sqrt(1/2)] * ...
       [1 1 1;1 1 -2;1 -1 0] * ...
       [log10(tmp(1));log10(tmp(2));log10(tmp(3))];
       img2(i,j,1) = tmp(1);
       img2(i,j,2) = tmp(2);
       img2(i,j,3) = tmp(3);
   end
end

%% 计算均值和标准差
mean_l1 = mean2(img1(:,:,1));
mean_alpha1 = mean2(img1(:,:,2));
mean_beta1 = mean2(img1(:,:,3));
mean_l2 = mean2(img2(:,:,1));
mean_alpha2 = mean2(img2(:,:,2));
mean_beta2 = mean2(img2(:,:,3));
var_l1 = std2(img1(:,:,1));
var_alpha1 = std2(img1(:,:,2));
var_beta1 = std2(img1(:,:,3));
var_l2 = std2(img2(:,:,1));
var_alpha2 = std2(img2(:,:,2));
var_beta2 = std2(img2(:,:,3));

%% 进行图像变换
% 目标图像均值改为0
img1(:,:,1) = img1(:,:,1) - mean_l1;
img1(:,:,2) = img1(:,:,2) - mean_alpha1;
img1(:,:,3) = img1(:,:,3) - mean_beta1;
% 目标图像方差改为源图像方差
img1(:,:,1) = img1(:,:,1) * var_l2/var_l1;
img1(:,:,2) = img1(:,:,2) * var_alpha2/var_alpha1;
img1(:,:,3) = img1(:,:,3) * var_beta2/var_beta1;
% 目标图像均值改为源图像均值
img1(:,:,1) = img1(:,:,1) + mean_l2;
img3 = img1(:,:,:);
img3(:,:,2) = img3(:,:,2) + mean_alpha2;
img3(:,:,3) = img3(:,:,3) + mean_beta2;


%% 将img1从l-alpha-beta空间还原到RGB空间
for i = 1:wid1
   for j = 1:hei1 
       % lab -> LMS
       tmp1 = [1 1 1;1 1 -1;1 -2 0] * ...
       [sqrt(1/3) 0 0;0 sqrt(1/6) 0;0 0 sqrt(1/2)] * ...
       [img1(i,j,1);img1(i,j,2);img1(i,j,3)];
       tmp2 = [1 1 1;1 1 -1;1 -2 0] * ...
       [sqrt(1/3) 0 0;0 sqrt(1/6) 0;0 0 sqrt(1/2)] * ...
       [img3(i,j,1);img3(i,j,2);img3(i,j,3)];
       % LMS -> RGB
       tmp1 = [4.4679 -3.5873 0.1193;-1.2186 2.3809 -0.1624;0.0497 -0.2439 1.2045] * ...
           [10^tmp1(1);10^tmp1(2);10^tmp1(3)];
       img1(i,j,1) = tmp1(1);
       img1(i,j,2) = tmp1(2);
       img1(i,j,3) = tmp1(3);
       tmp2 = [4.4679 -3.5873 0.1193;-1.2186 2.3809 -0.1624;0.0497 -0.2439 1.2045] * ...
           [10^tmp2(1);10^tmp2(2);10^tmp2(3)];
       img3(i,j,1) = tmp2(1);
       img3(i,j,2) = tmp2(2);
       img3(i,j,3) = tmp2(3);
   end
end
%% 打印结果
% alpha-beta均值和img2一致的图片
figure(3);
imshow(img3);
% alpha-beta均值为0的图片
figure(4);
imshow(img1);

