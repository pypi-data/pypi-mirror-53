from data.connect_database import *

"""
.. note::
    This module provides methods to maintain database

"""


def update_data(database_name, table_name):
    """
        This function is used to update information in database

    :param database_name: string
           The database to connect to
    :param table_name: string
           The database table being updated
    :return:
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    if table_name is 'item':
        update_info = input("please enter update information(ITEM_ID,ELEMENT_LIST,ELEMENT_NUM),split by ' ':")
        update_info = update_info.split(' ')
        item_id = update_info[0]
        element_list = update_info[1]
        element_num = update_info[2]

        sql = (
            "update [{0}] set ELEMENT_LIST ='{1}',ELEMENT_NUM = '{2}' where ITEM_ID = {3}".format(table_name,
                                                                                                  element_list,
                                                                                                  element_num,
                                                                                                  item_id))

        c.execute(sql)
        conn.commit()

    elif table_name is 'group':
        update_info = input("please enter update information(GROUP_ID,ITEM_LIST,ITEM_NUM,ELEMENT_LIST,ELEMENT_NUM)"
                            ",split by ' ':")
        update_info = update_info.split(' ')
        group_id = update_info[0]
        item_list = update_info[1]
        item_num = update_info[2]
        element_list = update_info[3]
        element_num = update_info[4]

        sql = ("update [{0}] set ITEM_LIST ='{1}',ELEMENT_LIST = '{2}',ITEM_NUM = '{3}',ELEMENT_NUM='{4}' "
               "where GROUP_ID = {5}".format(table_name, item_list, element_list, item_num, element_num,group_id))
        c.execute(sql)
        conn.commit()

    else:
        print("no such table exists in '{0}' database".format(database_name))

    conn.close()

    return 0

# update_data('sample','item')

def insert_data(database_name, table_name):
    """
        This function is used to insert data into database
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being inserted
    :return:
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    if table_name is 'item':
        insert_info = input("please enter insert information(ITEM_ID,ELEMENT_LIST,ELEMENT_NUM),split by ' ':")
        insert_info = insert_info.split(' ')
        item_id = insert_info[0]
        element_list = insert_info[1]
        element_num = insert_info[2]

        sql = ("insert into {0} (ITEM_ID,ELEMENT_LIST,ELEMENT_NUM) values ({1},{2},{3})".format
               (table_name, item_id, element_list, element_num))

        c.execute(sql)
        conn.commit()

    elif table_name is 'group':
        insert_info = input("please enter insert information(GROUP_ID,ITEM_LIST,ITEM_NUM,ELEMENT_LIST,ELEMENT_NUM)"
                            ",split by ' ':")
        insert_info = insert_info.split(' ')
        group_id = insert_info[0]
        item_list = insert_info[1]
        item_num = insert_info[2]
        element_list = insert_info[3]
        element_num = insert_info[4]

        sql = ("insert into [{0}] (GROUP_ID,ITEM_LIST,ITEM_NUM,ELEMENT_LIST,ELEMENT_NUM) values ({1},{2},{3},{4},{5})".format
               (table_name, group_id, item_list, item_num, element_list, element_num))
        c.execute(sql)
        conn.commit()

    else:
        print("no such table exists in '{0}' database".format(database_name))

    conn.close()

    return 0


# insert_data('sample', 'item')

def delete_data(database_name, table_name, primary_key, primary_key_content):
    """
        This function is to delete information from database
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being deleted
    :param primary_key: string
            The primary key of the database table
    :param primary_key_content: string
            The specific primary key content to be deleted
    :return:
    """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("delete from '{0}' where {1} = '{2}'".format(table_name, primary_key, primary_key_content))

    c.execute(sql)
    conn.commit()

    conn.close()

    return 0

# delete_data('sample', 'item','ITEM_ID','1')
# delete_data('sample', 'group','group_ID','1')