# -*- coding: utf-8 -*-
import re
from storage_sqlite import StorageSqlite as Storage
from config import config

def split_entry_from_html(html_path, db_path):
    """
    1.读取字典html文件（这里就是“原版debug.html”），并以</>为记号分割文件。每一块称为一个block。个别entry对应对个block
    2.从block中分离出词项(entry)的拼写(spelling)和html内容(htmlblock)。
    3.按entry把各htmlblock存储到db_path指定的数据库(这是累加存储，所以多次执行可能产生重复数据)中的Oxford9和Oxford9Rest列。数据库结构参见storage_api.py中的定义。

    :param html_path: 要被拆分的字典html文件的路径。
    :type html_path: str
    :param db_path: 数据存储到哪个数据库
    :type db_path: str
    """
    # 读取字典html文件
    html_file = open(html_path, "r", encoding="UTF-8")
    html = html_file.read()
    html_file.close()

    # 拆分block：split the file based on label </>, get block_list.
    block_list = html.split("</>")
    # the last element of block_list is empty string, del it
    block_list = block_list[:-1]

    # 分block存储
    # parse each block, get the spelling and htmlblock, and save them in entry_dict
    Storage.open(db_path)
    for cur_block in block_list:
        # delete the \n at the start
        if cur_block[0] == "\n":
            cur_block = cur_block[1:]

        # get the spelling and htmlblock
        match = re.match('[\s\S]+?\n', cur_block)
        spelling = match.group()[:-1]
        htmlblock = cur_block[match.regs[0][1]:]

        # 删除<head>标签
        if htmlblock[161:168] == r"</head>":
            htmlblock = htmlblock[168:]

        # 修改资源路径
        htmlblock = htmlblock.replace(r'img src="', r'img src="/static/oxford9/pic/')

        # 存储
        entry = Storage.get_entry(spelling)
        # 如果一个entry对应多个htmlblock，更新它
        if entry != {}:
            print("对应多个html块:", spelling)
            block_raw = entry["Oxford9"]
            Storage.update_entry(spelling, {"Oxford9": block_raw+htmlblock, "Oxford9Rest": block_raw+htmlblock})
        # 如果一个entry对应1个htmlblock，创建它
        else:
            init_info_of_my_dict = "<item><spelling>%s</spelling><pronunciations></pronunciations><meanings></meanings></item>" % spelling
            Storage.create_entry(spelling, {"Oxford9": htmlblock, "Oxford9Rest": htmlblock, "MyDict": init_info_of_my_dict})
    del block_list

    # 关闭数据库
    Storage.close()


split_entry_from_html(html_path="raw/原版debug.html", db_path=config["db_path"])
