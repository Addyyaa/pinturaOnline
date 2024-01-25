import os
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

# 例子：将当前目录下所有 JPG 文件压缩到分辨率 (1080, 1920) 并保存到 output 文件夹
input_folder = "."
output_folder = "output"
target_resolution = (1080, 1920)

batch_compress_images(input_folder, output_folder, target_resolution)
