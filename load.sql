-- pgres config:
create test_user with encrypted password 'Ab@123';
create database test_docker owner test_user;
