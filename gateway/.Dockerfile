FROM python:3.10-slim
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]