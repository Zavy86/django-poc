FROM python:3.13-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/src

COPY app/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && useradd --create-home --uid 1000 py \
    && chown -R py:py /app

COPY --chown=py:py app/ /app/
COPY docker/scaffold.py /opt/poc/scaffold.py
COPY docker/templates/ /opt/poc/templates/

USER py

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000
