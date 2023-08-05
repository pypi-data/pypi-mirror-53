import numpy as np
from sim.cal_itemsim import *
from data.connect_database import *
import numpy as np


def cal_2groupaverage(database_name, table_name, group_name1, group_name2, item_method):
    """
        Calculate similarity between two disease groups based on average method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_name1: string
            A group for calculating similarity
    :param group_name2: string
            A group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: average
            The average similarity between two groups
    """
    ###############################
    # 得到group的item信息
    ###############################
    item_list1 = get_group_info(database_name, table_name, group_name1)[1]
    item_list2 = get_group_info(database_name, table_name, group_name2)[1]

    item_list1 = item_list1.split(',')
    item_list2 = item_list2.split(',')

    sim_list = []  # 列表，两两相似值计算后加入该列表中

    for item1 in item_list1:
        for item2 in item_list2:
            if item_method == 'jaccard':
                sim = cal_2itemjaccard(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            elif item_method == 'cosine':
                sim = cal_2itemcosine(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            elif item_method == 'lin':
                sim = cal_2itemlin(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            # elif indi_method == 'mathur':
            #     sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
            #     sim = float(sim)
            #     sim_list.append(sim)

            else:
                print("wrong item similarity method!")
                exit(0)

    sim_sum = 0
    # print(sim_list)
    # print(item_list1,item_list2)
    for sim_value in sim_list:
        sim_sum = sim_sum + sim_value

    average = sim_sum / len(sim_list)

    average = '%.5f' % average

    return average


# print(cal_2groupaverage('sample', 'group', 'I', 'J', 'lin'))


def cal_2groupcomplete(database_name, table_name, group_name1, group_name2, item_method):
    """
        Calculate similarity between two disease groups based on complete method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_name1: string
            A group for calculating similarity
    :param group_name2: string
            A group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: complete
            The complete similarity between two groups
    """
    ###############################
    # 得到group的item信息
    ###############################
    item_list1 = get_group_info(database_name, table_name, group_name1)[1]
    item_list2 = get_group_info(database_name, table_name, group_name2)[1]

    item_list1 = item_list1.split(',')
    item_list2 = item_list2.split(',')

    sim_list = []  # 列表，两两相似值计算后加入该列表中

    for item1 in item_list1:
        for item2 in item_list2:
            if item_method == 'jaccard':
                sim = cal_2itemjaccard(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            elif item_method == 'cosine':
                sim = cal_2itemcosine(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            elif item_method == 'lin':
                sim = cal_2itemlin(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            # elif indi_method == 'mathur':
            #     sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
            #     sim = float(sim)
            #     sim_list.append(sim)

            else:
                print("wrong item similarity method!")
                exit(0)

    complete = max(sim_list)

    complete = '%.5f' % complete

    return complete


# print(cal_2groupcomplete('sample', 'group', 'I', 'J', 'lin'))


def cal_2groupsingle(database_name, table_name, group_name1, group_name2, item_method):
    """
        Calculate similarity between two disease groups based on single method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_name1: string
            A group for calculating similarity
    :param group_name2: string
            A group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: single
            The single similarity between two groups
    """

    ###############################
    # 得到group的item信息
    ###############################
    item_list1 = get_group_info(database_name, table_name, group_name1)[1]
    item_list2 = get_group_info(database_name, table_name, group_name2)[1]

    item_list1 = item_list1.split(',')
    item_list2 = item_list2.split(',')

    sim_list = []  # 列表，两两相似值计算后加入该列表中

    for item1 in item_list1:
        for item2 in item_list2:
            if item_method == 'jaccard':
                sim = cal_2itemjaccard(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            elif item_method == 'cosine':
                sim = cal_2itemcosine(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            elif item_method == 'lin':
                sim = cal_2itemlin(database_name, 'item', item1, item2)
                sim = float(sim)
                sim_list.append(sim)

            # elif indi_method == 'mathur':
            #     sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
            #     sim = float(sim)
            #     sim_list.append(sim)

            else:
                print("wrong item similarity method!")
                exit(0)

    single = min(sim_list)

    single = '%.5f' % single

    return single


# print(cal_2groupsingle('sample', 'group', 'I', 'J', 'lin'))

def cal_grouplistaverage(database_name, table_name, group_list1, group_list2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on average method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_list1: string
            A list of group for calculating similarity
    :param group_list2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The average similarity matrix between the two lists of group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2groupaverage(database_name, table_name, group_name1, group_name2, item_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_grouplistaverage('sample', 'group', 'I,J', 'I,J', 'cosine'))


def cal_grouplistcomplete(database_name, table_name, group_list1, group_list2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on complete method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_list1: string
            A list of group for calculating similarity
    :param group_list2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The complete similarity matrix between the two lists of group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2groupcomplete(database_name, table_name, group_name1, group_name2, item_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_grouplistcomplete('sample', 'group', 'I,J', 'I,J', 'lin'))

def cal_grouplistsingle(database_name, table_name, group_list1, group_list2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on single method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_list1: string
            A list of group for calculating similarity
    :param group_list2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The single similarity matrix between the two lists of group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2groupsingle(database_name, table_name, group_name1, group_name2, item_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_grouplistsingle('sample', 'group', 'I,J', 'I,J', 'cosine'))


def cal_2group_itemmodule(database_name, table_name, group_name1, group_name2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on single method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_name1: string
            A list of group for calculating similarity
    :param group_name2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The similarity score between the two lists of group based on item_method
    """
    element_list1 = get_group_info(database_name, table_name, group_name1)[3]
    element_list2 = get_group_info(database_name, table_name, group_name2)[3]

    shared_element_list = get_2group_shared_items(database_name, table_name, group_name1, group_name2)[2]

    element_list1 = element_list1.split(',')
    element_list2 = element_list2.split(',')
    shared_element_list = shared_element_list.split(',')
    # print(element_list1)
    # print(element_list2)
    # print(shared_element_list)

    if item_method is 'jaccard':
        element_list1_len = get_group_info(database_name, table_name, group_name1)[4]
        element_list2_len = get_group_info(database_name, table_name, group_name2)[4]
        shared_element_list_len = get_2group_shared_elements(database_name, table_name, group_name1, group_name2)[3]

        sim = float(shared_element_list_len) / (float(element_list1_len) + float(element_list2_len) -
                                                     float(shared_element_list_len))

        # print(element_list1_len, element_list2_len, shared_element_list_len)

        sim = '%.5f' % sim

    elif item_method is 'cosine':
        cosine_set1 = set(element_list1)
        cosine_set2 = set(element_list2)

        set1_union_set2 = cosine_set1 | cosine_set2

        vector1 = []
        vector2 = []

        #######################################################
        # 原来的部分，只看其出现没出现，设置0/1，不关心其出现的次数
        #######################################################
        # for item in set1_union_set2:
        #     if item in cosine_set1:
        #         vector1.append(1)
        #     elif item not in cosine_set1:
        #         vector1.append(0)
        #     if item in cosine_set2:
        #         vector2.append(1)
        #     elif item not in cosine_set2:
        #         vector2.append(0)
        # print(vector1)
        # print(vector2)

        for item in set1_union_set2:
            num = 0
            for key in element_list1:
                if key == item:
                    num = num + 1
            vector1.append(num)

        for item in set1_union_set2:
            num = 0
            for key in element_list2:
                if key == item:
                    num = num + 1
            vector2.append(num)

        vectorlen = len(set1_union_set2)
        a = b = c = 0
        for i in range(vectorlen):
            a = a + vector1[i] * vector2[i]
            b = b + vector1[i] * vector1[i]
            c = c + vector2[i] * vector2[i]

        sim = a / ((b ** 0.5) * (c ** 0.5))
        sim = '%.5f' % sim

    elif item_method is 'lin':
        element_list1_len = get_group_info(database_name, table_name, group_name1)[4]
        element_list2_len = get_group_info(database_name, table_name, group_name2)[4]
        shared_element_list_len = get_2group_shared_elements(database_name, table_name, group_name1, group_name2)[3]

        sim = (2 * float(shared_element_list_len)) / (element_list1_len + element_list2_len)
        sim = '%.5f' % sim

    return sim


# print(cal_2group_itemmodule('sample', 'group', 'I', 'J', 'jaccard'))


def cal_grouplist_itemmodule(database_name, table_name, group_list1, group_list2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on item_module method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_list1: string
            A list of group for calculating similarity
    :param group_list2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The similarity matrix between the two lists of group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2group_itemmodule(database_name, table_name, group_name1, group_name2, item_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim

# print(cal_grouplist_itemmodule('sample', 'group', 'I,J', 'I,J', 'lin'))


def cal_2groupfunsimmax(database_name, table_name, group_name1, group_name2, item_method):
    """
        Calculate similarity between two disease groups based on funsimmax method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_name1: string
            A group for calculating similarity
    :param group_name2: string
            A group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: average
            The funsimmax similarity between two groups
    """
    item_list1 = get_group_info(database_name, table_name, group_name1)[1]
    item_list2 = get_group_info(database_name, table_name, group_name2)[1]

    item_list1 = item_list1.split(',')
    item_list2 = item_list2.split(',')

    row_num = len(item_list1)
    column_num = len(item_list2)
    # print(row_num, column_num)

    lst = []

    for item1 in item_list1:
        a = []
        for item2 in item_list2:
            if item_method == 'jaccard':
                sim = cal_2itemjaccard(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            elif item_method == 'cosine':
                sim = cal_2itemcosine(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            elif item_method == 'lin':
                sim = cal_2itemlin(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            # elif indi_method == 'mathur':
            #     sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
            #     sim = float(sim)
            #     a.append(sim)

            else:
                print("wrong item similarity method!")
                exit(0)
        lst.append(a)

    sim_matrix = np.matrix(lst)
    # print(sim_matrix)

    row_simlist = np.max(sim_matrix, 1)
    column_simlist = np.max(sim_matrix, 0)

    # print(row_simlist, column_simlist)

    addrow = 0
    addcolumn = 0

    for item in row_simlist:
        item = float(item)
        addrow = addrow + item

    lst_columnsim = column_simlist.tolist()  # 行/列矩阵最大值，存储的形式不一样注意这里的形式转换

    for item in lst_columnsim[0]:
        item = float(item)
        addcolumn = addcolumn + item

    row_score = addrow / row_num
    column_score = addcolumn / column_num
    # print(row_score,column_score)

    funsimmax = max(row_score, column_score)
    funsimmax = '%.5f' % funsimmax

    return funsimmax


# print(cal_2groupfunsimmax('sample', 'group', 'I', 'J', 'jaccard'))


def cal_2groupfunsimavg(database_name, table_name, group_name1, group_name2, item_method):
    """
        Calculate similarity between two disease groups based on funsimavg method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_name1: string
            A group for calculating similarity
    :param group_name2: string
            A group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: average
            The funsimavg similarity between two groups
    """
    item_list1 = get_group_info(database_name, table_name, group_name1)[1]
    item_list2 = get_group_info(database_name, table_name, group_name2)[1]

    item_list1 = item_list1.split(',')
    item_list2 = item_list2.split(',')

    row_num = len(item_list1)
    column_num = len(item_list2)
    # print(row_num, column_num)

    lst = []

    for item1 in item_list1:
        a = []
        for item2 in item_list2:
            if item_method == 'jaccard':
                sim = cal_2itemjaccard(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            elif item_method == 'cosine':
                sim = cal_2itemcosine(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            elif item_method == 'lin':
                sim = cal_2itemlin(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            # elif indi_method == 'mathur':
            #     sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
            #     sim = float(sim)
            #     a.append(sim)

            else:
                print("wrong item similarity method!")
                exit(0)
        lst.append(a)

    sim_matrix = np.matrix(lst)
    # print(sim_matrix)

    row_simlist = np.max(sim_matrix, 1)
    column_simlist = np.max(sim_matrix, 0)

    # print(row_simlist, column_simlist)

    # print(row_simlist, column_simlist)

    addrow = 0
    addcolumn = 0

    for item in row_simlist:
        item = float(item)
        addrow = addrow + item

    lst_columnsim = column_simlist.tolist()  # 行/列矩阵最大值，存储的形式不一样注意这里的形式转换

    for item in lst_columnsim[0]:
        item = float(item)
        addcolumn = addcolumn + item

    row_score = addrow / row_num
    column_score = addcolumn / column_num

    # print(row_score,column_score)

    funsimavg = 0.5 * (row_score + column_score)
    funsimavg = '%.5f' % funsimavg

    return funsimavg


# print(cal_2groupfunsimavg('sample', 'group', 'I', 'J', 'jaccard'))


def cal_2groupbma(database_name, table_name, group_name1, group_name2, item_method):
    """
        Calculate similarity between two disease groups based on bma method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_name1: string
            A group for calculating similarity
    :param group_name2: string
            A group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: average
            The bma similarity between two groups
       """
    item_list1 = get_group_info(database_name, table_name, group_name1)[1]
    item_list2 = get_group_info(database_name, table_name, group_name2)[1]

    item_list1 = item_list1.split(',')
    item_list2 = item_list2.split(',')

    row_num = len(item_list1)
    column_num = len(item_list2)
    # print(row_num, column_num)

    lst = []

    for item1 in item_list1:
        a = []
        for item2 in item_list2:
            if item_method == 'jaccard':
                sim = cal_2itemjaccard(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            elif item_method == 'cosine':
                sim = cal_2itemcosine(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            elif item_method == 'lin':
                sim = cal_2itemlin(database_name, 'item', item1, item2)
                sim = float(sim)
                a.append(sim)

            # elif indi_method == 'mathur':
            #     sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
            #     sim = float(sim)
            #     a.append(sim)

            else:
                print("wrong item similarity method!")
                exit(0)
        lst.append(a)

    sim_matrix = np.matrix(lst)
    # print(sim_matrix)

    row_simlist = np.max(sim_matrix, 1)
    column_simlist = np.max(sim_matrix, 0)

    # print(row_simlist, column_simlist)

    # print(row_simlist, column_simlist)

    addrow = 0
    addcolumn = 0

    for item in row_simlist:
        item = float(item)
        addrow = addrow + item

    lst_columnsim = column_simlist.tolist()  # 行/列矩阵最大值，存储的形式不一样注意这里的形式转换

    for item in lst_columnsim[0]:
        item = float(item)
        addcolumn = addcolumn + item

    bma = (addrow + addcolumn) / (row_num + column_num)
    bma = '%.5f' % bma

    return bma


# print(cal_2groupbma('sample', 'group', 'I', 'J', 'jaccard'))


def cal_grouplistfunsimmax(database_name, table_name, group_list1, group_list2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on funsimmax method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_list1: string
            A list of group for calculating similarity
    :param group_list2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The funsimmax similarity matrix between the two lists of group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2groupfunsimmax(database_name, table_name, group_name1, group_name2, item_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_grouplistfunsimmax('sample', 'group', 'I,J', 'I,J', 'jaccard'))

def cal_grouplistfunsimavg(database_name, table_name, group_list1, group_list2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on funsimavg method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_list1: string
            A list of group for calculating similarity
    :param group_list2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The funsimavg similarity matrix between the two lists of group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2groupfunsimavg(database_name, table_name, group_name1, group_name2, item_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_grouplistfunsimavg('sample', 'group', 'I,J', 'I,J', 'jaccard'))

def cal_grouplistbma(database_name, table_name, group_list1, group_list2, item_method):
    """
        Calculate the similarity matrix between two lists of group based on bma method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param group_list1: string
            A list of group for calculating similarity
    :param group_list2: string
            A list of group for calculating similarity
    :param item_method: string
            Methods for calculating similarity between two diseases presented in "cal_itemsim.py"
            jaccard/cosine/lin
    :return: sim
            The bma similarity matrix between the two lists of group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2groupbma(database_name, table_name, group_name1, group_name2, item_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_grouplistbma('sample', 'group', 'I,J', 'I,J', 'jaccard'))