FROM mysql

ENV MYSQL_DATABASE=db \
    MYSQL_ROOT_PASSWORD=example
    # ^ definitelly not the best way to store secrets, but I'll leave it for simplicity

ADD db/schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306
