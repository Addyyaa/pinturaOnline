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

def image_process(is_stretch):
    image_path = input("请输入图片路径：")
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

def compress_image():
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

    target_resolution = image_process(is_stretch)

    if target_resolution is None:
        return

    image_path = input("请输入图片路径：")
    img = Image.open(image_path)

    if not os.path.exists('output'):
        os.makedirs('output')

    output_path = os.path.join('output', 'compressed_image.jpg')
    resized_img = img.resize(target_resolution, Image.LANCZOS)
    resized_img.save(output_path)

    print(f"压缩后的图片已保存到：{output_path}")

compress_image()
