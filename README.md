# Приложение "Форум"

Стек (python3.9, Django 4.1.2, Postgres 14)

Для создания базы Postgres в Docker локально требуется воспользоваться командой docker-compose up -d.

Для создания образа базы postgres:
docker exec -i library-postgres-1 --username library --password library library_db > C:\Users\Admin\Desktop\library/library.sql
