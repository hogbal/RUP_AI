FROM mariadb:10.9.3

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=rup_db
ENV MYSQL_USER=rup
ENV MYSQL_PASSWORD=rup

COPY my.cnf /etc/mysql/my.cnf
COPY init.sql /docker-entrypoint-initdb.d

EXPOSE 3306 

CMD ["mysqld"]
