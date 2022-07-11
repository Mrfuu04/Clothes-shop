# GeekShop

## _Проект интернет магазина_

## Запуск
```sh
* git clone git@github.com:Mrfuu04/Geekshop.git

* В корневой папке создать файл .env
* В .env задать SECRET_KEY='любое значение'
* Переопределить GSRegisterView.post() в authapp для отключения подтверждения по письму 
```

### Для запуска в Docker
```sh
в settings.py:
SERVER = False
DOCKER = True

docker-compose up -d
```
Запускается локальный сервер на localhost:8080

* При SERVER = False и DOCKER = False используется sqlite3, иначе Postgres
