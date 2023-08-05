from data.connect_database import *


def get_group_info(database_name, table_name, group_name):
    """
            Query item-element information from item table

        :param database_name: string
                The database to connect to
        :param table_name: string
                The database table being queried
        :param group_name: string
                The item for query
        :return: query_list
                Information in query_list represent GROUP_ID, ITEM_LIST, ITEM_NUM, ELEMENT_LIST, ELEMENT_NUM respectively.
        """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from [{0}] where GROUP_ID = '{1}'".format(table_name, group_name))
    c.execute(sql)
    query_info = c.fetchall()
    query_info = query_info[0]
    query_list = list(query_info)

    conn.close()

    return query_list

# print(get_group_info('sample', 'group', 'I'))


def get_item_info(database_name, table_name, item_name):
    """
        Query item-element information from item table

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param item_name: string
            The item for query
    :return: query_list
            Information in query_list represent ITEM_ID, ELEMENT_LIST, ELEMENT_NUM, respectively.
    """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from {0} where ITEM_ID = '{1}'".format(table_name,item_name))
    c.execute(sql)
    query_info = c.fetchall()
    query_info = query_info[0]
    query_list = list(query_info)

    conn.close()

    return query_list

# print(get_item_info('sample','item', 'i1'))


def get_2group_shared_items(database_name, table_name, group1, group2):
    """
        Query the shared items information between group1 and group2
    :param database_name: string
            The database to connect to
    :param table_name: string
            The item table being queried
    :param group_name1: string
            group_id of group1
    :param group_name2: string
            group_id of group2
    :return: query_list
            Information in query_list represent group1,group2,shared_item_list,shared_item_num
            respectively.
    """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from [{0}] where GROUP_ID = '{1}' ".format(table_name, group1))
    c.execute(sql)

    query1_info = c.fetchall()
    query1_info = query1_info[0]
    query1_1ist = list(query1_info)

    sql = ("select * from [{0}] where GROUP_ID = '{1}' ".format(table_name, group2))
    c.execute(sql)

    query2_info = c.fetchall()
    query2_info = query2_info[0]
    query2_1ist = list(query2_info)

    itemlist1 = query1_1ist[1]
    itemlist1 = itemlist1.split(',')
    itemset1 = set(itemlist1)

    itemlist2 = query2_1ist[1]
    itemlist2 = itemlist2.split(',')
    itemset2 = set(itemlist2)

    shared_itemset = itemset1 & itemset2
    shared_itemlist = list(shared_itemset)
    num_of_shared_item = len(shared_itemlist)
    shared_itemlist = ','.join(shared_itemlist)

    query_list = list()
    query_list.append(group1)
    query_list.append(group2)
    query_list.append(shared_itemlist)
    query_list.append(num_of_shared_item)

    conn.close()

    return query_list


# print(get_2group_shared_items('sample', 'group', 'I', 'J'))


def get_2item_shared_elements(database_name, table_name, item1, item2):
    """
        Query the shared elements information between item1 and item2
    :param database_name: string
            The database to connect to
    :param table_name: string
            The item table being queried
    :param item1: string
            item_id of item1
    :param item2: string
            item_id of item2
    :return: query_list
            Information in query_list represent item1,item2,shared_element_list,shared_element_num
            respectively.
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from [{0}] where ITEM_ID = '{1}' ".format(table_name, item1))
    c.execute(sql)

    query1_info = c.fetchall()
    query1_info = query1_info[0]
    query1_1ist = list(query1_info)

    sql = ("select * from [{0}] where ITEM_ID = '{1}' ".format(table_name, item2))
    c.execute(sql)

    query2_info = c.fetchall()
    query2_info = query2_info[0]
    query2_1ist = list(query2_info)

    elementlist1 = query1_1ist[1]
    elementlist1 = elementlist1.split(',')
    elementset1 = set(elementlist1)

    elementlist2 = query2_1ist[1]
    elementlist2 = elementlist2.split(',')
    elementset2 = set(elementlist2)

    shared_elementset = elementset1 & elementset2
    shared_elementlist = list(shared_elementset)
    num_of_shared_element = len(shared_elementlist)
    shared_elementlist = ','.join(shared_elementlist)

    query_list = list()
    query_list.append(item1)
    query_list.append(item2)
    query_list.append(shared_elementlist)
    query_list.append(num_of_shared_element)

    conn.close()

    return query_list


# print(get_2item_shared_elements('sample', 'item', 'i2', 'j2'))


def get_2group_shared_elements(database_name, table_name, group1, group2):
    """
        Query the shared elements information between group1 and group2
    :param database_name: string
            The database to connect to
    :param table_name: string
            The item table being queried
    :param group1: string
            group_id of group1
    :param group2: string
            group_id of group2
    :return: query_list
            Information in query_list represent group1,group2,shared_element_list,shared_element_num
            respectively.
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from [{0}] where GROUP_ID = '{1}' ".format(table_name, group1))
    c.execute(sql)

    query1_info = c.fetchall()
    query1_info = query1_info[0]
    query1_1ist = list(query1_info)

    sql = ("select * from [{0}] where GROUP_ID = '{1}' ".format(table_name, group2))
    c.execute(sql)

    query2_info = c.fetchall()
    query2_info = query2_info[0]
    query2_1ist = list(query2_info)

    elementlist1 = query1_1ist[3]
    elementlist1 = elementlist1.split(',')
    elementset1 = set(elementlist1)

    elementlist2 = query2_1ist[3]
    elementlist2 = elementlist2.split(',')
    elementset2 = set(elementlist2)

    shared_elementset = elementset1 & elementset2
    shared_elementlist = list(shared_elementset)
    num_of_shared_element = len(shared_elementlist)
    shared_elementlist = ','.join(shared_elementlist)

    query_list = list()
    query_list.append(group1)
    query_list.append(group2)
    query_list.append(shared_elementlist)
    query_list.append(num_of_shared_element)

    conn.close()

    return query_list


# print(get_2group_shared_elements('sample', 'group', 'I', 'J'))

def get_all_element_num(database_name, table_name):
    """
        Query all element number

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :return: all_element_num
            The number of all the elements
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    all_element_list = list()

    sql = ("select * from [{0}]".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        tuple_list = query_line[1]
        tuple_list = tuple_list.split(',')
        for gene in tuple_list:
            if gene not in all_element_list:
                all_element_list.append(gene)

    all_element_num = len(all_element_list)

    return all_element_num

# print(get_all_element_num('sample','item'))


def get_all_element_list(database_name, table_name):
    """
        Query the list of all elements
    :param database_name: string
        The database to connect to
    :param table_name: string
        The item table
    :return: all_element_list
        The list of all elements
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    all_element_list = list()

    sql = ("select * from [{0}]".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        tuple_list = query_line[1]
        tuple_list = tuple_list.split(',')
        for gene in tuple_list:
            if gene not in all_element_list:
                all_element_list.append(gene)

    return all_element_list


# print(get_all_element_list('sample', 'item'))



def get_all_group_num(database_name, table_name):
    """
           Query all group number
       :param database_name: string
           The database to connect to
       :param table_name: string
           The group table name
       :return: all_group_num
           The number of all the group
       """
    conn = connect_database(database_name)
    c = conn.cursor()
    all_group_list = list()

    sql = ("select * from [{0}]".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        group = query_line[0]
        if group not in all_group_list:
            all_group_list.append(group)

    all_group_num = len(all_group_list)

    return all_group_num


def get_all_item_num(database_name, table_name):
    """
        Query all element number
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :return: all_item_num
            The number of all the items
    """
    conn = connect_database(database_name)
    c = conn.cursor()
    all_item_list = list()

    sql = ("select * from [{0}]".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        mesh = query_line[0]
        if mesh not in all_item_list:
            all_item_list.append(mesh)
    all_item_num = len(all_item_list)

    return all_item_num


# print(get_all_item_num('sample','item'))





# print(get_all_group_num('sample','group'))