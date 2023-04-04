import nextcloud_client
from django.shortcuts import render

from link_sender.settings import NC_PASS, NC_LOGIN
from linker.logic import getid_url, connect_db, get_path, create_url, send_email


# Create your views here.
def index(request):
    if request.method == 'POST':
        nc = nextcloud_client.Client('https://cloud.peterphoto.ru')
        nc.login(NC_LOGIN, NC_PASS)
        modern = '/modern'
        email = request.POST.get('email')
        url = request.POST.get('url')
        # file = "/Фото/Бескровных Екатерина/Декабрь/5.12 ПЦ/2 нд/исх/750A9021.jpg"
        # Получить ID файла из URL
        fileid = getid_url(url)
        # Получить путь к файлу из базы данных
        connection = connect_db()
        path = modern + get_path(fileid, connection)
        # Создать URL-ссылку с паролем на файл
        link, password = create_url(path)
        print(f"Link: {link}\nPassword: {password}")
        send_email(to=email, body=f"Link: {link}\nPassword: {password}")
    return render(request, 'index.html')
