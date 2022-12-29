FROM python:3
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/
COPY ./entrypointFastApi.sh /entrypointFastApi.sh
RUN chmod +x /entrypointFastApi.sh