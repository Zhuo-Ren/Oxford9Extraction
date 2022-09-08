# -*- coding: utf-8 -*-
from dbsql_sqlite import DbSql
from storage_api import StorageApi


class StorageSqlite(StorageApi):
    @staticmethod
    def open(pth):
        """
        链接指定数据库
        :param pth: 数据库路径
        :type pth: str
        """
        # 链接数据库
        DbSql.connectDataBase(pth)
        # 建表
        DbSql.ensureTable(
            tableName=StorageApi.tableName,
            tableStructureInDict=StorageApi.tableStructureInDict,
            updateStrategy='continue'
        )

    @staticmethod
    def close():
        DbSql.disconnectDataBase()

    @staticmethod
    def get_entry(spelling):
        selected_row = DbSql.selectRow(StorageApi.tableName, {'Spelling': spelling})
        if selected_row == []:
            return {}
        else:
            selected_row = selected_row[0]
            return {
                "Spelling": selected_row[0],
                "Oxford9": selected_row[1],
                "Oxford9Rest": selected_row[2],
                "MyDict": selected_row[3]
            }

    @staticmethod
    def update_entry(spelling, update_dict):
        DbSql.updateRow(
            tableName=StorageApi.tableName,
            selectDict={'Spelling': spelling},
            setDict=update_dict
        )
        return True

    @staticmethod
    def create_entry(spelling, entry_dict):
        entry_dict["spelling"] = spelling
        DbSql.insertRow(StorageApi.tableName, entry_dict)
        return True
