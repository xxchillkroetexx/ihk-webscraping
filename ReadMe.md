nothing to see here

SQL-Database

```
create user admin@localhost identified by 'admin'
create database ihk;
grant all privileges on ihk.* to admin@localhost;
flush privileges;
```

```
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| ihk                |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
4 rows in set (0.000 sec)
```