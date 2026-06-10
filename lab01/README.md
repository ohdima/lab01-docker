# Лабораторная работа №1. Контейнеризация и Docker

## Метаданные студента

| Параметр        | Значение                                        |
| --------------- | ----------------------------------------------- |
| ФИО             | Муратов Дмитрий Владимирович                    |
| Группа          | AC-576                                          |
| StudentID       | 220239                                          |
| Email           | [zas57612@g.bstu.by](mailto:zas57612@g.bstu.by) |
| GitHub          | ohdima                                          |
| Вариант         | 13                                              |
| Дата выполнения | 13.05.2026                                      |
| Курс            | RSIOT                                           |

---

## Описание проекта

В рамках лабораторной работы разработан HTTP-сервис на Python/Flask и выполнена его контейнеризация с использованием Docker.

Проект включает:

* Flask HTTP-сервис;
* Multi-stage Dockerfile;
* Docker Compose;
* Redis в качестве зависимого сервиса;
* Healthcheck;
* Graceful Shutdown;
* Переменные окружения;
* Пользовательскую сеть Docker;
* Именованный том для хранения данных Redis;
* Запуск контейнера от непривилегированного пользователя.

---

## Используемые технологии

* Python 3.12
* Flask 3.0.3
* Docker
* Docker Compose
* Redis 7 Alpine

---

## Структура проекта

```text
lab01-docker/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── Makefile
└── README.md
```

---

## Переменные окружения

```text
PORT=8080
STU_ID=220239
STU_GROUP=AC-576
STU_VARIANT=13
REDIS_URL=redis://redis:6379/0
```

---

## Сборка Docker-образа

```bash
docker build -t ohdima/lab01:stu-220239-v13 .
```

---

## Запуск контейнера

```bash
docker run --rm -p 8080:8080 ohdima/lab01:stu-220239-v13
```

---

## Запуск через Docker Compose

```bash
docker compose up --build
```

---

## Проверка работы сервиса

Главная страница:

```bash
curl http://localhost:8080
```

Ответ:

```json
{
  "message": "Hello, variant 13"
}
```

Проверка Health Endpoint:

```bash
curl http://localhost:8080/health
```

Ответ:

```json
{
  "status": "ok"
}
```

Проверка Ready Endpoint:

```bash
curl http://localhost:8080/ready
```

Ответ:

```json
{
  "status": "ready"
}
```

---

## Проверка контейнеров

```bash
docker ps
```

Результат:

* app-ac-576-220239-v13
* redis-ac-576-220239-v13

---

## Проверка томов

```bash
docker volume ls
```

Результат:

```text
data-ac-576-220239-v13
```

---

## Проверка сети

```bash
docker network ls
```

Результат:

```text
net-ac-576-220239-v13
```

---

## Проверка размера образа

```bash
docker images
```

Размер образа:

```text
49.8 MB
```

Требование задания (≤150 MB) выполнено.

---

## Проверка непривилегированного пользователя

```bash
docker inspect app-ac-576-220239-v13
```

Результат:

```json
"User": "10001:10001"
```

Контейнер работает от непривилегированного пользователя.

---

## Проверка Graceful Shutdown

Остановка контейнера:

```bash
docker stop --time=30 <container_id>
```

Лог приложения:

```text
Shutting down gracefully
Graceful shutdown completed
```

Требование корректного завершения работы выполнено.

---

## Метаданные Docker

### Docker Image Tag

```text
ohdima/lab01:stu-220239-v13
```

### Volume

```text
data-ac-576-220239-v13
```

### Network

```text
net-ac-576-220239-v13
```

### Slug

```text
ac-576-220239-v13
```

---

## Репозиторий GitHub

https://github.com/ohdima/lab01-docker

---

## Вывод

В ходе выполнения лабораторной работы был разработан и контейнеризирован HTTP-сервис на Flask. Были реализованы multi-stage сборка Docker-образа, healthcheck, graceful shutdown, работа с Docker Compose, Redis, именованными томами и пользовательской сетью. Все требования задания выполнены.
