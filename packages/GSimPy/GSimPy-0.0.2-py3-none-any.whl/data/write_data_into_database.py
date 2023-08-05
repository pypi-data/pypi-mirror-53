"""
.. note::
    This module provides methods to transfer data from TXT file into database

"""
import sqlite3
import json
from data.connect_database import *
from function.get_datainfo import *


def write_item_info_into_database(database_name, table_name, txt_file_path):
    """
        Transfer item-element data from txt file to database.
        Every line in txt file represents a item-element association.
        The first and the last field of each line represent item_id, element_id respectively.
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to store item-element data
    :param txt_file_path: string
            The path of item-element association txt file.
    :return:
    """
    f = open(txt_file_path, 'r+')
    linelist = f.readlines()

    item_element_dt = {}

    for line in linelist:
        line = line.strip('\n')

        line = line.split(' ')
        item_element_dt.setdefault('{0}'.format(line[0]), []).append(line[1])
        # 将字典写入json文件中
        # json_str = json.dumps(item_element_dt, indent=4)
        # with open('../data/{0}_dt.json'.format(table_name), 'w') as f:
        #     f.write(json_str)

    # 链接数据库,sql语句创建数据库表item

    conn = connect_database(database_name)
    c = conn.cursor()
    sql = "create table {0} (ITEM_ID VARCHAR(50) PRIMARY KEY, ELEMENT_LIST VARCHAR(255), " \
          "ELEMENT_NUM INT(10))".format(table_name)

    c.execute(sql)

    for item in item_element_dt:
        infolist = item_element_dt[item]
        str = ','.join(infolist)  # 用","连接元素，构建成新的字符串
        sql = "insert into {0}(ITEM_ID,ELEMENT_NUM,ELEMENT_LIST) values('%s',%d,'%s')".format(table_name) \
              % (item, len(item_element_dt[item]), str)
        c.execute(sql)
        conn.commit()
    conn.close()


# write_item_info_into_database('sample', 'item', '../data/item.txt')


def write_group_info_into_database(database_name, table_name, txt_file_path):
    """
        Transfer group-item-element data from txt file to database.
        Every line in txt file represents a item-element association.
        The first and the last field of each line represent item_id, element_id respectively.
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to store item-element data
    :param txt_file_path: string
            The path of item-element association txt file.
    :return:

    """

    f = open(txt_file_path, 'r+')
    linelist = f.readlines()

    group_item_dt = {}

    for line in linelist:
        line = line.strip('\n')

        line = line.split(' ')
        group_item_dt.setdefault('{0}'.format(line[0]), []).append(line[1])
        # 将字典写入json文件中
        # json_str = json.dumps(item_element_dt, indent=4)
        # with open('../data/{0}_dt.json'.format(table_name), 'w') as f:
        #     f.write(json_str)

    # 链接数据库 创建group表
    conn = connect_database(database_name)
    c = conn.cursor()
    sql = "create table [{0}] (GROUP_ID VARCHAR(50) PRIMARY KEY, ITEM_LIST VARCHAR(255), " \
          "ITEM_NUM INT(10),ELEMENT_LIST VARCHAR(255),ELEMENT_NUM INT(10))".format(table_name)
    c.execute(sql)

    for group in group_item_dt:
        group_element = []
        item_list = group_item_dt[group]
        item_str = ','.join(item_list)
        for item in item_list:
            # print(item)
            item_info = get_item_info(database_name, 'item', item)

            element_list = item_info[1]
            element_list = element_list.split(',')
            # print(element_list)
            for element in element_list:
                if element not in group_element:
                    group_element.append(element)
        element_str = ','.join(group_element)

        sql = "insert into [{0}] (GROUP_ID,ELEMENT_NUM,ELEMENT_LIST,ITEM_LIST,ITEM_NUM) values('%s',%d,'%s','%s',%d)".format(table_name) \
              % (group, len(group_element), element_str, item_str, len(item_list))
        c.execute(sql)
        conn.commit()
    conn.close()


# write_group_info_into_database('sample', 'group', '../data/group.txt')