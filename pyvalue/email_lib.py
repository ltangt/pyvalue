# The library for sending the notification email
# Author: Liang Tang
# License: BSD

import smtplib
from email.mime.text import MIMEText


def send(msg, subject, src_addr, dest_addr):
    email_msg = MIMEText(msg)
    email_msg['Subject'] = subject
    email_msg['To'] = dest_addr
    email_msg['From'] = src_addr
    s = smtplib.SMTP('localhost')
    s.sendmail(src_addr, [dest_addr], email_msg.as_string())
    s.quit()
