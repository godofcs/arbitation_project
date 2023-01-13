FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
RUN echo "===> Installing system dependencies..." && \
    BUILD_DEPS="curl unzip" && \
    apt-get update && apt-get install --no-install-recommends -y \
    python3.9-dev libpython3.9-dev python3-pip wget \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0\
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 libpq-dev build-essential \
    $BUILD_DEPS && \
    \
    \
    echo "===> Installing geckodriver and firefox..." && \
    GECKODRIVER_VERSION="v0.32.0" && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    \
    \
    FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP && \
    \
    \
    python3.9 -m pip install selenium==4.7.2 \
    selenium-stealth==1.0.6 \
    pyTelegramBotAPI==4.8.0 \
    sqlalchemy==1.4.42 \
    sqlalchemy_serializer==1.4.1 \
    telebot==0.0.4 \
    psycopg2-binary==2.9.3 \
    pika==1.2.1

RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev && rm -rf /var/lib/apt/lists/*

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY . $APP_HOME/
CMD tail -f /dev/null