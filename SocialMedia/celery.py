# myproject/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialMedia.settings')

app = Celery('SocialMedia')

# تنظیمات celery از تنظیمات Django بارگذاری شود
app.config_from_object('django.conf:settings', namespace='CELERY')

# این قسمت برای اینکه همه taskهای تعریف شده در اپ‌های Django را کشف کند
app.autodiscover_tasks()
