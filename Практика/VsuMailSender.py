import os
import smtplib
import sys
import csv
import time
from configparser import ConfigParser

status_dict = ["SUCCESS ", "WARNING ", "ERROR "]

base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, "config.ini")
if os.path.exists(config_path):
    cfg = ConfigParser()
    cfg.read(config_path)
else:
    print(status_dict[0] + "Файл конфига не найден!")
    input("Нажмите любую клавишу...")
    sys.exit(1)

message_recipients = ""
message_sender = cfg.get("smtp", "from_addr")
message_subject = "Test"
message_text = "test"


def send_email(subject, mail_text, to_addr):
    host = cfg.get("smtp", "server")  # Адрес сервера из конфига
    from_addr = cfg.get("smtp", "from_addr")  # Адрес отправителя из конфига
    from_addr_password = cfg.get("smtp", "from_addr_password")  # Пароль отправителя из конфига

    mail_body = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        mail_text
    ))

    server = smtplib.SMTP_SSL(host)
    server.login(from_addr, from_addr_password)
    server.sendmail(from_addr, [to_addr], mail_body)
    server.quit()


if __name__ == '__main__':
    with open("contacts_file.csv") as mail_dict:
        reader = csv.DictReader(mail_dict, delimiter=',')
        for line in reader:
            message_recipients = line["email"]
            print(message_recipients)
            send_email(message_subject, message_text, message_recipients)
            time.sleep(5)
        print("\n" + status_dict[0] + "Done!")
        sys.exit(1)