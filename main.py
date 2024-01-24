import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import phonenumbers
import re
import requests
import json
import msvcrt

headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2104K10AC Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.210 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/34.909092)",
        "Content-Type": "application/json",
        "Content-Length": "78",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

# 先输入登入信息
# 获取用户要检测的屏幕组
# 查询接口获取屏幕列表以及在线状态
# 设备状态发生变化发送邮件，在线变离线发送离线提醒，离线变在线发送上线提醒

def is_valid_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if email_pattern.match(email):
        return True
    else:
        return False


def phone_number_format_validation(phone):
    try:
        parsed_number = phonenumbers.parse(f'+{phone}')
        is_valid_number = phonenumbers.is_valid_number(parsed_number)
        phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        if is_valid_number:
            print(f"号码：{phone_number}校验通过")
            return phone_number[len(str(parsed_number.country_code)) + 1:]
        else:
            print(f"号码：{phone}校验失败")
            return False
    except phonenumbers.NumberParseException as e:
        print(f"号码解析异常,请确认是否输入区号{e}")


# 校验账号是邮箱还是手机号
def check_account(account):
    if is_valid_email(account):
        account_type = 'email'
        return account_type
    elif phone_number := phone_number_format_validation(account):
        account_type = 'phone'
        return account_type, phone_number
    else:
        return False


def check_password(passwd):
    # 检查长度是否在6-12之间
    if 6 <= len(passwd) <= 12:
        # 检查是否由字母和数字组成
        if passwd.isalnum():
            return passwd
        else:
            print("输入必须由字母和数字组成，请重新输入。")
            return False
    else:
        print("输入长度不符合要求，请重新输入。")
        return False


def login():
    data = {
        "account": None,
        "password": None,
        "areaCode": None,
        "loginType": None
    }

    while True:
        area = input("请选择地区：\n1. 中国-测试环境\n2. 中国-正式环境\n3. 美国-测试环境\n4. 美国-正式环境\n")
        if area == '1':
            server = '139.224.192.36:8082'
            data['areaCode'] = '+86'
        elif area == '2':
            server = 'cloud-service.austinelec.com:8080'
            data['areaCode'] = '+86'
        elif area == '3':
            server = '52.53.201.220:8080'
            data['areaCode'] = '+1'
        elif area == '4':
            server = '52.53.201.220:8080'
            data['areaCode'] = '+1'
        else:
            print('地区输入错误,请重新输入！')
            continue
        login_interface = 'http://' + server + '/api/v1/account/login'
        while True:
            account = input('请输入账号：')
            if account != "":
                account_result = check_account(account)
                # 邮箱登录
                if isinstance(account_result, str):
                    data['account'] = account
                    data['loginType'] = '3'
                    data.pop('areaCode')
                    break
                # 手机登录
                elif isinstance(account_result, tuple) and account_result[0] == 'phone':
                    data['account'] = account_result[1]
                    data['loginType'] = '2'
                    break
                else:
                    print('账号格式不正确,请重新输入！')
                    continue
            else:
                print('账号不能为空,请重新输入！')
        while True:
            passwd = input('请输入密码：')
            result = check_password(passwd)
            if isinstance(result, str):
                data['password'] = result
                break
            else:
                continue

        data_tmp = json.dumps(data)
        response = requests.post(login_interface, data=data_tmp, headers=headers)
        response = response.json()
        message = response['message']
        cookie = response['data']
        if message == '成功':
            print('登录成功')
            return cookie
        else:
            print(message)

def get_groupid():
    pass


def get_screen_list():
    pass


def check_online():
    pass


# # 邮件配置信息
# smtp_server = 'smtp.qq.com'
# smtp_port = 587  # 一般为587或465
# smtp_username = '2698567570@qq.com'
# smtp_password = 'ruppilfmltsjdgbj'
# sender_email = '2698567570@qq.com'
# receiver_email = '2698567570@qq.com'
# subject = 'Test Email'
#
# # 邮件正文
# body = '你的设备离线啦！.'
#
# # 创建邮件对象
# message = MIMEMultipart()
# message['From'] = sender_email
# message['To'] = receiver_email
# message['Subject'] = subject
#
# # 添加邮件正文
# message.attach(MIMEText(body, 'plain'))
#
# # 如果需要附件，可以添加附件
# # attachment = open('file.txt', 'rb')
# # attach_part = MIMEApplication(attachment.read(), Name='file.txt')
# # attachment.close()
# # attach_part['Content-Disposition'] = 'attachment; filename="file.txt"'
# # message.attach(attach_part)
#
# # 连接到 SMTP 服务器并发送邮件
# try:
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         # 开启 TLS 连接
#         server.starttls()
#
#         # 登录邮箱
#         server.login(smtp_username, smtp_password)
#
#         # 发送邮件
#         server.sendmail(sender_email, receiver_email, message.as_string())
#
#     print('Email sent successfully.')
# except Exception as e:
#     print(f'Error: {e}')
login()
