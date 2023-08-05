from data.connect_database import *
from function.get_datainfo import *
import numpy as np


def cal_2itemjaccard(database_name, table_name, item1, item2):
    """
        Calculate similarity between two items based on Jaccard Index
    :param database_name: string
        The database to connect to
    :param table_name: string
        The database table to be queried
    :param item1: string
         An item for calculating similarity
    :param item2: string
         An item for calculating similarity
    :return: jaccard_num
         The jaccard similarity between two items
    """

    conn = connect_database(database_name)

    c = conn.cursor()
    sql1 = ("select * from [{0}] where ITEM_ID = '{1}'".format(table_name, item1))
    sql2 = ("select * from [{0}] where ITEM_ID = '{1}'".format(table_name, item2))

    c.execute(sql1)
    infolist1 = c.fetchall()
    c.execute(sql2)
    infolist2 = c.fetchall()

    for member in infolist1:
        tuple_list1 = member[1]  # get the causing gene list from the result of querying
        tuple_list1 = tuple_list1.split(',')
        set_list1 = set(tuple_list1)  # transfer the causing gene list into set, set A
        set_list1_len = len(set_list1)  # the size of the causing gene set A
    for member2 in infolist2:
        tuple_list2 = member2[1]
        tuple_list2 = tuple_list2.split(',')
        set_list2 = set(tuple_list2)  # set B
        set_list2_len = len(set_list2)  # the size of causing gene set B

    set1_and_set2_list = set_list1 & set_list2  # the intersection of set A and set B
    # print(set1_and_set2_list)
    set1_and_set2_list_len = len(set1_and_set2_list)  # the size of the intersection of set A and set B

    jaccard_num = set1_and_set2_list_len / (set_list1_len + set_list2_len - set1_and_set2_list_len)

    jaccard_num = '%.5f' % jaccard_num

    conn.close()

    return jaccard_num

# print(cal_2itemjaccard('sample','item', 'i1','j2'))


def cal_2itemcosine(database_name, table_name, item1, item2):
    """
        Calculate similarity between two items based on Cosine method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param item1: string
            An item for calculating similarity
    :param item2: string
            An item for calculating similarity
    :return: cosθ
            The Cosine similarity between two items
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    sql1 = ("select * from [{0}] where ITEM_ID = '{1}'".format(table_name, item1))
    sql2 = ("select * from [{0}] where ITEM_ID = '{1}'".format(table_name, item2))

    c.execute(sql1)
    infolist1 = c.fetchall()
    c.execute(sql2)
    infolist2 = c.fetchall()

    ########################################################
    # 原来的部分，只看其出现没出现，设置0/1，不关心其出现的次数
    ########################################################
    # for member1 in infolist1:
    #     tuple_list1 = member1[1]
    #     tuple_list1 = tuple_list1.split(',')
    #     set_list1 = set(tuple_list1)  # 集合A
    #     # print(len(set_list1))
    # for member2 in infolist2:
    #     tuple_list2 = member2[1]
    #     tuple_list2 = tuple_list2.split(',')
    #     set_list2 = set(tuple_list2)  # 集合B
    #     # print(len(set_list2))
    # set1_union_set2_list = set_list1 | set_list2

    for member1 in infolist1:
        vector_list1 = member1[1]
        vector_list1 = vector_list1.split(',')
        set_list1 = set(vector_list1)
    for member2 in infolist2:
        vector_list2 = member2[1]
        vector_list2 = vector_list2.split(',')
        set_list2 = set(vector_list2)

    set1_union_set2_list = set_list1 | set_list2

    vector1 = []
    vector2 = []

    for item in set1_union_set2_list:
        num = 0
        for key in vector_list1:
            if key == item:
                num = num + 1
        vector1.append(num)

    for item in set1_union_set2_list:
        num = 0
        for key in vector_list2:
            if key == item:
                num = num + 1
        vector2.append(num)

    # print(set1_union_set2_list)
    # print(len(set1_union_set2_list))

    # samelist = []
    # for key1 in set_list1:
    #     for key2 in set_list2:
    #         if key1 == key2:
    #             samelist.append(key1)
    # print(samelist)

    ########################################################
    # 原来的部分，只看其出现没出现，设置0/1，不关心其出现的次数
    ########################################################
    # vector1 = []
    # vector2 = []
    #
    # for item in set1_union_set2_list:
    #     if item in set_list1:
    #         vector1.append(1)
    #     elif item not in set_list1:
    #         vector1.append(0)
    #     if item in set_list2:
    #         vector2.append(1)
    #     elif item not in set_list2:
    #         vector2.append(0)

    # print(vector1)
    # print(vector2)
    vectorlen = len(set1_union_set2_list)
    a = b = c = 0
    for i in range(vectorlen):
        a = a + vector1[i] * vector2[i]
        b = b + vector1[i] * vector1[i]
        c = c + vector2[i] * vector2[i]
    cosθ = a / ((b ** 0.5) * (c ** 0.5))
    cosθ = '%.5f' % cosθ

    conn.close()

    return cosθ


# print(cal_2itemcosine('sample', 'item', 'j1', 'i1'))


def cal_2itemlin(database_name, table_name, item1, item2):
    """
        Calculate similarity between two items based on Lin's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param item1: string
            An item for calculating similarity
    :param item2: string
            An item for calculating similarity
    :return: lin_num
            The Lin's method similarity between two items
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    sql1 = ("select * from [{0}] where ITEM_ID = '{1}'".format(table_name, item1))
    sql2 = ("select * from [{0}] where ITEM_ID = '{1}'".format(table_name, item2))

    c.execute(sql1)
    infolist1 = c.fetchall()
    c.execute(sql2)
    infolist2 = c.fetchall()

    for member in infolist1:
        tuple_list1 = member[1]  # get the causing gene list from the result of querying
        tuple_list1 = tuple_list1.split(',')
        set_list1 = set(tuple_list1)  # transfer the causing gene list into set, set A
        set_list1_len = len(set_list1)  # the size of the causing gene set A
    for member2 in infolist2:
        tuple_list2 = member2[1]
        tuple_list2 = tuple_list2.split(',')
        set_list2 = set(tuple_list2)  # set B
        set_list2_len = len(set_list2)  # the size of causing gene set B
    set1_and_set2_list = set_list1 & set_list2  # the intersection of set A and set B
    # print(set1_and_set2_list)
    set1_and_set2_list_len = len(set1_and_set2_list)  # the size of the intersection of set A and set B

    # print(set_list1_len, set_list2_len, set1_and_set2_list_len)
    lin_num = (2 * set1_and_set2_list_len) / (set_list1_len + set_list2_len)

    lin_num = '%.5f' % lin_num

    conn.close()

    return lin_num

# print(cal_2itemlin('sample', 'item', 'j1', 'i1'))


def cal_itemlistjaccard(database_name, table_name, item_group1, item_group2):
    """
        Calculate similarity metrix between two list of items based on Jaccard Index
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param item_group1: string
            A disease group for calculating similarity
    :param item_group2: string
            A disease group for calculating similarity
    :return: sim
            The similarity matrix based on Jaccard Index between the two lists of items
    """

    item_group1 = item_group1.split(',')
    item_group2 = item_group2.split(',')

    # m = len(individual_group1)
    # n = len(individual_group2)  # 创建的是m*n大小的矩阵

    lst = []
    for item_name1 in item_group1:
        a = []
        for item_name2 in item_group2:
            s = cal_2itemjaccard(database_name, table_name, item_name1, item_name2)
            a.append(s)
        lst.append(a)

    sim = np.matrix(lst)

    return sim


# print(cal_itemlistjaccard('sample', 'item', 'j1,j2', 'i1,i2'))



def cal_itemlistcosine(database_name, table_name, item_group1, item_group2):
    """
        Calculate similarity metrix between two list of items based on Cosine method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param item_group1: string
            A disease group for calculating similarity
    :param item_group2: string
            A disease group for calculating similarity
    :return: sim
            The similarity matrix based on Cosine method between the two lists of items
    """

    item_group1 = item_group1.split(',')
    item_group2 = item_group2.split(',')

    # m = len(individual_group1)
    # n = len(individual_group2)  # 创建的是m*n大小的矩阵

    lst = []
    for item_name1 in item_group1:
        a = []
        for item_name2 in item_group2:
            s = cal_2itemcosine(database_name, table_name, item_name1, item_name2)
            a.append(s)
        lst.append(a)

    sim = np.matrix(lst)

    return sim


# print(cal_itemlistcosine('sample', 'item', 'j1,j2,i1,i2', 'i1,i2,j1,j2'))


def cal_itemlistlin(database_name, table_name, item_group1, item_group2):
    """
        Calculate similarity metrix between two list of items based on Lin's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param item_group1: string
            A disease group for calculating similarity
    :param item_group2: string
            A disease group for calculating similarity
    :return: sim
            The similarity matrix based on Lin's method between the two lists of items
    """

    item_group1 = item_group1.split(',')
    item_group2 = item_group2.split(',')

    # m = len(individual_group1)
    # n = len(individual_group2)  # 创建的是m*n大小的矩阵

    lst = []
    for item_name1 in item_group1:
        a = []
        for item_name2 in item_group2:
            s = cal_2itemlin(database_name, table_name, item_name1, item_name2)
            a.append(s)
        lst.append(a)

    sim = np.matrix(lst)

    return sim


# print(cal_itemlistlin('sample', 'item', 'j1,j2,i1,i2', 'i1,i2,j1,j2'))