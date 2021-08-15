just4fun文件夹里实现的是普通的SeamCarving，可以快速处理当前图片，做着玩的

data.zip是全部的图片，便于上传打了包

SeamCarving.py为实现第一题的程序，输出Seam Carving处理后的图片

ImageSegmentation.py为实现第二题的程序，输出图像分区后的图片，IOUcalc.py用于计算分区后的图片的IOU值

VisualBoW.py为实现第三题的程序，最终会打印结果。该程序使用到了segUtil.py模块，用于图像的分区和训练数据的生成。

code\output\SeamCarving文件夹下有一个gifGenerator.py程序，执行后能够生成编号为57和557两张图片的gif

statistics文件夹下储存第二题的分区结果和第三问的分区结果，用于第三问的训练和测试数据的产生

