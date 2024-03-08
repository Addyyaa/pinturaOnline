import cv2
from cv2 import dnn
# 加载ESPCN模型
sr = cv2.dnn.
sr.readModel('path_to_ESPCN_model.pb')
sr.setModel('espcn', 4)  # 这里的参数4表示将图像放大4倍

# 读取低分辨率图像
low_res_image = cv2.imread('low_res_image.jpg')

# 对低分辨率图像进行超分辨率重建
high_res_image = sr.upsample(low_res_image)

# 显示原始低分辨率图像和超分辨率重建后的高分辨率图像
cv2.imshow('Low Resolution Image', low_res_image)
cv2.imshow('High Resolution Image', high_res_image)
cv2.waitKey(0)
cv2.destroyAllWindows()