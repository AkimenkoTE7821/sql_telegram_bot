# Telegram-бот для тестирования по SQL (PostgreSQL)

## Описание
Данный проект представляет собой Telegram-бота для тестирования и обучения навыкам работы с SQL-запросами в PostgreSQL. Бот поддерживает два режима: обучение (с пояснениями) и контроль (оценка после теста).

## Требования
- Python 3.8+
- Библиотека [python-telegram-bot](https://python-telegram-bot.org/)

## Установка и запуск

1. Клонируйте репозиторий:
``` 
git clone https://github.com/yourusername/sql-telegram-bot.git
cd sql-telegram-bot 
```
2. Установите зависимости:
```
pip install python-telegram-bot
```
3. Зарегистрируйте Telegram-бота через [@BotFather](https://t.me/BotFather) и получите токен.
4. Вставьте ваш токен в файл `main.py`:
```
app = Application.builder().token("ВАШ_ТОКЕН_ЗДЕСЬ").build()
```
5. Запустите бота:
```
python main.py
```
## Структура файлов
- `main.py` — основной код бота
- `questions.json` — вопросы теста (пример структуры внутри файла)
- `results.json` — результаты пользователей
- `README.md` — инструкция по запуску
- `report.docx/pdf` — отчёт по лабораторной работе

## Пример вопроса (questions.json)
```
{
"id": 1,
"question": "Как выбрать все столбцы и записи из таблицы musicians?",
"options": [
"SELECT * FROM musicians;",
"SELECT ALL FROM musicians;",
"SELECT columns FROM musicians;"
],
"correct_option": 0,
"explanation": "В PostgreSQL для вывода всех столбцов и записей используется SELECT * FROM table_name;."
}
```

## Пример работы
*(Добавьте скриншоты работы бота)*



