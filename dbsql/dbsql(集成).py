# -*- coding: utf-8 -*-

# 关系型数据库
import sqlite3  # 引入sqlite3来使用sqlite
import pymysql  # 引入pymysql来使用mysql
import redis  # 引入redis来使用nosql数据库
# 非关系型数据库 有关nosql的相关知识，可参考https://www.cnblogs.com/dachenzi/articles/7899774.html
import pymssql  # 引用pymssql来使用SQLServer数据库
import cx_Oracle  # 引用cx_Oracle来使用Oracle
#
import re
import os  #用于存储操作
import os.path  #用于存储操作

dbConnect = None
dbCursor = None


###############################################################################
###########################连接数据库############################################
###############################################################################
def connectSQLite(dbName):
    global dbConnect
    global dbCursor
    # dbName用来指明要连接到的数据库名字
    # 创建连接
    dbConnect = sqlite3.connect(dbName)
    # 创建游标
    dbCursor = dbConnect.cursor()
    print('建立sqlite数据库连接')


def connectMYSQL(dbName):
    global dbConnect
    global dbCursor
    # dbName用来指明要连接到的数据库名字
    # 创建连接
    dbConnect = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db=dbName,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    # 创建游标
    dbCursor = dbConnect.cursor()
    print('建立mysql数据库连接')


def connectnoSQL(dbName):
    global dbConnect
    # dbName用来指明要连接到的数据库名字
    # 创建连接
    dbConnect = redis.Redis(host="192.168.6.137", port=6379, db=dbName)
    print('建立nosql数据库连接')


def connectSQLServer(dbName):
    global dbConnect
    global dbCursor
    # dbName用来指明要连接到的数据库名字
    # 创建连接
    dbConnect = pymssql.connect(database=dbName)
    # 创建游标
    dbCursor = dbConnect.cursor()
    print('建立SQL Server数据库')


def connectOracle(dbName):
    global dbConnect
    global dbCursor
    # dbName用来指明要连接到的数据库名字
    # 创建连接
    dbConnect = cx_Oracle.connect(dbName)
    # 创建游标
    dbCursor = dbConnect.cursor()
    print("建立Oracle数据库")


def connect(dbType, dbName):
    # 将连接各类型数据库进行整合
    # dbName用来指明要连接到的数据库名字，dbType用来指明要连接的数据库类型
    if dbType == 'sqlite':
        connectSQLite(dbName)
    elif dbType == 'mysql':
        connectMYSQL(dbName)
    elif dbType == 'nosql':
        connectnoSQL(dbName)
    elif dbType == 'sqlserver':
        connectSQLServer(dbName)
    elif dbType == 'oracle':
        connectOracle(dbName)
    else:
        print("no such database")


###############################################################################
###########################释放数据库############################################
###############################################################################
def disconnectSQLite():
    global dbConnect
    global dbCursor
    if dbCursor is not None:
        # 关闭游标
        dbCursor.close()
        # 提交事务
        dbConnect.commit()
        # 关闭连接
        dbConnect.close()
        # 日志
        print('释放sqlite数据库连接')


def disconnectMySQL():
    global dbConnect
    global dbCursor
    if dbCursor is not None:
        # 关闭游标
        dbCursor.close()
        # 提交事务和关闭连接
        dbConnect.commit()
        dbConnect.close()
        # 日志
        print('释放mysql数据库连接')


def disconnectNoSQL():
    # 未找到相应代码
    print('释放nosql数据库')


def disconnectSQLServer():
    if dbCursor is not None:
        # 提交事务
        dbConnect.commit()
        # 关闭游标与关闭连接
        dbCursor.close()
        dbConnect.close()
        # 日志
        print('释放SQL Server数据库连接')


def disconnectOracle():
    if dbCursor is not None:
        # 提交事务
        dbConnect.commit()
        # 关闭游标与关闭连接
        dbCursor.close()
        dbConnect.close()
        # 日志
        print('释放Oracle数据库')


def disconnect(dbType):
    # 该函数用于将各类型数据库的关闭操作进行汇总
    # 其中dbType用来指明要连接的数据库类型
    if dbType == 'sqlite':
        disconnectSQLite()
    elif dbType == 'mysql':
        disconnectMySQL()
    elif dbType == 'nosql':
        disconnectNoSQL()
    elif dbType == 'sqlserver':
        disconnectSQLServer()
    elif dbType == 'oracle':
        disconnectOracle()
    else:
        # 日志
        print('dbType error')


#####################################################################################
##########################执行语句#####################################################
#####################################################################################
######执行语句可以进行插入，删除，更新，查询功能，视具体command而定#############################
def executeCommand(dbType, command):
    global dbCursor
    # dbType用来表明数据库的类型，command用来表明需要执行的数据库语句
    # 注意：command会因数据库类型及实现不同的功能而有所差异
    try:
        # 对关系型数据库进行操作
        if dbType == 'sqlite' or dbType == 'sqlserver' or dbType == 'mysql' or dbType == 'oracle':
            dbCursor.execute(command)
            dbCursor.fetchall()
        elif dbType == 'nosql':
        # 对非关系型数据库进行操作，使用管道进行数据处理
            pipline = dbConnect.pipline(transaction=True)
            pipline.set(command)
            pipline.execute()
    except Exception as e:
        print('如下语句执行出错：', command)
        print('错误为：', e)


###############################################################################
##########################建表#################################################
###############################################################################
def establishTables(dbType, tableName, field):
    global dbCursor
    # 根据不同的关系型数据库，使用不同的数据库语言进行建表
    # 其中，dbType用来指明数据库类型，tableName用来指明数据表名称，field用于指明数据表中所需要创建的字段
    # 注意：field应该详细指出各个字段的名称，类型，是否可为空，是否为主键等信息，具体字段将会因数据库语言不同而有所差异
    if dbType == 'sqlite':
        sql_create = 'CREATE TABLE %s (%s)' % (tableName, field)
        print(sql_create)
        dbCursor.execute(sql_create)
    elif dbType == 'mysql' or dbType == 'sqlserver' or dbType == 'oracle':
        sql_create = 'CREATE TABLE %s (%s)' % (tableName, field)
        dbCursor.execute(sql_create)
    else:
        print("非关系(NoSQL)数据库一般不会对表的结构进行严格的定义，一般使用分区键及键值来检索值、列集或者半结构化数据")


###############################################################################
##########################删表#################################################
###############################################################################
def deleteTables(dbType, tableName):
    global dbCursor
    # 根据不同的关系型数据库，使用不同的关系型数据库语言来删除指定表
    # dbType代表数据库类型，tableName代表数据库中某数据表名
    if dbType == 'sqlite':
        sql_delete = 'DROP TABLE %s', tableName
        dbCursor.execute(sql_delete)
    elif dbType == 'mysql':
        sql_delete = "drop table if exists %s", tableName
        dbCursor.execute(sql_delete)
    elif dbType == 'sqlserver' or dbType == 'oracle':
        sql_delete = 'drop table' + tableName
        dbCursor.execute(sql_delete)
    else:
        print('非关系(NoSQL)数据库一般不会对表的结构进行严格的定义，一般使用分区键及键值来检索值、列集或者半结构化数据')


###############################################################################
##########################查询某表是否存在#######################################
###############################################################################
def isExists(dbType, tableName):
    global dbCursor
    # 根据不同的关系型数据库，使用不同的关系型数据库语言来查找指定表是否存在
    # dbType代表数据库类型，tableName代表数据库中某数据表名
    if dbType == 'mysql':
        dbCursor.execute('show tables')
        tables = [dbCursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if tableName in table_list:
            return True
        else:
            return False
    elif dbType == 'sqlite':
        sql_exists = 'select * from sqlite_master where name=%s', tableName
        result = dbCursor.execute(sql_exists)
        if result.getInt(0) == 0 :
            return False
        else:
            return True
    elif dbType == 'sqlserver':
        # 该语句可能存在问题
        sql_exists = 'SELECT * FROM sysobjects WHERE name=%s' % tableName
        result = dbCursor.execute(sql_exists)
        if result.getInt(0) == 0:
            return False
        else:
            return True
        print()
    elif dbType == 'oracle':
        sql_exits = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s', tableName
        result = dbCursor.execute(sql_exits)
        if result.fetchone()[0] == 1:
            return True
        else:
            return False
    else:
        print('非关系(NoSQL)数据库一般不会对表的结构进行严格的定义，一般使用分区键及键值来检索值、列集或者半结构化数据')


######################################################################################
############################查询某数据库中的所有表########################################
######################################################################################
def searchTables(dbType):
    # 根据数据库类型，查询数据库中所有表
    # 注意：该函数存在缺陷，本函数默认查询的是数据库中的所有表
    # 若想单独查询系统表或某一用户的用户表，则需对sql_search语句进行修改（即from后的字段）
    # 将查询到的结构进行保存（使用列表）
    global dbCursor
    result = []
    if dbType == 'sqlite':
        sql_search = "select name from sqlite_master where type='table' order by name"
        dbCursor.execute(sql_search)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    elif dbType == 'mysql':
        sql_search = 'SHOW TABLES'
        dbCursor.execute(sql_search)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    elif dbType == 'sqlserver':
        sql_search = 'SELECT * FROM sysobjects'
        dbCursor.execute(sql_search)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    elif dbType == 'oracle':
        sql_search = 'SELECT * FROM ALL_TABLES'
        dbCursor.execute(sql_search)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    else:
        print('非关系(NoSQL)数据库一般不会对表的结构进行严格的定义，一般使用分区键及键值来检索值、列集或者半结构化数据')


######################################################################################
##########################查询表结构####################################################
######################################################################################
def queryStructure(dbType, tableName):
    global dbCursor
    # 根据数据库类型及表名查询某一表中的所有字段信息
    # 注意：本函数默认是从所有数据表中查询某一表信息，如若缩小范围（即从系统表或某一用户的用户表进行搜索），需更改sql_query语句
    # 一般更改from后字段即可
    # 将返回结果进行保存
    result = []
    if dbType == 'sqlite':
        sql_query = 'PRAGMA table_info(%s)' % tableName
        dbCursor.execute(sql_query)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    elif dbType == 'mysql':
        sql_query = 'select * from %s' % tableName
        dbCursor.execute(sql_query)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    elif dbType == 'sqlserver':
        sql_query = 'SELECT  * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s ORDER BY ORDINAL_POSITION' % tableName
        dbCursor.execute(sql_query)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    elif dbType == 'oracle':
        sql_query = 'select * from all_tab_columns where Table_Name=%s' % tableName
        dbCursor.execute(sql_query)
        allData = dbCursor.fetchall()
        for ad in allData:
            result.append(ad)
        return result
    else:
        print('非关系(NoSQL)数据库一般不会对表的结构进行严格的定义，一般使用分区键及键值来检索值、列集或者半结构化数据')
