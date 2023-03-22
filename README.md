### Краткое описание:

Проект "Продуктовый помощник", сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

Данный проект является результатом изучения основ бэкенд-разработки в Яндекс Практикуме.

### Как запустить проект:

Клонировать репозиторий:
```
git clone  git@github.com:AFrantsevich/foodgram-project-react.git
```

Скопировать файлы:
```
docker-compose.yaml и infra/nginx.conf
в home/<ваш_username>/docker-compose.yaml 
и home/<ваш_username>/nginx.conf соответственно.
```

Добавить файл .env в директорию /infra:

```
SECRET_KEY = ''
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Скопировать файлы:
```
docker-compose.yaml и infra/nginx.conf
в home/<ваш_username>/docker-compose.yaml 
и home/<ваш_username>/nginx.conf соответственно.
```


В папке infra выполните команду:
```
docker-compose up
```

Сделайте миграциии и создайте суперпользователя:
```
docker-compose exec backend python manage.py migrate

sudo docker-compose exec backend python manage.py createsuperuser
```

После этого проект запустился по адресу:
```
http://localhost/
```

Ключевые эндпоинты:
```
http://localhost/admin - админка сайта

http://localhost/api/docs/ - документация API
```


### Данные по развернутому проекту:

Ip:

```
94.198.220.15
```

Доступ к админке:

```
94.198.220.15/admin

Login: Andrey

Password: Andrey93
```

### Технологии:
```
Python
```
```
Django, Django REST framework
```

```
Docker, Docker - Compose
```
```
React
```