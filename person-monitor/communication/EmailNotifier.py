import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailNotifier:
    __EMAIL_HOST = 'smtp.gmail.com'
    __EMAIL_PORT = 587

    def __init__(self, sender_email_address: str, sender_password):
        self.__sender_email_address = sender_email_address
        self.__sender_password = sender_password

    def send_alert(self, email_address: str, subject: str, body: str) -> None:
        address = self.__email_config.sender_address
        receiver = self.__home_defence_config.notified_email_address
        msg = MIMEMultipart()
        msg['From'] = self.__sender_email_address
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(self.__EMAIL_HOST, self.__EMAIL_PORT)
        try:
            server.starttls()
            server.login(self.__sender_email_address, self.__sender_password)
            text = msg.as_string()
            server.sendmail(self.__sender_email_address, email_address, text)
            server.quit()
        except Exception as e:
            print(e)