# Menu
Приложение для создания своего Django template tag "draw_menu".
Определяет текущий пункт меню по url, рекурсивно раскрывает все меню выше данного пункта, 
плюс один дочерний уровень, если он есть.

Работает с несколькими меню на одной странице. Для каждого меню на странице используется один запрос к БД

## Использование
* установка зависимостей
```
pip install -r requirements.txt
```
* create superuser
```
python manage.py createsuperuser
```
* migrations для тестирования
```
python manage.py makemigrations
python manage.py migrate
```
* загрузите templatetags на вашей странице
```
{% load draw_menu_tags %}
```
* сформируется меню по названию меню в вашей БД
```
<div class="some-class">
    {% draw_menu 'main_menu' %}
</div>
```
Меню будет формироваться автоматически, основываясь на текущей странице.
* можно формировать сразу несколько меню на странице
```
<div class="main_menu-class">
    {% draw_menu 'main_menu' %}
</div>

<div class="footer_menu-class">
    {% draw_menu 'footer_menu' %}
</div>
```
* запустите проект
```
python manage.py runserver
```