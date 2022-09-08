# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class StorageApi(metaclass=ABCMeta):
    tableName = "entryTable"
    tableStructureInDict = {
        "Spelling": {"类型": "文本", "主键否": "主键"},
        "Oxford9": {"类型": "文本", "主键否": "非主键"},  # 原始htmlblock
        "Oxford9Rest": {"类型": "文本", "主键否": "非主键"},  # 原始htmlblock中减去抽取过的信息
        "MyDict": {"类型": "文本", "主键否": "非主键"}  # 抽取得到的信息
    }

    @staticmethod
    @abstractmethod
    def open():
        pass

    @staticmethod
    @abstractmethod
    def close():
        pass

    @staticmethod
    @abstractmethod
    def get_entry(spelling):
        """
        检索一个词项。

        :param spelling: 要索取的词项
        :type spelling: str
        :return:
            如果没有，返回{},
            否则返回{
                "spelling":"apple",
                "Oxford9":"<html>原始html</html>",
                "Oxford9Rest":"<html>剩下的html</html>",
                "MyDict":"<html>抽取得到的信息</html>"
            }
        :rtype: dict
        """
        pass

    @staticmethod
    @abstractmethod
    def update_entry(spelling, update_dict):
        """
        更新一个词项。

        :param spelling: 要更新哪个词项
        :type spelling: str
        :param update_dict: 要更新的内容
        :type update_dict: dict
        :return:
            如果成功，返回True,
            否则返回错误信息
        :rtype: bool | str
        """
        pass

    @staticmethod
    @abstractmethod
    def create_entry(spelling, entry_dict):
        """
        创建一个词项。

        :param spelling: 要创建哪个词项
        :type spelling: str
        :param update_dict: 词项内容
        :type update_dict: dict
        :return:
            如果成功，返回True,
            否则返回错误信息
        :rtype: bool | str
        """
        pass
