import PythonMagick
img = PythonMagick.Image("C:\\Users\\redhat\\Desktop\\timg.jpg")
img.sample('256x256')
img.write('C:\\Users\\redhat\\Desktop/wechat.ico')