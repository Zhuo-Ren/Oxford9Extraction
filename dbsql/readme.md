dbsql用于整合各种数据库。
针对每种数据库，各有一个py文件，里边用不同的方式实现同名的类DbSql。
想使用哪个数据库，就import dbsql_dbname as DbSql。
例如想用sqlite数据库，那么就`from dbsql_sqlite import DbSql`。
具体使用方式，请查看对应的test文件，例如`dbsql_sqlite_test.py`。

dbsql(集成).py没啥用，是个笔记demo。
