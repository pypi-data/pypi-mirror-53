# -*- coding: utf-8 -*-
"""
Created on Mon May 13 16:33:15 2019

@author: hx
总体功能：
选择某一路径下图片进行识别（对于汉字的识别效果不是很好，可以自行训练文字库，增加识别概率）
识别后生成文本放在某一路径下(E:/testText/image_to_text)
将文本内容显示到页面对应的位置

"""

from PIL import ImageTk
from tkinter import filedialog as fd
#from tkinter import *
import PIL
import tkinter as tk
import OCR_image_to_text

class select_image_GUI(object):

    #初始化方法，只要调用select_image_GUI(ocr_path)即执行,ocr_path为ocr识别程序exe所在路径
    def __init__(self,ocr_path):
        self.root = tk.Tk()
        
        # 设置整个顶层GUI页面长宽可拉伸
        self.root.resizable(width=True,height=True)   
        #存放图片路径变量
        self.path = tk.StringVar()
        #存放生成txt文件路径
        self.text_path = tk.StringVar()
        self.ocr_path='E:/Tesseract-OCR/tesseract.exe'
        #grid布局管理器，与pack功能类似：https://www.cnblogs.com/ruo-li-suo-yi/p/7425307.html
        tk.Label(self.root,text = "待识别图片路径:").grid(row = 0, column = 0) 
        #输入、输出框存放选择路径
        tk.Entry(self.root, textvariable = self.path, width=113).grid(row = 0, column = 1)
        tk.Button(self.root, text = "待识别图片选择", command = self.selectPath).grid(row = 0, column = 2)
        
        tk.Label(self.root,text = "识别后生成文件路径:").grid(row = 1, column = 0) 
        #输入、输出框存放识别后生成文件路径
        tk.Entry(self.root, textvariable = self.text_path, width=113).grid(row = 1, column = 1)
        #保留后续根据图片识别图片，且将生成的识别文件存于某个路径
        tk.Button(self.root,text="识别图片文字",command=self.image_to_text).grid(row = 1, column = 2) # 按键
        tk.Button(self.root,text="关闭识别插件",command=self.close_code).grid(row = 5, column = 2) # 按键
        
        self.root.mainloop()

    #关闭GUI窗口
    def close_code(self):
        self.root.destroy()           # 关闭窗体
        #os.remove(self.path.get())   # 删除图片，先不进行删除，方便与识别结果对比
        
    #路径选择入口，调用图片展示方法    
    def selectPath(self):
        path_ = fd.askopenfilename()
        self.path.set(path_)
        #选测路径之后进行图片展示
        self.showPhoto(self.path.get())
    
    #重置图片（按要求缩放）
    def resize(self, w_box, h_box, pil_image): #参数是：要适应的窗口宽、高、Image.open后的图片
        w, h = pil_image.size #获取图像的原始大小   
        f1 = 1.0*w_box/w 
        f2 = 1.0*h_box/h    
        factor = min([f1, f2])   
        width = int(w*factor)    
        height = int(h*factor)    
        return pil_image.resize((width, height), PIL.Image.ANTIALIAS) 
    
    #图片展示到固定布局
    #open_path为选择图片的路径
    def showPhoto(self,open_path):
        #期望图像显示的大小  
        w_box = 800  
        h_box = 800 
        # get the size of the image  
       
        #根据选择的路径显示图片
        im=PIL.Image.open(open_path)
        
        # resize the image so it retains its aspect ration  
        # but fits into the specified display box  
        #缩放图像让它保持比例，同时限制在一个矩形框范围内  
        im_resize = self.resize(w_box, h_box, im)
        
        img=ImageTk.PhotoImage(im_resize)
        
        tk.Label(self.root,image=img).grid(row = 2, column = 1) # 布局控件
        self.root.mainloop() #显示图片
        
    #根据路径执行文字识别
    def image_to_text(self):
        #调用时，一个为ocr识别软件位置，一个为选择的图片位置
        result=OCR_image_to_text.OCR_image_to_text().image_to_text(self.ocr_path,self.path.get())
        self.text_path.set(result[0])
        tk.Label(self.root,text = "识别后文本:").grid(row = 4, column = 0) 
        print('hhhhhhhhh'+result[1])
        text=tk.Text(self.root,width=113,height=10)
        text.insert(tk.INSERT,result[1])
        text.grid(row = 4, column = 1)
        


if __name__ == '__main__':
    select_image_GUI('E:/Tesseract-OCR/tesseract.exe')
