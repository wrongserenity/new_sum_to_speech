FROM postgres:14.1-alpine
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql
USER root
RUN chown postgres:postgres /docker-entrypoint-initdb.d/init.sql