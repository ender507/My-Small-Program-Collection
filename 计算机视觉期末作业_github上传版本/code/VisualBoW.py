from PIL import Image
from PIL import ImageFilter
import random
import numpy as np
import matplotlib.pyplot as plt
from segUtil import *
from sklearn import decomposition
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier


def imSave(pic, title, save_path, show=True):
    # 展示1s的图片
    if show:
        plt.get_current_fig_manager().window.state('zoomed')
        plt.imshow(pic)
        #plt.show()
        plt.ion()
        plt.pause(1)
        plt.close()
        
    # 保存
    # pic.save(save_path+str(title)+'.png')


# 计算图片的归一化RGB直方图
def getPictureHistogram(img):
    img_array = np.array(img)
    histogram = np.zeros((8,8,8))
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            histogram[img_array[i][j][0]//32,img_array[i][j][1]//32,img_array[i][j][2]//32] += 1
    histogram /= np.sum(histogram)  # 归一化
    return histogram.reshape(-1)


if __name__ == '__main__':
    gen_new_data = False    # 是否新生成训练数据

    if gen_new_data:
        histograms_total = np.empty((0,1024))
        labels_total = np.empty((0,1))
        pid = [i for i in range(1,1001)]
        pid = random.sample(pid, 200)
        t = 0
        for pic_id in pid:
            print(t)
            t+=1
            img = Image.open("data\\imgs\\"+str(pic_id)+".png")       # 原图
            ground = Image.open("data\\gt\\"+str(pic_id)+".png").convert('1')    # 前景背景图，转化为黑白图
            histogram = getPictureHistogram(img)   # 获取整幅图的归一颜色直方图
            histograms, labels = segment(img, ground)   # 分区并获取各个区域的颜色直方图和标签
            # 将直方图转换为特征向量
            for i in range(histograms.shape[0]):
                tmp = np.hstack((histograms[i].reshape(-1),histogram))
                histograms_total = np.vstack((histograms_total,tmp))
            labels_total = np.vstack((labels_total,labels.reshape(-1,1)))
        np.save('statistics\\histograms_total.npy',histograms_total)
        np.save('statistics\\labels_total.npy',labels_total)
    else:
        histograms_total = np.load('statistics\\histograms_total.npy')
        labels_total = np.load('statistics\\labels_total.npy')
    # PCA降维
    pca = decomposition.PCA(n_components=20)
    histograms_total = pca.fit_transform(histograms_total)
    # histograms_total.shape = (区域样本数, 每个区域的20维特征向量)
    # labels_total = (区域样本数, 每个区域的1维标签)

    
    # 使用K-means将样本分为50类
    kmeans = KMeans(n_clusters=50)
    kmeans.fit(histograms_total)
    cluster_centers = kmeans.cluster_centers_.copy()    # 获取分类中心(50*20)

    # 计算余弦相似度
    cosine_sim = np.dot(histograms_total, cluster_centers.reshape(20,50)) / \
np.dot(np.linalg.norm(histograms_total, axis=1).reshape(-1,1), np.linalg.norm(cluster_centers, axis=1).reshape(1,-1))
    # 将50维余弦相似度加到20维对比度后，形成70维特征
    histograms_total = np.hstack((histograms_total, cosine_sim))    
    # 用这些样本与标签建立KNN模型
    knn = KNeighborsClassifier()
    knn.fit(histograms_total, labels_total.reshape(-1))
    # 读入测试样本，即第二问的结果
    test_samples = np.empty((0,1024))
    test_labels = np.empty((0,1))
    num = 0
    for i in range(57,1000, 100):
        seg_group = np.load('statistics\\SEG_GROUP_'+str(i)+'.npy',allow_pickle=True).item()
        img_array = np.array(Image.open("data\\imgs\\"+str(i)+".png"))
        ground_array = np.array(Image.open("output\\ImageSegmentation\\"+str(i)+"_2.png").convert('1'))
        # 计算整幅图的RGB直方图
        histogram = getPictureHistogram(img_array)
        histograms = np.zeros((len(seg_group.keys()),8,8,8))
        # 遍历每个区域并且计算归一化RGB直方图
        for seg in seg_group.keys():
            for pixel in seg_group[seg]:
                histograms[num,img_array[pixel[0],pixel[1],0]//32,
                    img_array[pixel[0],pixel[1],1]//32,img_array[pixel[0],pixel[1],2]//32] += 1
            histograms[num] /= np.sum(histograms[num])  # 直方图归一化
            # 添加当前区域的标签（真实值）
            test_labels = np.vstack((test_labels,np.array([ground_array[seg[0],seg[1]]]).reshape(1,1)))
        num += 1
        # 添加当前图片所有区域的50维对比度特征值
        for i in range(histograms.shape[0]):
            tmp = np.hstack((histograms[i].reshape(-1),histogram))
            test_samples = np.vstack((test_samples,tmp))
    # 用训练好的pca模型降维
    test_samples = pca.transform(test_samples)
    # 计算余弦相似度
    cosine_sim = np.dot(test_samples, cluster_centers.reshape(20,50)) / \
np.dot(np.linalg.norm(test_samples, axis=1).reshape(-1,1), np.linalg.norm(cluster_centers, axis=1).reshape(1,-1))
    # 将50维余弦相似度加到20维对比度后，形成70维特征
    test_samples = np.hstack((test_samples, cosine_sim))
    # 用训练好的knn模型预测结果
    predict_labels = knn.predict(test_samples)

    # 统计结果
    total = predict_labels.shape[0]
    right = np.sum(test_labels.reshape(-1) == predict_labels)
    print('总计有'+str(total)+'个区域，其中前景背景预测正确的有'+str(right)+'个')
    print('准确率为：',right/total)
    
        
