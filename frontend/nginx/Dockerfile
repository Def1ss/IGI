FROM nginx:1.17.4-alpine

RUN apk add --no-cache bash

COPY wait.sh /wait.sh
COPY default.dev.conf /etc/nginx/conf.d/default.conf

RUN chmod +x /wait.sh

# Исправленная команда: передаем хост и порт правильно
CMD ["/wait.sh", "web-front:3000", "--", "nginx", "-g", "daemon off;"]