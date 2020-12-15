各个文件的说明：
FaceRecognition.m 人脸识别算法的主体部分，程序开始运行的部分
LoadTrainSet.m 读入训练集、预处理、得到A矩阵
BP_linprog.m 解方程Ax=y使得x的l1范数最小
TestAll.m 读入全部测试集并进行测试和结果统计
train_set 包含训练集全部的图片
test_set 包含测试集全部的图片

为了上传github，对图片文件夹进行了打包