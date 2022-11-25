FROM centos:7
COPY startUpScript.sh /
COPY load.sql /
RUN yum install -y epel-release maven wget \
&& yum clean all \
&& yum install -y  https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
&& yum install -y postgresql11-server postgresql11-contrib \
&& chown root /startUpScript.sh \
&& chgrp root /startUpScript.sh \
&& chmod 777 /startUpScript.sh
CMD ["/bin/bash","-c","/startUpScript.sh && tail -f /dev/null"]


# FROM tiangolo/uwsgi-nginx-flask:python3.7
# COPY requirements.txt /tmp/
# RUN pip install -U pip
# RUN pip install -r /tmp/requirements.txt
# RUN apt-get update
# RUN apt-get install -y postgresql
# RUN apt-get install -y sudo
# RUN sudo -i -u postgres
# CMD ["psql", "create database alchemy", "exit", "exit"]
# create postgres user, password and give privileges to db.
# COPY ./app /app
# docker run --name pgadmin-baeldung -p 127.0.0.1:5051:80 -e "PGADMIN_DEFAULT_EMAIL=vicitest@dbase.com" -e "PGADMIN_DEFAULT_PASSWORD=vicciSQL" -d dpage/pgadmin4