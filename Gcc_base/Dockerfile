#   编译阶段
FROM python:3.8-alpine3.12
# FROM python:3.10-alpine3.13
WORKDIR /app
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk --no-cache add gcc \
&& apk --no-cache add g++ \
&& apk --no-cache add musl-dev \
&& apk --no-cache add libffi-dev \
&& apk --no-cache add openssl-dev \
&& apk --no-cache add python3-dev \
&& apk --no-cache add libxml2-dev \
&& apk --no-cache add libxslt-dev \
&& apk --no-cache add libjpeg-turbo-dev \
&& apk --no-cache add zlib-dev \
&& apk --no-cache add libressl-dev \
&& apk --no-cache add libffi-dev \
&& apk --no-cache add tzdata \
&& cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& apk del tzdata