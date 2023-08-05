# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 18:57:40 2019

@author: x-h

opencv图片处理
"""
import cv2
from matplotlib import pyplot as plt
import numpy as np
class opencv_deal_image(object):
    """
    读图片成为灰度图，结果为像素点组成的矩阵
    入参：图片对应路径
    """
    def open_image(self,path):
        #读图片，结果为像素点组成的矩阵，0为灰度图
        #参数1：图片的文件名
        #如果图片放在当前文件夹下，直接写文件名就行了，如’lena.jpg’
        #否则需要给出绝对路径，如’D:\OpenCVSamples\lena.jpg’
        #参数2：读入方式，省略即采用默认值
        #cv2.IMREAD_COLOR：彩色图，默认值(1)
        #cv2.IMREAD_GRAYSCALE：灰度图(0)
        #cv2.IMREAD_UNCHANGED：包含透明通道的彩色图(-1)
        img=cv2.imread(path,0)
        return img
    
    """
    展示图片
    入参：图片像素点矩阵
    """
    def show_image(self,img):
        #展示图片
        cv2.imshow('title', img)
        #等待外界关闭窗口
        cv2.waitKey(0)
        
    """
    在对应路径下生成图片
    入参：1、图片像素点矩阵；2、图片路径
    """
    def save_image(self,img,path):
        #将图片保存在path路径下
        cv2.imwrite(path,img)
        
    """
    获取图片属性
    """
    def get_image_param(self,img):
        #获取图片属性:
        #img.shape获取图像的形状，图片是彩色的话，返回一个包含行数（高度）、列数（宽度）和通道数的元组
        #灰度图只返回行数和列数
        img.shape
        #获取图像总的像素数
        img.size
        
        
    """
    截取部分图片
    入参：1、y_start:纵坐标起始，行开始
         2、y_end:纵坐标结束，行结束
         3、x_start:横坐标起始，列开始
         4、x_end:横坐标起始，列结束
         5、图片像素点矩阵
    """
    
    def get_ROI(self,y_start,y_end,x_start,x_end,img):
        child_img=img[y_start:y_end,x_start:x_end]
        return child_img
    
    #阈值分割，阈值分割并不是二值化，阈值分割结果是两类值，而不是两个值
    #固定阈值分割
    #自适应阈值分割
    def do_threshold(self,img):
        #◦参数1：要处理的原图(一般为灰度图)
        #◦参数2：最大阈值，一般为255
        #◦参数3：小区域阈值的计算方式◦ADAPTIVE_THRESH_MEAN_C：小区域内取均值
        #                         ◦ADAPTIVE_THRESH_GAUSSIAN_C：小区域内加权求和，权重是个高斯核
        #◦参数4：阈值方式（跟前面讲的那5种相同）cv2.THRESH_BINARY（常用）、
        #                                   cv2.THRESH_BINARY_INV、
        #                                   cv2.THRESH_TRUNC、
        #                                   cv2.THRESH_TOZERO、
        #                                   cv2.THRESH_TOZERO_INV
        #◦参数5：小区域的面积，如11就是11*11的小块
        #◦参数6：最终阈值等于小区域计算出的阈值再减去此值
        #image_mean=cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 35, 4)
        #cv2.imshow("image_mean", image_mean) #展示图片
        #cv2.waitKey(0)
        #blur = cv2.GaussianBlur(img, (5, 5), 0)
        image_gaussian=cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 4)
        cv2.imshow("image_gaussian", image_gaussian) #展示图片
        cv2.waitKey(0)
        cv2.imshow("image_gaussian", ~image_gaussian) #展示图片
        cv2.waitKey(0)
        
        # 先进行高斯滤波，再使用Otsu阈值法
        #blur = cv2.GaussianBlur(img, (5, 5), 0)
        ret3, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow("image_otsu", otsu) #展示图片
        cv2.waitKey(0)
        
        return image_gaussian
    
    
    def plot_image(self,img):
        # 绘制阈值图
        plt.subplot(2, 2, 1)
        plt.imshow(img, 'gray')
        plt.title('gray', fontsize=8)
        plt.xticks([]), plt.yticks([])

        # 绘制直方图plt.hist，ravel函数将数组降成一维
        plt.subplot(2, 2, 2)
        plt.hist(img.ravel(), 256)
        plt.title('Histogram', fontsize=8)
        plt.xticks([]), plt.yticks([])

    """
    图片缩放
    入参：1、图片像素点矩阵；2、缩放尺寸
    """
    def img_resize(self,img,size):
        # 按照比例缩放，如x,y轴均放大一倍
        res = cv2.resize(img, None, fx=size, fy=size, interpolation=cv2.INTER_LINEAR)
        cv2.imshow("image_resize", res) #展示图片
        cv2.waitKey(0)
        return res
    
    #选转图片
    #参数一：img灰度图片
    #参数二：du选转度数（正：逆时针，负：顺时针）
    #参数三：缩放比例
    def xuanZHuan_img(self,img,du,resize):
        #获取行、列
        rows, cols = img.shape
        #定义变换矩阵
        #◦参数1：图片的旋转中心
        #◦参数2：旋转角度(正：逆时针，负：顺时针)
        #◦参数3：缩放比例，0.5表示缩小一半
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), du, resize)
        #进行旋转
        dst = cv2.warpAffine(img, M, (cols, rows))

        cv2.imshow('rotation', dst)
        cv2.waitKey(0)
        
    #仿射变换
    def FANGSHE_transform(self,img):
        #获取灰度图的行、列
        rows, cols = img.shape

        # 变换前的三个点
        pts1 = np.float32([[50, 65], [150, 65], [210, 210]])
        # 变换后的三个点
        pts2 = np.float32([[50, 100], [150, 65], [100, 250]])

        # 生成变换矩阵
        M = cv2.getAffineTransform(pts1, pts2)
        dst = cv2.warpAffine(img, M, (cols, rows))
        cv2.imshow('FANGSHE_transform', dst)
        cv2.waitKey(0)
    
    #透视变换    
    def TOUSHI_transform(self,img):
        #获取灰度图的行、列
        rows, cols = img.shape 
        # 原图中卡片的四个角点
        pts1 = np.float32([[148, 80], [437, 114], [94, 247], [423, 288]])
        # 变换后分别在左上、右上、左下、右下四个点
        pts2 = np.float32([[0, 0], [320, 0], [0, 178], [320, 178]])

        # 生成透视变换矩阵
        M = cv2.getPerspectiveTransform(pts1, pts2)
        # 进行透视变换，参数3是目标图像大小
        dst = cv2.warpPerspective(img, M, (cols, rows))
        cv2.imshow('TOUSHI_transform', dst)
        cv2.waitKey(0)
        
        
    #两幅图片直接相加会改变图片的颜色，如果用图像混合，则会改变图片的透明度，所以我们需要用按位操作
    #按位运算，将十进制数值转为二进制，之后进行二进制的按位运算，结果重新转为十进制
    def bitwise(self,flag,src1,src2):
        if flag=='bitwise_and':
            #将两个图片按位与运算（入参为图片的像素矩阵）
            dst=cv2.bitwise_and(src1,src2)
            cv2.imshow('bitwise_and', dst)
            cv2.waitKey(0)
        elif flag=='bitwise_not':
            #将图片按位取非运算（入参为图片的像素矩阵）
            dst=cv2.bitwise_not(src1)
            cv2.imshow('bitwise_not', dst)
            cv2.waitKey(0)
        elif flag=='bitwise_or':
            #将两个图片按位或运算（入参为图片的像素矩阵）
            dst=cv2.bitwise_or(src1,src2)
            cv2.imshow('bitwise_or', dst)
            cv2.waitKey(0)
        else:
            #将两个图片按位异或运算（入参为图片的像素矩阵）
            dst=cv2.bitwise_xor(src1,src2)
            cv2.imshow('bitwise_xor', dst)
            cv2.waitKey(0)
        return dst


if __name__ == '__main__':
    #获取图片
    img=opencv_deal_image().open_image('C:/Users/Administrator/Desktop/7.jpg')
    # 放大图片
    img_resize=opencv_deal_image().img_resize(img)
    #阈值分割
    image_gaussian=opencv_deal_image().do_threshold(img_resize)
    #选转图片
    opencv_deal_image().xuanZHuan_img(image_gaussian,45,0.2)
    
    #仿射变换
    opencv_deal_image().FANGSHE_transform(image_gaussian)
    
    #透视变换
    opencv_deal_image().TOUSHI_transform(image_gaussian)
    #opencv_deal_image().plot_image(image_gaussian)
    
