from PIL import Image

def convert_png_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    resized_img = img.resize((512, 512), Image.LANCZOS)
    resized_img.save(ico_path, format='PNG')

# 调用示例
png_path = 'compress.png'
ico_path = 'image11111111111.ico'
convert_png_to_ico(png_path, ico_path)