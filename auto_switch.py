import os
from PIL import Image
import logging

def get_image_resolution(image_path):
    try:
        img = Image.open(image_path)
        width, height = img.size
        return width, height
    except Exception as e:
        logging.error(f"Error: {e}")
        return None

def image_process(is_stretch, image_path):
    resolution = get_image_resolution(image_path)
    if resolution is None:
        return None
    width, height = resolution
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        logging.error("长宽参数无效")
        return None
    if is_stretch:  # 拉伸处理
        if width > height:
            width = 1920
            height = 1200
        elif width <= height:
            width = 1200
            height = 1920
    else:  # 不做拉伸，但限制最大值
        if width > height and width > 1920:
            width = 1920
            if height > 1200:
                height = 1200
        elif width <= height and height > 1920:
            height = 1920
            if width > 1200:
                width = 1200
    return width, height

def compress_image(image_path, target_resolution):
    img = Image.open(image_path)

    if not os.path.exists('output'):
        os.makedirs('output')

    # 使用原始文件名并添加 _compressed 标识
    filename, file_extension = os.path.splitext(os.path.basename(image_path))
    output_filename = f"{filename}_compressed{file_extension}"

    output_path = os.path.join('output', output_filename)
    resized_img = img.resize(target_resolution, Image.LANCZOS)
    resized_img.save(output_path)

    print(f"压缩后的图片已保存到：{output_path}")

def process_all_images(is_stretch):
    current_directory = os.getcwd()
    jpg_files = [file for file in os.listdir(current_directory) if file.lower().endswith(".jpg")]

    for jpg_file in jpg_files:
        image_path = os.path.join(current_directory, jpg_file)
        target_resolution = image_process(is_stretch, image_path)

        if target_resolution is not None:
            compress_image(image_path, target_resolution)

if __name__ == "__main__":
    while True:
        is_stretch = input("是否拉伸处理(y/n):")
        if is_stretch.lower() == 'y':
            is_stretch = True
            break
        elif is_stretch.lower() == 'n':
            is_stretch = False
            break
        else:
            print("输入无效，请重新输入")
            continue

    process_all_images(is_stretch)
