import smtplib
import base64

# Gmail账户信息
gmail_user = 'xxx@gmail.com'
gmail_password = 'xxx'

# SMTP服务器信息
smtp_server = "smtp.gmail.com"
smtp_port = 587  # 使用TLS

try:
    # 创建SMTP连接
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)  # 打开调试模式
    server.ehlo()
    server.starttls()
    server.ehlo()

    # 登录到SMTP服务器
    server.login(gmail_user, gmail_password)
    
    print("SMTP登录成功。")
except Exception as e:
    print(f"SMTP登录失败：{e}")
finally:
    server.quit()
