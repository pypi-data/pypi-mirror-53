# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:23:19 2019
将图片按照表格框线交叉点分割成子图片（传入图片路径）
@author: x-h
"""

import cv2
import numpy as np
import pytesseract
import image_deal
class Image_To_text(object):
    #锐化图片
    def custom_blur_demo(self,image):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
        dst = cv2.filter2D(image, -1, kernel=kernel)
        return dst
    #二值化后的图片降噪
    def depoint(self,img):
        """传入二值化后的图片数组进行降噪"""
        pixdata = img
        w,h = img.shape
        for y in range(1,h-1):
            for x in range(1,w-1):
                count = 0
                if pixdata[x,y-1] > 245:#上
                    count = count + 1
                if pixdata[x,y+1] > 245:#下
                    count = count + 1
                if pixdata[x-1,y] > 245:#左
                    count = count + 1
                if pixdata[x+1,y] > 245:#右
                    count = count + 1
                if pixdata[x-1,y-1] > 245:#左上
                    count = count + 1
                if pixdata[x-1,y+1] > 245:#左下
                    count = count + 1
                if pixdata[x+1,y-1] > 245:#右上
                    count = count + 1
                if pixdata[x+1,y+1] > 245:#右下
                    count = count + 1
                if count > 4:
                    pixdata[x,y] = 255
        return img

    def image_to_text(self,ocr_path,image_path):
        image = cv2.imread(image_path, 1)
        print(image)
        #灰度图片
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #二值化
        binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
        #ret,binary = cv2.threshold(~gray, 127, 255, cv2.THRESH_BINARY)
        
        #cv2.imshow("二值化图片：", binary) #展示图片
        #cv2.waitKey(0)

        rows,cols=binary.shape
        scale = 40
        #识别横线
        kernel  = cv2.getStructuringElement(cv2.MORPH_RECT,(cols//scale,1))
        eroded = cv2.erode(binary,kernel,iterations = 1)
        #cv2.imshow("Eroded Image",eroded)
        dilatedcol = cv2.dilate(eroded,kernel,iterations = 1)
        #cv2.imshow("表格横线展示：",dilatedcol)
        #cv2.waitKey(0)

        #识别竖线
        scale = 20
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,rows//scale))
        eroded = cv2.erode(binary,kernel,iterations = 1)
        dilatedrow = cv2.dilate(eroded,kernel,iterations = 1)
        #cv2.imshow("表格竖线展示：",dilatedrow)
        #cv2.waitKey(0)

        #标识交点
        bitwiseAnd = cv2.bitwise_and(dilatedcol,dilatedrow)
        #cv2.imshow("表格交点展示：",bitwiseAnd)
        #cv2.waitKey(0)
        # cv2.imwrite("my.png",bitwiseAnd) #将二值像素点生成图片保存

        #标识表格
        #merge = cv2.add(dilatedcol,dilatedrow)
        #cv2.imshow("表格整体展示：",merge)
        #cv2.waitKey(0)


        #两张图片进行减法运算，去掉表格框线
        #merge2 = cv2.subtract(binary,merge)
        #cv2.imshow("图片去掉表格框线展示：",merge2)
        #cv2.waitKey(0)

        #识别黑白图中的白色交叉点，将横纵坐标取出
        ys,xs = np.where(bitwiseAnd>0)

        mylisty=[] #纵坐标
        mylistx=[] #横坐标

        #通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值值相近，我只取相近值的最后一点
        #这个10的跳变不是固定的，根据不同的图片会有微调，基本上为单元格表格的高度（y坐标跳变）和长度（x坐标跳变）
        i = 0
        myxs=np.sort(xs)
        for i in range(len(myxs)-1):
            if(myxs[i+1]-myxs[i]>10):
                mylistx.append(myxs[i])
            i=i+1
        mylistx.append(myxs[i]) #要将最后一个点加入
        
        
        i = 0
        myys=np.sort(ys)
        #print(np.sort(ys))
        for i in range(len(myys)-1):
            if(myys[i+1]-myys[i]>10):
                mylisty.append(myys[i])
            i=i+1
        mylisty.append(myys[i]) #要将最后一个点加入
        
        print('mylisty',mylisty)
        print('mylistx',mylistx)
        
        

        text_String_total=''
        #调用图片去框线方法,并且已经灰度化
        image2=image_deal.deal_image().deal_part1(image_path)
        #循环y坐标，x坐标分割表格
        for i in range(len(mylisty)-1):
            for j in range(len(mylistx)-1):
                #在分割时，第一个参数为y坐标，第二个参数为x坐标
                ROI = image2[mylisty[i]:mylisty[i+1]-3,mylistx[j]:mylistx[j+1]-3] #减去3的原因是由于我缩小ROI范围
               
                
                ROI_INFO = ROI.shape #获取图像的原始大小  
                #缩放倍数
                factor = 4  
                width = int(ROI_INFO[1]*factor)    
                height = int(ROI_INFO[0]*factor)    
                ROI_RESIZE = cv2.resize(ROI,(width, height))
               
                #imageVar = cv2.Laplacian(ROI_RESIZE, cv2.CV_64F)
                #print(cv2.CV_64F) #6
                #cv2.imshow("2：",imageVar)
                #cv2.waitKey(0)
                #对放大后的图片进行灰度图片
                #gray_ROI_RESIZE = cv2.cvtColor(ROI_RESIZE, cv2.COLOR_BGR2GRAY)
                #锐化图片
                dst=self.custom_blur_demo(ROI_RESIZE)
                #第二次锐化（锐化次数再多会变得更不清晰）
                dst=self.custom_blur_demo(dst)

 
               
                #对放大后的图片进行二值化
                binary_ROI_RESIZE = cv2.adaptiveThreshold(~dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)

                
                #降噪
                binary_ROI_RESIZE=self.depoint(binary_ROI_RESIZE)

                #special_char_list = '`~!@#$%^&*()-_=+[]{}|\\;:‘’，。《》/？ˇ'
                pytesseract.pytesseract.tesseract_cmd = ocr_path
                text1 = pytesseract.image_to_string(binary_ROI_RESIZE,lang='chi_sim')  #读取文字，此为默认英文
                #替换换行
                text1=text1.replace('\n','')
                #替换空格
                text1=text1.replace(' ','')
                #替换o为0
                text1=text1.replace('o','0')
                #替换I为1
                text1=text1.replace('I','1')
               
                
                #text2 = ''.join([char for char in text2 if char not in special_char_list])
                print('识别分割子图片信息为：'+text1)
                text_String_total=text_String_total+text1+'|'
            
                j=j+1
            text_String_total=text_String_total+'\n'
            i=i+1

        print(text_String_total)
        #返回识别后的文本字符串
        return text_String_total

if __name__ == '__main__':
    Image_To_text().image_to_text('E:/Tesseract-OCR/tesseract.exe','C:/Users/Administrator/Desktop/7.jpg')