![logo](https://user-images.githubusercontent.com/74112037/142832530-dbe22c2c-d260-4d9f-843b-91b2815ee100.png)

## **Телеграм бот для сайта http://innovations.kh.ua/khnews/**
>Бот создан для парсинга последних новостей с сайта с помощью Python.
>Так же подключены различные API, на данный момент OpenWeather выдаёт информацию о погоде.

### [⛏ChangeLogs(LINK)](https://github.com/Jylik322/kh-news-bot/blob/main/CHANGELOG.md)


## 💾 Project Files Description:

- #### *images - папка с картинками проекта*
- #### newsbot.py - Главный скрипт который работает на сервере и совмещает в себе все другие
- #### parsing.py - Скрипт парсинга новостей с сайта и сохранения
- #### payment.py - Скрипт для работы с платежами внутри бота
- #### requirements.txt - Файл требований для работы Heroku
- #### runtime.txt - Python Version
- #### weather.py - Open Weather API, получаем информацию о погоде
- #### Procfile - Файл для подключения Dyno Heroku

## 📱Команды бота:
### /start - Запуск бота
### /weather - Посмотреть информацию о погоде в Харькове
### /news - Посмотреть последние новости
### /help - Список доступных команд.
