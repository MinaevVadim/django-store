# Создание интернет-магазина


Аналоги интернет-магазина: holodilnik.ru, citilink.ru, ozon.ru.
Проект разработан на фреймворке Django.

* реальное eCommerce приложение написанное на Python;
* реализована кастомная модель пользователя (регистрация и логирование пользователей по email и паролю);
* регистрация, логирование пользователей, изменение пароля;
* создание товаров с описанием, ценами, фото и т.д. по категориям;
* карточка товара с описанием, фото, вариациями и галереей фото товара;
* корзина, изменение количества товаров, удаление товаров;
* пагинация и поиск; 
* отзывы товаров;
* личный кабинет с возможностью просмотра заказов, изменение профиля, пароля; 
* для удобства использования и администрирования сайта реализована админ панель со всеми необходимыми настройками.
* реализация сервер очередей Celery в связке с redis

### Используемые инструменты

* Django
* Python 3
* celery
* redis
* Postgres
* HTML, CSS, JavaScript, Bootstrap

### Установка

* запустите проект с помощью команды
```
docker compose up -d
```

* Команда для создания миграций приложения для базы данных
```
python manage.py migrate
```

* Команда для загрузки фикстур в проект
```
python manage.py loaddata fixtures_user.json
                 fixtures_profile.json
                 fixtures_tags.json
                 fixtures_categories.json 
                 fixtures_products.json
                 fixtures_files_products.json
```
