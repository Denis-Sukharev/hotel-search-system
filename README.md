# Инстуркция по установке и запуске программного обеспечения для оптимизации маршрутов путешествий

## Конфигураця проекта

### Добавление необходимых файлов

Клонируем проект с репозитория.

В корневой папке создать файл `.env`.
Добавить в него слудующую инфрмацию:
```
DB_HOST=Адрес_БД
DB_PORT=Порт_БД
DB_USER=Пользователь_БД
DB_PASSWORD=Пароль_БД
DB_NAME=Название_БД
```

В папке `client` создать файл `env-config.json`.
Добавить в него следующую информцию:
```json
{
    "protocol": "Протокол_соединения_с_сервером",
    "serverHost": "Адрес_сервера",
    "serverPort": "Порт_сервера",
    "serverLocation": "/api",
    "timeout": 600000,
    "apiOsm": "API OSM",
    "apiGh": "API GH"
}
```

## Запуск

Установка `docker`:

1. Set up Docker's `apt` repository
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

2. Install the `Docker` packages
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Запуск проекта
```bash
docker compose up --build
```

---
## Архив


## Серверная часть

### Установка зависимостей и запуск

Создание виртуального окружения
```bash
pip install -r requirements.txt
```

Установка зависимостей из файла `requirements.txt`
```bash
python -m venv venv
```

Запуск виртуального окружения (`Windows`) (1 вариант)
```bash
.\venv\Scripts\activate.bat
```

Запуск виртуального окружения (`Windows`) (2 вариант)
```bash
.\venv\Scripts\Activate.ps1
```

Запуск виртуального окружения (`Linux`)
```bash
source venv/bin/activate
```

Запуск локального сервера из папки `server`
```bash
uvicorn main:app --reload
```

### Внешние ресурсы

1. База гостиниц Москвы [101 Hotels](https://m.101hotels.com/main/cities/moskva/alphabetically#B)

---

## Веб-клиент

### Установка зависимостей и запуск

Предварительно необходимо установить:
1. [NodeJS](https://nodejs.org/en)
2. [Nmp](https://www.npmjs.com/) (Устанавливается с `NodeJS`)

Находясь в корневой папке проекта переходим в папку веб-клиента
```bash
cd ./client
```

Устанавливаем зависимости:
```bash
npm install
```

Запуск проекта в режиме разработки (исползуется `Vite`):
```bash
npm run dev
```

Сборка приложения:
```bash
npm build
```

### Внешние ресурсы

1. Библиотека компонентов [Material uI](https://mui.com/material-ui/)

Установка
```bash
npm install @mui/material @emotion/react @emotion/styled
```

2. Шрифт [Roboto](https://fonts.google.com/specimen/Roboto)

Установка
```bash
npm install @fontsource/roboto
```

3. Карты [OpenRoute Service](https://openrouteservice.org/)




### Запуск
* Команда для запуска скрипта вычисления матрицы расстояний
```bash
python compute_distance_matrix.py -i coords_wineries.csv -o crimea_matrix.csv -p params.yaml -t matrix
```

`-i/--input` - путь к файлу с координатами объектов
`-o/--output` - путь к файлу, куда сохранить результат (направления или матрица расстояний)
`-p/--params` - путь к файлу с параметрами для доступа к ГИС-сервису
`-t/--target` - целевое название (directions или matrix)

* Команда для запуска скрипта оптимизации маршрута
```bash
python optimize_route.py -i crimea_matrix.csv -t distance -o route.json -s 1 -e 1
```
`-i/--input` - путь к csv-файлу с матрицей расстояний
`-o/--ouput` - путь к json-файлу для сохранения результатов оптимизации
`-t/--target` - имя оптимизационной цели из матрицы расстояний (расстояние или продолжительность)
`-s/--start` - начальная точка маршрута; будет выбрана точка, соответствующая оптимальной, если не указана
`-e/--end` - конечная точка маршрута; будет выбрана точка, соответствующая оптимальной, если не указана

Последовательность действий:
1. Запуск файла data_collection/create_tables.py, который создает пустые таблицы базы данных
2. Запуск файла data_collection/get_hotels.py, который собирает данные о гостиницах и заносит их в базу данных
3. Запуск файла data_collection/get_poi.py, который собирает данные о категориях интересующих мест и заносит их в базу данных

4. Запуск heat_map.ipynb, который создаст файл csv/all_points.csv с координатами точек из бд и "тепловую" карту

5. Запуск proxy.py, который создаст файл matrix.csv, содержащий матрицу времени и расстояний всех точек
6. Запуск finding_ways/start.py, который найдет лучшие варианты гостиниц