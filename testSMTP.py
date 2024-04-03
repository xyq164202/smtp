import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import random
import os

def read_email_list_from_file(file_path):
    """
    从给定的文本文件中读取电子邮件地址并返回一个列表。
    """
    with open(file_path, 'r') as file:
        emails = [line.strip() for line in file if line.strip()]
    return emails

# Gmail账户信息
sender_email = 'frankxuearthlab@gmail.com'
password = 'arsqkufvcxtrreyd'

# SMTP服务器设置
smtp_server = "smtp.gmail.com"
smtp_port = 587  # 使用TLS

# 读取电子邮件地址
base_path = '/Users/qinyaoxu/Downloads/split'
file_paths = [f"{base_path}/email_group_{i}.txt" for i in range(1, 33) if os.path.exists(f"{base_path}/email_group_{i}.txt")]


# 选择一个文件作为示例
selected_file = file_paths[8]  # 例如，只读取第一个文件的电子邮件地址
recipients = read_email_list_from_file(selected_file)

# 定义邮件内容
subject = "Elevate Your Brand with Earth Lab's Sustainable Swag"
html_content = """
<html>
<body>
    <p>Dear Sir/Madam,</p>
    
    <p>I hope this message finds you well. I'm Frank Xu, Senior Sales Director for North America at Earth Lab. We specialize in creating sustainable swag from recycled materials, blending environmental stewardship with innovative design. Our mission is to help brands like yours make a meaningful statement through high-quality, eco-conscious promotional items.</p>

    <p>Our curated swag collection is designed to align with your sustainability goals and enhance your brand's impact. I invite you to explore our catalogue  <a href="https://www.earthlab.live/_files/ugd/f18b02_682b39925964414a8bd0327a4be4c4d5.pdf">here</a>, showcasing our range of sustainable swag options.</p>

    <p>If you're interested, I’d love to discuss how our products can complement your branding efforts in a Zoom meeting.</p>

    <p>Looking forward to the opportunity to collaborate and help enhance your brand with our sustainable swag.</p>

    <p>Best regards,</p>
    <p>Frank Xu<br>Senior Sales Director<br>Earth Lab</p>
</body>
</html>
"""

# 发送邮件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, password)
    
    for recipient in recipients:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        server.sendmail(sender_email, recipient, msg.as_string())
        print(f"邮件成功发送给 {recipient}")

        # 随机暂停1到7秒
        sleep_time = random.randint(1, 7)
        print(f"等待 {sleep_time} 秒...")
        time.sleep(sleep_time)
    
    server.quit()
except Exception as e:
    print(f"邮件发送失败：{e}")
