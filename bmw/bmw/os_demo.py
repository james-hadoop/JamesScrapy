import os

images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
if not os.path.exists(images_path):
    print('images文件夹不存在')
    os.mkdir(images_path)
else:
    print('images文件夹存在')
