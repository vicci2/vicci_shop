#!/bin/bash
# su -l postgres -c /usr/pgsql-11/bin/initdb
# su -l postgres -c "/usr/pgsql-11/bin/pg_ctl -D /var/lib/pgsql/11/data -l /tmp/pg_logfile start"
# create user custom_test with encrypted password 'vicciSQL';
# create database test_db owner custom_test;
#!/bin/bash
su -l postgres -c /usr/pgsql-11/bin/initdb
su -l postgres -c "/usr/pgsql-11/bin/pg_ctl -D /var/lib/pgsql/11/data -l /tmp/pg_logfile start"
su -l postgres -c "psql -U postgres -h localhost -d postgres -f /load.sql"
# docker run --name some-postgres -p 5432:5432 -e POSTGRES_USER=userpostgres -e POSTGRES_PASSWORD=Ab@123 -e POSTGRS_DB=test_docker -d postgres