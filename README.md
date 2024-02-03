# Магазин с оплатой

## Описание

Проект представляет собой простой сайт-магазин, при покупке товаров в котором происходит переход на сервис оплаты stripe.

## Функции
· 	Просмотр всех товаров и их индивидуальных страниц

· 	Возможность добавить товар и корзину и убрать его. Доступна страница корзины

· 	Покупка товаров через сервис оплаты stripe 

· 	Учёт заранее заданных налогов и скидок при оплате заказа

## Используемые инструменты

- Python
- Django (Web framework)
- HTML/CSS
- PostgreSQL (Database)
- Stripe API

## Демонстрация

### Главная страница
![Demonstration](https://github.com/amrylnikov/stripe_api/blob/main/demonstration/1.PNG?raw=true)

### Страница конкретного товара
![Demonstration](https://github.com/amrylnikov/stripe_api/blob/main/demonstration/2.PNG?raw=true)

### Оплата товара
![Demonstration](https://github.com/amrylnikov/stripe_api/blob/main/demonstration/3.PNG?raw=true)

### Страница корзины
![Demonstration](https://github.com/amrylnikov/stripe_api/blob/main/demonstration/4.PNG?raw=true)

### Оплата корзины
![Demonstration](https://github.com/amrylnikov/stripe_api/blob/main/demonstration/5.PNG?raw=true)

### Панель администратора
![Demonstration](https://github.com/amrylnikov/stripe_api/blob/main/demonstration/6.PNG?raw=true)

### Видео работы приложения
https://www.youtube.com/watch?v=MzpebwZW_7s

## Запуск 

- Используйте эту команду для настройки проекта:
> pip install --upgrade poetry && poetry build && poetry install
- Используйте эту команду, чтобы запустить проект:
> python manage.py runserver