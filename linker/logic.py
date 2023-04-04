import nextcloud_client
import psycopg2
from django.core.mail import EmailMessage
from psycopg2 import Error
import re
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from link_sender.settings import NC_LOGIN, NC_PASS

nc = nextcloud_client.Client('https://cloud.peterphoto.ru')
nc.login(NC_LOGIN, NC_PASS)


def connect_db():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="1111",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres_db")
    except (Exception, Error) as error:
        print("Ошибка при подключении к PostgreSQL", error)
        connection = None
    return connection


def get_path(fileid, connection):
    if not connection:
        print("Соединение с PostgreSQL не установлено")
        return
    cursor = connection.cursor()
    try:

        postgresql_select_query = "select path from oc_filecache where fileid = %s"
        cursor.execute(postgresql_select_query, (fileid,))
        path = cursor.fetchall()
        print(path)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def getid_url(url):
    if url:
        find = re.split(r'fileid=|/f/', url)
        fileid = find[1]
        if fileid:
            return fileid
        else:
            raise ValueError("Проблема с парсингом")
    else:
        raise ValueError("Не задана урла")


def create_url(file):
    password = secrets.token_urlsafe(8)
    if file:
        link_info = nc.share_file_with_link(file, password=password)
        return link_info.get_link(), password
    else:
        raise ValueError("Не задана урла")


def main():
    file = "/modern/Фото/Бескровных Екатерина/Декабрь/5.12 ПЦ/2 нд/исх/750A9021.jpg"

    # Получить ID файла из URL
    url = "your_url_here"
    fileid = getid_url(url)
    # Получить путь к файлу из базы данных
    connection = connect_db()
    get_path(fileid, connection)
    # Создать URL-ссылку с паролем на файл
    link, password = create_url(file)
    print(f"Link: {link}\nPassword: {password}")


def send_email(to, body):
    subject = 'Ссылка'
    from_email = 'mailbot@verweb.dev'  # замените на свой адрес электронной почты
    message = body
    email = EmailMessage(subject, message, from_email, [to])
    email.send()
