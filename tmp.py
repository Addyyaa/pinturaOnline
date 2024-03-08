import requests
import time
import os
import glob
#创建相册
headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Dnt": "1",
    "Host": "139.224.192.36:8082",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "X-Token": "eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50SWQiOjEsImFjY291bnQiOiJzeXNhZG1pbiIsImxvZ2luVHlwZSI6MSwidXNlclR5cGUiOjIsImlhdCI6MTcwNjY3NTY2OCwibmJmIjoxNzA2Njc1NjY4LCJleHAiOjE3MDc1Mzk2Njh9.4OJMF_H-KQX6tEeCXPAV5qkWz1t3fgTnaIFcUSxTL-8"
}
body_data = {
  "cover": "",
  "tags": [
    2077
  ],
  "isFeatured": 2,
  "status": "",
  "summary": "",
  "createBy": "",
  "createTime": "",
  "type": 0,
  "name": ""
}
interface = "http://139.224.192.36:8082/api/v1/manage/materialLibrary"
for i in range(1, 101):
    body_data["name"] = i
    response = requests.post(interface, headers=headers, json=body_data)

# 上传图片
# headers = {
#     "authority": "up-z2.qiniup.com",
#     "method": "POST",
#     "path": "/",
#     "scheme": "https",
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarySKfD1dOlubD6Vnzf",
#     "Dnt": "1",
#     "Origin": "http://139.224.192.36:8888",
#     "Referer": "http://139.224.192.36:8888/",
#     "Sec-Ch-Ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
# }
# body_data = {
#     "token": "bA5ywMRj7I2-6x1fPx2C4KQ4Vsz4cLt1Ce63aZ8o:_xM_Tj_4vcnzNs2fkVDD1mE5cWw"
#              "=:eyJzY29wZSI6ImltYWdlcy1maWxlcy10ZXN0IiwiZGVhZGxpbmUiOjE3MDY3NTQwMzZ9",
# }
# files = {}
# # 获取当前程序所在目录
# current_dir = os.getcwd()
# # 获取当前目录下的所有文件和目录名称
# contents = os.listdir(current_dir)
# for i in contents:
#     timestamp = time.time()
#     timestamp = int(timestamp * 1000)
#     key = "uaZiZz_" + str(timestamp) + ".jpg"
#     body_data["key"] = key
#     jpg_files = glob.glob(f"{i}/*.jpg")
#     print(jpg_files)
#     for path in jpg_files:
#         file = open(path, 'rb')
#         files[key] = file
#     # 上传图片
#     response = requests.post(url="https://up-z2.qiniup.com", headers=headers, json=body_data, files=files)
#     print(response.text)