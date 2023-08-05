from distutils.core import setup
#前三个为必要元素，后面的随意，可填可不填
setup(
      name='image_to_text', #项目名称，取值随意
      version='1.0.1', #版本号
      py_modules=['opencv_deal_image','image_deal','OCR_image_to_text','read_childImage','select_image_GUI'], #对应模块文件的名称
      author='HanXiao',
      author_email='911432860@qq.com',
      url='https://blog.csdn.net/HXiao0805',
      description='这是一个简单的excel图标样式图片转换为文字的模块'
      )