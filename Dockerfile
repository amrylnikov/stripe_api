FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=stripe_demo.settings

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
