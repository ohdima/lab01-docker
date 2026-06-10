# Лабораторная работа №2

# Kubernetes: базовый деплой stateless-приложения

## Метаданные студента

| Параметр             | Значение                                        |
| -------------------- | ----------------------------------------------- |
| ФИО                  | Муратов Дмитрий Владимирович                    |
| Группа               | AC-576                                          |
| Student ID           | 220239                                          |
| Email                | [zas57612@g.bstu.by](mailto:zas57612@g.bstu.by) |
| GitHub               | ohdima                                          |
| Вариант              | 13                                              |
| Курс                 | RSIOT                                           |
| Дата выполнения      | 13.05.2026                                      |
| ОС                   | Windows 10 Enterprise 22H2                      |
| Docker Desktop       | v4.77.0                                         |
| Kubernetes (kubectl) | v1.34.1                                         |
| Minikube             | v1.38.1                                         |

---

# Цель работы

Изучить основы развертывания контейнеризированных приложений в Kubernetes, освоить работу с Deployment, Service, ConfigMap, Ingress, readiness/liveness probes, а также выполнить rolling update без простоя приложения.

---

# Исходные данные

В качестве приложения использован HTTP-сервис на Flask, разработанный в лабораторной работе №1.

Docker Image:

```text
ohdima/lab01:stu-220239-v13
```

---

# Параметры варианта №13

| Параметр       | Значение |
| -------------- | -------- |
| Namespace      | web13    |
| Имя приложения | app13    |
| Реплики        | 2        |
| Порт сервиса   | 8061     |
| Ingress Class  | nginx    |
| CPU Request    | 150m     |
| Memory Request | 128Mi    |

---

# Структура проекта

```text
lab01-docker/
│
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── app.py
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

# Создание Kubernetes-кластера

Для локального тестирования использовался Minikube.

Запуск кластера:

```bash
minikube start --driver=docker
```

Результат:

```text
Done! kubectl is now configured to use "minikube"
```

---

# Включение Ingress Controller

```bash
minikube addons enable ingress
```

Результат:

```text
The 'ingress' addon is enabled
```

---

# Создание Namespace

Файл:

```text
k8s/namespace.yaml
```

Применение:

```bash
kubectl apply -f k8s/namespace.yaml
```

Результат:

```text
namespace/web13 created
```

---

# Создание ConfigMap

Файл:

```text
k8s/configmap.yaml
```

Содержит переменные окружения:

```text
PORT=8080
STU_ID=220239
STU_GROUP=AC-576
STU_VARIANT=13
```

Применение:

```bash
kubectl apply -f k8s/configmap.yaml
```

---

# Создание Deployment

Файл:

```text
k8s/deployment.yaml
```

Основные параметры:

* replicas = 2
* RollingUpdate
* Readiness Probe
* Liveness Probe
* Requests/Limits
* ConfigMap

Стратегия обновления:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

---

# Настройка ресурсов

Requests:

```yaml
requests:
  cpu: 150m
  memory: 128Mi
```

Limits:

```yaml
limits:
  cpu: 300m
  memory: 256Mi
```

---

# Настройка Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
```

---

# Настройка Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /live
    port: 8080
```

Для выполнения лабораторной работы в приложение Flask был добавлен endpoint:

```python
@app.route("/live")
def live():
    return jsonify({
        "status": "live"
    })
```

---

# Создание Service

Файл:

```text
k8s/service.yaml
```

Тип сервиса:

```yaml
type: ClusterIP
```

Порт:

```yaml
port: 8061
targetPort: 8080
```

---

# Создание Ingress

Файл:

```text
k8s/ingress.yaml
```

Параметры:

```yaml
host: app13.local
ingressClassName: nginx
```

После создания получен адрес:

```text
192.168.49.2
```

---

# Развертывание приложения

Применение всех манифестов:

```bash
kubectl apply -f k8s/
```

---

# Проверка состояния ресурсов

Проверка:

```bash
kubectl get all -n web13
```

Результат:

```text
2 Pods Running
1 Service
1 Deployment
1 ReplicaSet
```

Проверка Pod:

```bash
kubectl get pods -n web13
```

Результат:

```text
app13-64d7599c75-956gr   1/1 Running
app13-64d7599c75-kzp6j   1/1 Running
```

---

# Проверка Ingress

Проверка:

```bash
kubectl get ingress -n web13
```

Результат:

```text
app13.local
192.168.49.2
```

---

# Smoke Test

Выполнен Port Forward:

```bash
kubectl port-forward service/app13 8061:8061 -n web13
```

Проверка:

```bash
curl http://localhost:8061
```

Полученный результат:

```json
{
  "message": "Hello, variant 13"
}
```

Статус ответа:

```text
HTTP 200 OK
```

---

# Rolling Update

Для проверки обновления без простоя выполнена смена образа:

```bash
kubectl set image deployment/app13 app13=nginx -n web13
```

Результат:

```text
deployment.apps/app13 image updated
```

После чего выполнен возврат к исходному образу:

```bash
kubectl set image deployment/app13 app13=ohdima/lab01:stu-220239-v13 -n web13
```

Результат:

```text
deployment.apps/app13 image updated
```

Таким образом подтверждена работа стратегии RollingUpdate без остановки сервиса.

---

# Метаданные Kubernetes

Labels:

```text
org.bstu.owner=ohdima
org.bstu.student.slug=ac-576-220239-v13
org.bstu.student.id=220239
org.bstu.group=ac-576
org.bstu.variant=13
org.bstu.course=rsiot
```

Annotation:

```text
org.bstu.student.fullname=Муратов Дмитрий Владимирович
```

---

# Вывод

В ходе выполнения лабораторной работы был успешно развёрнут HTTP-сервис в Kubernetes. Были созданы Namespace, Deployment, Service, ConfigMap и Ingress. Настроены readiness и liveness probes, ресурсные ограничения контейнера, а также выполнено обновление приложения по стратегии RollingUpdate без простоя сервиса. Все требования лабораторной работы выполнены.
