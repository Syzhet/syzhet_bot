![Build Status](https://github.com/Syzhet/khas_telegram_bot/actions/workflows/khasbot.yml/badge.svg)


# khas_telegram_bot

## Телеграм-бот ассистент для графического дизайнера.

Исходный функционал:
- Предоставление информации о типах услуг.
- Возможность оформить заявку на оказание услуши.
- Предоставление ссылок на образцы работ.
- Запрос обратной связи.

Запланированное расширение:
- Подключение базы данных для хранения заявок и регистрации пользователей.
- Изолированный функционал для владельца бота по работе с БД.
- Возможность взаимодействия бота по REST API.


## Стек технологий 

<div>
  <a href="https://www.python.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  </a>
  <a href ="https://www.docker.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://github.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/github/github-original.svg" title="GitHub" alt="GitHub" width="40" height="40"/>&nbsp;
  </a>
</div>

Версии ПО:

- python: 3.10.4;
- aiogram: 2.22.1;
- Docker: 20.10.18;
- docker-compose: 1.26.0;


# Установка проекта локально
Склонировать репозиторий на локальную машину:
```sh
git clone https://github.com/Syzhet/khas_telegram_bot.git
```
Cоздать и активировать виртуальное окружение:
```sh
python -m venv venv
source venv/bin/activate
```
Cоздайте файл .env в корневой директории проекта содержанием:
- BOT_TOKEN= токен телеграм-бота, полученный у @BotFather
- ADMIN_ID= id администратора бота, полученный у @userinfobot
- HOST_ID= id владельца бота, полученный у @userinfobot

Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```


# Запуск проекта в Docker контейнере
Установите Docker и docker-compose
```sh
sudo apt install docker.io 
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Параметры запуска описаны в файлах docker-compose.yml.

Запустите docker-compose:
```sh
sudo docker-compose up -d
```

После сборки появляется 1 контейнер:

| Контайнер | Описание |
| ------ | ------ |
| khasbot | контейнер с запущенным ботом |


## Пример работы бота
- @KhasGuzBot

## Авторы проекта

- [Ионов А.В.](https://github.com/Syzhet) - Python разработчик.
