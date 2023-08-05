# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 16:53:45 2019

@author: hx
图片识别，生成文本文件，返回识别生成文件的文件路径
"""
import pytesseract
import read_childImage
import time

class OCR_image_to_text(object):
    
    #根据路径执行文字识别
    def image_to_text(self,ocr_path,image_path):
        #识别图片成文本，改成分割形式保存,调用image_to_excel.py中方法
        #text = pytesseract.image_to_string(PIL.Image.open(self.path.get()))
        #调用时使用文件名.类名()。方法名(参数)
        text = read_childImage.Image_To_text().image_to_text(ocr_path,image_path)
        print(text)
        #text = text.encode("utf-8")
        #获取当前时间戳整数部分，用来拼装生成文件的文件名使用，防止文件重名
        current_time=str(int(time.time()))
        #在指定路径打开指定名字文件（若在该路径下不存在改文件，则会新建文件）
        #mode模式如下：
        #w 只能操作写入  r 只能读取   a 向文件追加
        #w+ 可读可写   r+可读可写    a+可读可追加
        #wb+写入进制数据
        #w模式打开文件，如果而文件中有数据，再次写入内容，会把原来的覆盖掉
        text_path='E:/testText/image_to_text'+current_time+'.txt'
        
        #打开文件，在编写文件时设置编码格式，否则出现字符时会报错
        file_handle=open(text_path,mode='w',encoding= 'utf8')
        #将识别后的文本text写入指定文件
        file_handle.write(text)
        #写完之后关闭文件
        file_handle.close()
        #创建列表result，用来存储生成文本文件的路径，文本文件内容
        result=[text_path]
        result.append(text)
        return result