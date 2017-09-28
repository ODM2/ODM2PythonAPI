MySql Notes:
=========
On Linux, you are required to use { lower_case_table_names=1 }. It is suggested that databases should use this setting.

Connection String
=================

Create DB
=========

Populate with CV
===============


Linux Troubleshooting Notes
===========================
On Linux, you are required to use { lower_case_table_names=1 }.
to see if this is set type:
mysql --verbose -e "show variables like 'lower%';" --user=root
--------------
show variables like 'lower%'
--------------
+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| lower_case_file_system | OFF   |
| lower_case_table_names | 1     |
+------------------------+-------+

If not you can install this line in $HOME/.my.cnf, /etc/my.cnf, or /etc/mysql/my.cnf

[mysqld]
lower-case-table-names = 1

to see what files are being used by mysql:
> strace mysql 2>&1 | grep cnf

stat("/etc/my.cnf", 0x7ffef7c8dca0)     = -1 ENOENT (No such file or directory)
stat("/etc/mysql/my.cnf", {st_mode=S_IFREG|0644, st_size=5232, ...}) = 0
open("/etc/mysql/my.cnf", O_RDONLY|O_CLOEXEC) = 3
stat("/etc/mysql/conf.d/mariadb.cnf", {st_mode=S_IFREG|0644, st_size=435, ...}) = 0
open("/etc/mysql/conf.d/mariadb.cnf", O_RDONLY|O_CLOEXEC) = 4
stat("/etc/mysql/conf.d/mysqld_safe_syslog.cnf", {st_mode=S_IFREG|0644, st_size=36, ...}) = 0
open("/etc/mysql/conf.d/mysqld_safe_syslog.cnf", O_RDONLY|O_CLOEXEC) = 4
stat("/etc/mysql/conf.d/tokudb.cnf", {st_mode=S_IFREG|0644, st_size=285, ...}) = 0
open("/etc/mysql/conf.d/tokudb.cnf", O_RDONLY|O_CLOEXEC) = 4
stat("/home/travis/.my.cnf", 0x7ffef7c8dca0) = -1 ENOENT (No such file or directory)
