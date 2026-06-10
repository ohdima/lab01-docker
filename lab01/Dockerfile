# Dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim AS deps

WORKDIR /install

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim AS runtime

LABEL org.bstu.student.fullname="Муратов Дмитрий Владимирович" \
      org.bstu.student.id="220239" \
      org.bstu.group="AC-576" \
      org.bstu.variant="13" \
      org.bstu.course="RSIOT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    STU_ID=220239 \
    STU_GROUP=AC-576 \
    STU_VARIANT=13

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && groupadd --gid 10001 appgroup \
    && useradd --uid 10001 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser \
    && rm -rf /var/lib/apt/lists/*

COPY --from=deps /install /usr/local
COPY app.py .

USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["python"]
CMD ["app.py"]