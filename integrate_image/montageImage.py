import os
import math
from PIL import Image
import re


def merge_images(image_folder, store_folder, spot_alias, n, m):
    # 获取所有图像文件的列表
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')]

    # 计算每个小图像的大小和大图像的大小
    image_count = len(image_files)
    if image_count == 0:
        print('No image files found in the directory:', image_folder)
        return

    # 计算小图像的大小以及大图像的大小
    img = Image.open(image_files[0])
    img_size0 = img.size[0]
    img_size1 = img.size[1]
    new_img_size0 = img_size0 * n
    new_img_size1 = img_size1 * m

    # 创建一个新的大图像
    new_img = Image.new('RGB', (new_img_size0, new_img_size1), 'black')

    # 将所有小图像粘贴到新图像的正确位置
    for i, f in enumerate(image_files):
        # "\d+ 用于寻找字符串中连续完整的数字组成的列表"
        # 在satbeams中该波片为所在列
        column = re.findall("\d+", f)[-2]
        # 在satbeams中该波片为所在行
        row = re.findall("\d+", f)[-1]
        img = Image.open(f)
        img = img.resize((img_size0, img_size1))
        # 放大相应倍数之后再铺在背景图中
        new_img.paste(img, (int(column) * 256, int(row) * 256))

    # 保存大图像
    if not os.path.exists(store_folder):
        os.makedirs(store_folder)
    new_img.save(store_folder + spot_alias + '.png')

if __name__ == '__main__':

    position_folder = '../get_json_data/image_completed'
    output_file = './output.png'
    n = 17  # 每行显示的图像数
    m = 17  # 每列显示的图像数
    # 获取位置信息
    positions = os.listdir(position_folder)
    positions = sorted(list(map(int, positions)))
    for position in positions:
        position = str(position)
        # 获取卫星名称
        for satellite in os.listdir(position_folder + "/" + position):
            # 获取波片别名
            for spot_alias in os.listdir(position_folder + "/" + position + '/' + satellite):
                # 获取图片
                image_folder = position_folder + "/" + position + "/" + satellite + '/' + spot_alias
                # 构建文件夹（./image/位置/卫星名称）
                store_folder = './integral_image/' + str(position) + '/' + satellite + '/'
                merge_images(image_folder, store_folder, spot_alias, n, m)



