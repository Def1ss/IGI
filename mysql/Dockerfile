FROM mysql:8.4

# Копируем конфигурацию, если есть
COPY my.cnf /etc/mysql/conf.d/my.cnf


# Явно указываем права
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/