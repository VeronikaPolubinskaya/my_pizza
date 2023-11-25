import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypizza.settings')

app = Celery('mypizza')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_routes = {
    'tasks.payment': {'queue': 'payment'},
    'tasks.order_created': {'queue': 'order_created'},
    'tasks.delivery': {'queue': 'delivery'},
    'tasks.delivered': {'queue': 'delivered'}
}


#мы говорим Celery автоматически обнаруживать асинхронные задачи
# для приложений, перечисленных в параметрах INSTALLED_APPS.
# Celery будет искать файл tasks.py в каждом каталоге приложения
# для загрузки определенных в нем асинхронных задач.