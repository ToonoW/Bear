FROM daocloud.io/library/python:3.6-alpine

MAINTAINER toono

ENV LANG=en_US.UTF-8 \
    TIME_ZONE=Asia/Shanghai

RUN set -ex && \
    echo 'https://mirror.tuna.tsinghua.edu.cn/alpine/v3.8/main' > /etc/apk/repositories && \
    echo 'https://mirror.tuna.tsinghua.edu.cn/alpine/v3.8/community' >> /etc/apk/repositories && \
    apk update && apk add --no-cache supervisor nginx linux-headers build-base gcc musl-dev libxslt-dev mysql-dev

RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir pip==18.0 && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir pipenv uwsgi


# -- Install Application into container:
RUN set -ex && mkdir /app
WORKDIR /app
ADD . /app
RUN mkdir -p /data/nginx
RUN mkdir -p /data/supervisor

ADD nginx.conf /etc/nginx/nginx.conf
ADD app.conf /etc/nginx/sites-available/app.conf
RUN ln -s /etc/nginx/sites-available/app.conf /etc/nginx/conf.d/
RUN rm -f /etc/nginx/conf.d/default.conf


COPY Pipfile Pipfile
#COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system

RUN apk del build-base gcc

# -- Expose
EXPOSE 80
EXPOSE 1080

# -- Entrypoint
ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-n"]
