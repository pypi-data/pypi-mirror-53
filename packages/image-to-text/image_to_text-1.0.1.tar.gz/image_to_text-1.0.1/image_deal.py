# -*- coding: utf-8 -*-
"""
图片处理：通过直方图正规化增强对比度（传入图片路径）
python图像处理技术：降噪、滤波、增强对比度
***滤波还未使用
@author: x-h
"""

from skimage import io, data, morphology, segmentation
import cv2
import numpy as np

class deal_image(object):
    #膨胀、腐蚀
    def dil2ero(self,img,selem):
        img=morphology.dilation(img,selem) # 膨胀
        imgres=morphology.erosion(img,selem) # 腐蚀
        return imgres
    
    def deal_part1(self,image_path):
        # 通过直方图正规化增强对比度，读取图片时使用cv2.IMREAD_GRAYSCALE，直接灰度化图片
        in_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 求输入图片像素最大值和最小值
        Imax = np.max(in_image)
        Imin = np.min(in_image)
        # 要输出的最小灰度级和最大灰度级
        Omin, Omax = 0, 255
        # 计算a 和 b的值
        a = float(Omax - Omin)/(Imax - Imin)
        b = Omin - a* Imin
        # 矩阵的线性变化
        out_image = a*in_image + b
        # 数据类型的转化
        out_image = out_image.astype(np.uint8)
        # 显示原图和直方图正规化的效果
        #cv2.imshow('IN', in_image)
        #cv2.waitKey(0)
        #cv2.imshow('OUT', out_image)
        #cv2.waitKey(0)
        
        #识别图片框线？？？
        #原图片减掉框线？？？
        rows,cols=out_image.shape
        rows,cols=out_image.shape
        scale=10   #这个值越大,检测到的直线越多,图片中字体越大，值应设置越小。需要灵活调整该参数。
        col_selem=morphology.rectangle(cols//scale,1)
        #识别表格竖线
        img_cols=self.dil2ero(out_image,col_selem)

        row_selem=morphology.rectangle(1,rows//scale)
        #识别表格横线
        img_rows=self.dil2ero(out_image,row_selem)
      
        #求出整个表格,bitwise_and:同白为白，其余全为黑
        img_line=cv2.bitwise_and(img_cols,img_rows)
        #cv2.imshow('img_line', img_line)
        #cv2.waitKey(0)
        #框线与背景颜色互换
        #cv2.imshow('~img_line', ~img_line)
        #cv2.waitKey(0)

        #求出整个表格且框线与背景颜色互换，并且除去交叉点
        #img_xor=cv2.bitwise_xor(img_cols,img_rows)
        #cv2.imshow('img_xor', img_xor)
        #cv2.waitKey(0)
        
        #求出整个表格交叉点
        #img_or=cv2.bitwise_or(img_cols,img_rows)
        #cv2.imshow('img_or', img_or)
        #cv2.waitKey(0)
        #交叉点与背景颜色互换
        #cv2.imshow('~img_or', ~img_or)
        #cv2.waitKey(0)
        
        #原图片去掉框线
        merge = out_image+(~img_line)
        #cv2.imshow('merge', merge)
        #cv2.waitKey(0)
        return merge
        #cv2.destroyAllWindows()
        
    
if __name__ == '__main__':
    deal_image().deal_part1('C:/Users/Administrator/Desktop/7.jpg')