FROM nginx:1.25.2-alpine3.18-slim

COPY conf/nginx.conf /etc/nginx
COPY conf/proxy_params /etc/nginx

COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY conf/upstream.conf /etc/nginx/conf.d/upstream.conf

RUN echo http://dl-2.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
RUN apk --no-cache add bash shadow nano && \
    adduser -u 1000 -G www-data -s /bin/sh -D www-data && \
    usermod -u 1000 www-data

EXPOSE 80

CMD [ "nginx" ]
