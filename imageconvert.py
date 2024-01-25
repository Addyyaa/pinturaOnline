import os
import sys

from PIL import Image

def compress_image(input_path, output_path, target_resolution):
    img = Image.open(input_path)
    resized_img = img.resize(target_resolution, Image.LANCZOS)
    resized_img.save(output_path)

def batch_compress_images(input_folder, output_folder, target_resolution):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中所有的 JPG 文件
    jpg_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".jpg")]

    for jpg_file in jpg_files:
        input_path = os.path.join(input_folder, jpg_file)
        output_path = os.path.join(output_folder, jpg_file)
        compress_image(input_path, output_path, target_resolution)
    print("压缩完成，请到out文件夹下查看图片")
    current_path = os.path.dirname(os.path.abspath(__file__))
    outputpath = current_path + "/output"
    os.startfile(outputpath)

# 例子：将当前目录下所有 JPG 文件压缩到分辨率 (1080, 1920) 并保存到 output 文件夹
input_folder = "."
output_folder = "output"
while True:
    try:
        width = input("请输入转换后的宽分辨率：")
        width = int(width)
        # 限制分辨率大小1 到 8000
        if width < 1 or width > 8000:
            raise ValueError
        height = input("请输入转换后的高分辨率：")
        height = int(height)
        if height < 1 or height > 8000:
            raise ValueError
    except ValueError:
        print("输入无效，请重新输入")
        continue
    if isinstance(width, int) and isinstance(height, int):
        target_resolution = (width, height)
        break
batch_compress_images(input_folder, output_folder, target_resolution)
