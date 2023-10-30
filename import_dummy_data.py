import os
import csv
import django
from django.core.wsgi import get_wsgi_application
from django.conf import settings

from posts.models import Posts


import random
from faker import Faker  # 더미 데이터를 생성하기 위한 라이브러리


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()


django.setup()
# settings.configure()


def import_dummy_data():
    with open('dummy_data.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Posts.objects.create(
                content_id=row['content_id'],
                type=row['type'],
                title=row['title'],
                content=row['content'],
                view_count=int(row['view_count']),
                like_count=int(row['like_count']),
                share_count=int(row['share_count']),
            )

if __name__ == '__main__':
    import_dummy_data()
