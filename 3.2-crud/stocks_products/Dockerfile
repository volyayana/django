FROM python:3.8
WORKDIR /django-code
RUN git clone https://github.com/volyayana/django.git
RUN pip install -r /django-code/django/3.2-crud/stocks_products/requirements.txt
EXPOSE 8000
CMD python /django-code/django/3.2-crud/stocks_products/manage.py migrate
CMD cd /django-code/django/3.2-crud/stocks_products && gunicorn stocks_products.wsgi -b 0.0.0.0:8000