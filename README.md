# MegaMarket
Задание для Yandex Academy 2022

## Сборка и развертывание сервиса
### В Docker контейнере
Склонируйте проект и в папке с проектом и запустите:
```sh
docker-compose up -d
```
Сервис будет запушен на ```localhost:80```

## Документация
Документацию можно посмотреть по адресу https://protect-2043.usr.yandex-academy.ru/docs.  
Или после запуска сервиса на вашем компьютере по адресу http://localhost/docs.

## Тесты
Тесты находятся в папке ```tests```
Чтобы запустить тесты внутри Docker контейнера, выполните следующую команду в папке с проектом:
```shell
docker exec -it megamarket_web_1 pytest
```
