%% 读入图片文件
clear;
img1 = 'a.png';
img1 = imread(img1);
img1 = double(img1);

%% 在RGB空间比较通道关系
R = img1(:,:,1);
G = img1(:,:,2);
B = img1(:,:,3);
figure(1);
scatter(R(:),G(:),1);
hold on;
scatter(R(:),B(:),1);
hold on;
scatter(G(:),B(:),1);
grid on;
axis equal;

%% 将img1从RGB空间映射到l-alpha-beta空间 
[wid1, hei1, dep1] = size(img1);
img2 = img1(:,:,:);
for i = 1:wid1
   for j = 1:hei1 
       % RGB -> LMS
       tmp = [0.3811 0.5783 0.0402;0.1967 0.7244 0.0782;0.0241 0.1228 0.8444] * ...
       [img1(i,j,1);img1(i,j,2);img1(i,j,3)];
       % LMS -> AC1C2
       tmp2 = [2.0 1.0 0.05; 1.0 -1.09 0.09; 0.11 0.11 -0.22] *...
       [tmp(1);tmp(2);tmp(3)];
       img2(i,j,1) = tmp2(1);
       img2(i,j,2) = tmp2(2);
       img2(i,j,3) = tmp2(3);
       % LMS -> l-a-b
       tmp = [sqrt(1/3) 0 0;0 sqrt(1/6) 0;0 0 sqrt(1/2)] * ...
       [1 1 1;1 1 -2;1 -1 0] * ...
       [log10(tmp(1));log10(tmp(2));log10(tmp(3))];
       img1(i,j,1) = tmp(1);
       img1(i,j,2) = tmp(2);
       img1(i,j,3) = tmp(3);
   end
end

%% l-a-b比较关系
l = img1(:,:,1);
a = img1(:,:,2);
b = img1(:,:,3);
figure(2);
scatter(l(:),a(:),1);
hold on;
scatter(l(:),b(:),1);
hold on;
scatter(a(:),b(:),1);
grid on;
axis equal;

%% A-C1-C2比较关系
A = img2(:,:,1);
C1 = img2(:,:,2);
C2 = img2(:,:,3);
figure(3);
scatter(A(:),C1(:),1);
hold on;
scatter(A(:),C2(:),1);
hold on;
scatter(C1(:),C2(:),1);
axis equal;
grid on;