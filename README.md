## Приложение для архивации и генерации случайных данных.

Возможности:
- Генерация случайных данных пользователя в таблицу формата xlsx, csv, txt до 2 млн. строк.
- Упаковка сгенерированной таблицы в zip или 7z.
- Упаковка пользовательских файлов в zip или 7z.
- 7z поддерживает разбиение на части.

#
### Для запуска необходимо активировать виртуальное окружение и установить зависимости из requirements.txt.


## Linux / macOS

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r requirements.txt

## Windows

python -m venv venv

venv\Scripts\activate.bat

python -m pip install -r requirements.txt

#
### Протестировано на Python 3.12.

### Точка входа - main.py.
