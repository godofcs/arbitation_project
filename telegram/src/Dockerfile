FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /src
RUN pip install --upgrade pip
RUN ls -l
RUN pip install -r requirements.txt