import asyncio
import json
import random
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def send_email(smtp, recipient_email, account_info, send_count):
    # 检查发件账户的发送限制
    if send_count[account_info['email']] >= 450:
        print(f"{account_info['email']} has reached its daily limit.")
        return

    msg = MIMEMultipart()
    msg['Subject'] = subject  # 使用定义的主题
    msg['From'] = account_info['email']
    msg['To'] = recipient_email

    # 使用 HTML 内容
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        await smtp.send_message(msg)
        send_count[account_info['email']] += 1  # 更新发送计数
        print(f"Email sent successfully from {account_info['email']} to {recipient_email}.")
        
    except Exception as e:
        print(f"Failed to send email from {account_info['email']} to {recipient_email}. Error: {e}")
        if 'Connection lost' in str(e) or 'Server not connected' in str(e) or 'Connection expired' in str(e):
            # 如果连接已过期，请重新连接
            await smtp.quit()
            wait_time = random.randint(300, 500)
            print(f"Error: {e}, Waiting for {wait_time} seconds. Reconnect SMTP ")
            await asyncio.sleep(wait_time)
            smtp = await create_smtp_session(account_info)
            await send_email(smtp, recipient_email, account_info, send_count)

async def create_smtp_session(account_info):
    smtp = SMTP(hostname='smtp.gmail.com', port=465, use_tls=True)
    await smtp.connect()
    await smtp.login(account_info['email'], account_info['password'])
    return smtp

async def main():
    with open('workers_config.json', 'r') as file:
        accounts = json.load(file)

    input_file_path = 'input_file/inputfile.txt'
    with open(input_file_path, 'r') as file:
        customer_emails = [line.strip() for line in file.readlines()]

    # 初始化每个账户的邮件发送计数
    send_count = {account['email']: 0 for account in accounts.values()}

    smtp_sessions = {}
    all_tasks = []
    for account_key, account_info in accounts.items():
        smtp_sessions[account_key] = await create_smtp_session(account_info)

    for idx, email in enumerate(customer_emails):
        account_key = list(accounts.keys())[idx % len(accounts)]
        account_info = accounts[account_key]
        smtp = smtp_sessions[account_key]
        
        if idx > 0:  # 在发送非第一封邮件之前加入随机等待
            wait_time = random.randint(10, 15)  # 生成随机等待时间
            print(f"Waiting for {wait_time} seconds before sending the next email.")
            await asyncio.sleep(wait_time)
        
        # 创建并执行发送任务
        task = asyncio.create_task(send_email(smtp, email, account_info, send_count))
        all_tasks.append(task)

    # 等待所有邮件发送完成
    await asyncio.gather(*all_tasks)

    # 关闭所有SMTP连接
    for smtp in smtp_sessions.values():
        await smtp.quit()

subject = "Enhance Your Brand with Earth Lab's Eco-Friendly Swag"
html_content = """
<!DOCTYPE html>
<html>
<body>
    <p>Dear Sir/Madam,</p>
    
    <p>Greetings from Earth Lab, where sustainability meets corporate swag. I'm Frank Xu, Senior Sales Director for North America. We specialize in eco-conscious promotional items crafted from recycled materials, aimed at elevating your brand while aligning with your environmental values.</p>

    <p>If you're interested in making a positive impact with your branding efforts and wish to explore our offerings, we'd be delighted to share our product catalogue with you. Additionally, we can arrange a Zoom meeting to discuss our sustainable solutions in detail.</p>

    <p>Looking forward to supporting your sustainable branding journey.</p>

    <p>Best regards,</p>
    <p>Frank Xu<br>Senior Sales Director<br>Earth Lab</p>
</body>
</html>

"""

asyncio.run(main())
