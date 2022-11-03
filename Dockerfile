# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /code
RUN pip install pipenv
COPY Pipfile Pipfile.lock ${WORKDIR}
RUN pipenv install --system --deploy
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /code/
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]