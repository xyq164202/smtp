import asyncio
import json
import random
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def send_email(smtp, recipient_email, account_info, send_count):
     # 在发送之间加入随机等待
    await asyncio.sleep(random.randint(10, 15))
    
    # 检查发件账户的发送限制
    if send_count[account_info['email']] >= 450:
        print(f"{account_info['email']} has reached its daily limit.")
        return

    msg = MIMEMultipart()
    msg['Subject'] = 'Your Marketing Campaign'
    msg['From'] = account_info['email']
    msg['To'] = recipient_email
    msg.attach(MIMEText('This is your marketing message.', 'plain'))
    
    try:
        await smtp.send_message(msg)
        send_count[account_info['email']] += 1  # 更新发送计数
        print(f"Email sent successfully from {account_info['email']} to {recipient_email}.")
        
    except Exception as e:
        print(f"Failed to send email from {account_info['email']} to {recipient_email}. Error: {e}")

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
        
        # 创建并执行发送任务
        task = asyncio.create_task(send_email(smtp, email, account_info, send_count))
        all_tasks.append(task)

    await asyncio.gather(*all_tasks)

    # 关闭所有SMTP连接
    for smtp in smtp_sessions.values():
        await smtp.quit()

asyncio.run(main())
