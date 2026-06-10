# Лабораторная работа №3

# Kubernetes: состояние и хранение данных (Stateful Applications)

## Метаданные студента

| Параметр        | Значение                                        |
| --------------- | ----------------------------------------------- |
| ФИО             | Муратов Дмитрий Владимирович                    |
| Группа          | AC-576                                          |
| Student ID      | 220239                                          |
| Email           | [zas57612@g.bstu.by](mailto:zas57612@g.bstu.by) |
| GitHub Username | ohdima                                          |
| Вариант         | 13                                              |

---

## Цель работы

Изучить развертывание stateful-приложений в Kubernetes с использованием StatefulSet, PersistentVolumeClaim, Headless Service, а также реализовать механизмы резервного копирования и восстановления данных.

---

## Исходные данные варианта

| Параметр        | Значение   |
| --------------- | ---------- |
| База данных     | PostgreSQL |
| PVC             | 5Gi        |
| StorageClass    | default    |
| Backup Schedule | 30 1 * * * |

---

## Архитектура решения

В ходе выполнения лабораторной работы были созданы следующие Kubernetes-ресурсы:

* Namespace
* Secret
* Headless Service
* StatefulSet
* PersistentVolumeClaim для хранения данных PostgreSQL
* PersistentVolumeClaim для хранения резервных копий
* CronJob для автоматического резервного копирования
* Job для восстановления данных

Структура проекта:

```text
lab03/
│
├── namespace.yaml
├── secret.yaml
├── service.yaml
├── statefulset.yaml
├── backup-pvc.yaml
├── cronjob-backup.yaml
├── restore-job.yaml
└── README.md
```

---

## Создание Namespace

Создан отдельный namespace:

```text
state-ac-576-220239-v13
```

Команда:

```bash
kubectl apply -f namespace.yaml
```

Результат:

```text
namespace/state-ac-576-220239-v13 created
```

---

## Создание Secret

Для хранения учетных данных PostgreSQL создан Secret:

```yaml
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

Команда:

```bash
kubectl apply -f secret.yaml
```

Результат:

```text
secret/postgres-secret created
```

---

## Создание Headless Service

Создан Headless Service:

```yaml
clusterIP: None
```

Назначение сервиса:

* обеспечение стабильного DNS-имени Pod;
* поддержка работы StatefulSet;
* обеспечение доступа к PostgreSQL внутри кластера.

Результат:

```text
service/db-ac-576-220239-v13 created
```

---

## Развертывание StatefulSet

Развернут StatefulSet PostgreSQL со следующими параметрами:

| Параметр     | Значение    |
| ------------ | ----------- |
| Image        | postgres:16 |
| Replicas     | 1           |
| Storage      | 5Gi         |
| StorageClass | standard    |

Результат проверки:

```text
NAME                     READY   STATUS
db-ac-576-220239-v13-0   1/1     Running
```

---

## Проверка PVC

После запуска StatefulSet автоматически создан PersistentVolumeClaim.

Результат:

```text
NAME                                  STATUS   CAPACITY
postgres-data-db-ac-576-220239-v13-0 Bound    5Gi
```

PVC успешно привязан к Persistent Volume и используется PostgreSQL для хранения данных.

---

## Создание тестовых данных

В PostgreSQL создана тестовая таблица:

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100)
);
```

Добавлена запись:

```sql
INSERT INTO students(fullname)
VALUES ('Dmitry Muratov');
```

Результат проверки:

```text
 id | fullname
----+----------------
  1 | Dmitry Muratov
```

---

## Проверка сохранности данных

Для проверки устойчивости StatefulSet был удален Pod PostgreSQL:

```bash
kubectl delete pod db-ac-576-220239-v13-0
```

После удаления Kubernetes автоматически создал новый экземпляр Pod.

Результат:

```text
NAME                     READY   STATUS
db-ac-576-220239-v13-0   1/1     Running
```

Повторная проверка таблицы показала сохранность данных:

```text
 id | fullname
----+----------------
  1 | Dmitry Muratov
```

Таким образом подтверждена корректная работа StatefulSet и PersistentVolumeClaim.

---

## Создание PVC для резервных копий

Создан отдельный PVC для хранения резервных копий базы данных.

Результат:

```text
NAME                     STATUS   CAPACITY
backup-ac-576-220239-v13 Bound    5Gi
```

---

## Настройка CronJob

Создан CronJob для автоматического резервного копирования PostgreSQL.

Расписание:

```cron
30 1 * * *
```

Результат:

```text
NAME                      SCHEDULE
backup-ac-576-220239-v13  30 1 * * *
```

---

## Проверка резервного копирования

Для тестирования был создан Job на основе CronJob.

Результат выполнения:

```text
NAME         STATUS
backup-test  Complete
```

Логи выполнения:

```text
Backup completed
```

Резервная копия успешно сохранена в выделенном PVC.

---

## Проверка восстановления данных

Для проверки восстановления были удалены данные из таблицы:

```sql
DELETE FROM students;
```

Проверка показала отсутствие записей:

```text
(0 rows)
```

После этого был выполнен Job восстановления:

```text
restore-ac-576-220239-v13
Complete
```

Проверка данных после восстановления:

```text
 id | fullname
----+----------------
  1 | Dmitry Muratov
```

Данные успешно восстановлены из резервной копии.

---

## Вывод

В ходе выполнения лабораторной работы были изучены механизмы хранения состояния приложений в Kubernetes.

Были успешно реализованы:

* StatefulSet PostgreSQL;
* PersistentVolumeClaim для хранения данных;
* Headless Service;
* Secret для хранения конфиденциальных данных;
* CronJob для автоматического резервного копирования;
* Job для восстановления данных;
* проверка сохранности данных после удаления Pod.

Полученные результаты подтверждают корректную работу механизмов хранения данных, резервного копирования и восстановления в Kubernetes для stateful-приложений.
