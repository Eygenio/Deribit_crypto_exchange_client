# 📈 Crypto Index Price API — FastAPI + Celery + PostgreSQL

Backend-сервис для сбора и хранения индексных цен криптовалют BTC и ETH с биржи Deribit
и предоставления публичного API для их анализа.

Проект реализует:
- периодический сбор цен с биржи
- хранение истории в PostgreSQL
- REST API для получения данных

---

## 🚀 Возможности

- ⏱️ Автоматический сбор цен BTC_USD и ETH_USD каждую минуту
- 🗄 Хранение истории цен
- 📊 Получение:
  - последней цены
  - всей истории
  - цен за выбранный период
- 🐇 Celery + RabbitMQ
- 🐳 Docker + docker-compose
- ⚡ FastAPI + async SQLAlchemy

---

## 🏗 Архитектура

Архитектура построена по принципу:
Routing → Service → Repository
  ↓
Deribit Client

```
app/
 ├── src/
 │    ├── clients
 │    │    └── deribit.py
 │    ├── config/
 │    │    ├── base.py
 │    │    └── logging_config.py
 │    ├── db
 │    │    └── db.py
 │    ├── models/
 │    │    ├── __init__.py
 │    │    ├── base.py
 │    │    └── index_price.py
 │    ├── repositories/
 │    │    ├── base.py
 │    │    └── index_price.py
 │    ├── routing/
 │    │    └── index_price.py
 │    ├── schemas/
 │    │    └── index_price.py
 │    ├── services/
 │    │    └── index_price.py
 │    ├── tasks/
 │    │    └── deribit.py
 │    ├── app.py
 │    └── celery_app.py
 ├── tests/
 │    ├── conftest.py
 │    ├── test_client.py
 │    └── test_index_price.py
 ├── .env
 ├── docker-compose.yml
 ├── Dockerfile
 ├── pytest.ini
 ├── README.md
 └── requirements.txt
```

---

## ⚙️ Стек

- FastAPI
- Celery 5
- RabbitMQ
- PostgreSQL
- aiohttp
- SQLAlchemy 2 (async)
- Docker + docker-compose
- Pytest

---

# 🚀 Запуск проекта (локально)

## 1. Клонировать репозиторий

```bash
git clone https://github.com/Eygenio/Deribit_crypto_exchange_client
```

## 2. Создать `.env` или скопируйте содержимое `.env.template` в `.env`

```
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=database
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=rpc://
RABBIT_USER=guest
RABBIT_PASSWORD=guest
```

## 3. 🐳 Сборка через Docker

```bash
docker-compose build
```

## 4. 🐳 Запуск через Docker

```bash
docker-compose up -d
```

## 🔗 Доступ к сервису

```bash
http://localhost::8080/ 
```

## 🔗 Доступ к документации

```bash
http://localhost::8080/docs/
```

---

## 📡 API

### Получить последнюю цену
```bash
GET /api/price/last?ticker=btc_usd
```

### Получить всю историю
```bash
GET /api/prices?ticker=btc_usd&page=1
```
### Получить цены за период
```bash
GET /api/price/by-date?ticker=btc_usd&from_ts=1700000000&to_ts=1700100000&page=1
```

---

## 🧠 Design decisions
Почему Celery

Deribit API нужно опрашивать регулярно — Celery Beat позволяет надёжно запускать задачи по расписанию и масштабировать сбор данных.

Почему aiohttp

aiohttp обеспечивает асинхронные HTTP-запросы без блокировки event loop FastAPI и Celery.

Почему Repository Pattern

Он отделяет бизнес-логику от SQL и позволяет:

легко писать тесты

менять БД

переиспользовать сервисы

Почему timestamp в UNIX

UNIX timestamp:

легко сравнивается

легко фильтруется

быстро индексируется

Почему pagination

История цен быстро растёт → API не должен отдавать тысячи строк за раз.

---

## 🧪 Тестирование
```bash
pytest
```
### 🐳 Запуск тестов в Docker
```bash
docker-compose exec app pytest -x
```

---