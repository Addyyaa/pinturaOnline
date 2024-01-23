import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 邮件配置信息
smtp_server = 'smtp.qq.com'
smtp_port = 587  # 一般为587或465
smtp_username = '2698567570@qq.com'
smtp_password = 'ruppilfmltsjdgbj'
sender_email = '2698567570@qq.com'
receiver_email = '2698567570@qq.com'
subject = 'Test Email'

# 邮件正文
body = 'Hello, this is a test email from Python.'

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
