FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /src
RUN pip install --upgrade pip
RUN pip install -r ./src/telegram/src/requirements.txt