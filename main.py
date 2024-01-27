import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import phonenumbers
import re
import requests
import json
import traceback
import sys

headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
    "user-agent": "Mozilla/5.0 (Linux; Android 13; M2104K10AC Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/34.909092)",
}
server = ""
groupid = ""


def log_exception(exception):
    # 将异常信息写入文件
    with open('/log/exception_log.txt', 'w') as f:
        f.write("Exception Type: {}\n".format(type(exception).__name__))
        f.write("Exception Value: {}\n".format(exception))
        f.write("Traceback:\n")
        traceback.print_exc(file=f)

def is_valid_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if email_pattern.match(email):
        return True
    else:
        return False

def send_email(subject="Pintura：您的设备离线啦！", message=""):
    # 邮件配置信息
    smtp_server = 'smtp.qq.com'
    smtp_port = 587  # 一般为587或465
    smtp_username = '2698567570@qq.com'
    smtp_password = 'ruppilfmltsjdgbj'
    sender_email = '2698567570@qq.com'
    receiver_email = '2698567570@qq.com'
    # 邮件正文
    body = message

    # 创建邮件对象
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # 添加邮件正文
    message.attach(MIMEText(body, 'plain'))

    # 如果需要附件，可以添加附件
    # attachment = open('file.txt', 'rb')
    # attach_part = MIMEApplication(attachment.read(), Name='file.txt')
    # attachment.close()
    # attach_part['Content-Disposition'] = 'attachment; filename="file.txt"'
    # message.attach(attach_part)

    # 连接到 SMTP 服务器并发送邮件
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # 开启 TLS 连接
            server.starttls()

            # 登录邮箱
            server.login(smtp_username, smtp_password)

            # 发送邮件
            server.sendmail(sender_email, receiver_email, message.as_string())

        print('Email sent successfully.')
    except Exception as e:
        print(f'Error: {e}')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Error: {e}')
    except smtplib.SMTPRecipientsRefused as e:
        print(f'Error: {e}')
    except smtplib.SMTPServerDisconnected as e:
        print(f'Error: {e}')
    except smtplib.SMTPException as e:
        print(f'Error: {e}')
    except smtplib.SMTPSenderRefused as e:
        print(f'Error: {e}')
    except smtplib.SMTPDataError as e:
        print(f'Error: {e}')
    except smtplib.SMTPConnectError as e:
        print(f'Error: {e}')

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
        global server
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
                    print('账号格式不正确,请重新输入！如果账号为手机号，需要携带区号，如：8612345678901')
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
        try:
            response = requests.post(login_interface, data=data_tmp, headers=headers)
            response.close()
            response = response.json()
        except json.decoder.JSONDecodeError:
            log_exception("JSON解码错误")
        except Exception as e:
            print(e)

        message = response['message']
        cookie = response['data']
        if message == '成功':
            print('登录成功')
            return cookie
        else:
            print(message)


def get_groupid():
    cookie = login()
    group_interface = 'http://' + server + '/api/v1/host/screen/group/device/list'
    global headers
    headers['X-TOKEN'] = cookie
    headers['Content-Type'] = 'application/json, text/plain, */*'
    try:
        response = requests.get(group_interface, headers=headers, timeout=(5, 10))
        response.raise_for_status()  # 检查是否有错误状态码
        response.close()
        # 处理响应数据
        response = response.json()
        data = response['data']['group']
        screen_group = []
        group_id = []
        for i in data:
            screen_group.append(i['name'])
            group_id.append(i['id'])
        message = ""
        for index, value in enumerate(screen_group):
            message += str(index + 1) + "： " + value + "\n"
        while True:
            selection_id = input(f"请选择要监视的屏幕组：\n{message}")
            try:
                selection_id = int(selection_id) - 1
                break
            except ValueError:
                print("输入无效，请输入数字选项！")
                continue
        selection_id = group_id[selection_id]
        global groupid
        groupid = str(selection_id)
        print("即将进入检测模式")
    except json.decoder.JSONDecodeError:
        log_exception("JSON解码错误")
    except requests.Timeout:
        print("请求超时,程序即将退出")
        time.sleep(2)
        sys.exit()
    except Exception as e:
        print(f"请求发生错误: {e}")



def get_screen_list():
    try:
        screen_list_interface = 'http://' + server + '/api/v1/host/screen/group/list/relation?screenGroupId=' + groupid
        response = requests.get(screen_list_interface, headers=headers)
        response.close()
        response = response.json()
        data = response['data']
        screens = {}
        offline_screens = []
        for i in data:
            screens[f'{i["screenId"]}'] = i['status']
        for key, value in screens.items():
            if value == 2:
                offline_screens.append(key)
        return offline_screens
    except json.decoder.JSONDecodeError:
        log_exception("JSON解码错误")
    except Exception as e:
        log_exception(e)


def check_online():
    get_groupid()
    last_offline_screens = []
    print('\n' * 5, '\033[1;31;40m 按 Ctrl + C 退出程序 \033[m')
    msg = '检测中...'
    while True:
        sys.stdout.write('\r' + " " * len(msg))
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write('\r' + msg)
        sys.stdout.flush()
        time.sleep(0.5)
        offline_screen_list = get_screen_list()
        if offline_screen_list:
            if offline_screen_list and offline_screen_list != last_offline_screens:
                print('发现离线屏幕：\n', offline_screen_list)
                message = f"发现离线屏幕：\n{offline_screen_list}"
                send_email(message=message)
                last_offline_screens = offline_screen_list
        else:
            last_offline_screens = []


try:
    check_online()
except Exception as e:
    log_exception(e)