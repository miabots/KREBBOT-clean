FROM postgres:latest


ARG DB_ENV=$DB_ENV

#COPY entrypoint.sh /entrypoint.sh
#COPY postgresql-$DB_ENV.conf /var/lib/postgresql/data/postgresql.conf
COPY data_$DB_ENV.sql /docker-entrypoint-initdb.d/data.sql

#ENTRYPOINT [ "/entrypoint.sh" ]