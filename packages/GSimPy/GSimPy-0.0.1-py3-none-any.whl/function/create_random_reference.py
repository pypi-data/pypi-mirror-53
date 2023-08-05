from function.get_datainfo import *
import random


def create_random_item(database_name, item_table_name, item):
    """
        Create random item example.
        The element number of each item are unchanged, but its elements are randomly selected from all elemets.
    :param database_name: string
            The database to connect to
    :param item_table_name: string
            item table
    :param item: string
            item id
    :return: random_item_info_list
            ITEM_ID, ELEMENT_LIST, ELEMENT_NUM
    """

    item_info = get_item_info(database_name, item_table_name, item)
    element_num = item_info[2]

    all_element_list = get_all_element_list(database_name, item_table_name)

    random_list = []
    random_list_len = len(random_list)

    while random_list_len is not element_num:
        random_element = random.choice(all_element_list)
        if random_element not in random_list:
            random_list.append(random_element)
            random_list_len = random_list_len + 1

    return item, random_list, random_list_len


# print(create_random_item('sample', 'item', 'i1'))


def create_random_group(database_name, group_table_name, item_table_name, group):
    """
        Create random group sample
        The element number of each item from group are unchanged, but its elements are randomly selected from all elemets.
    :param database_name: string
            The database to connect to
    :param group_table_name: string
            group table
    :param item_table_name: string
            item table
    :param group: string
            group id
    :return: random_group_info_list
    """

    group_info = get_group_info(database_name, group_table_name, group)
    item_list = group_info[1]
    item_list = item_list.split(',')
    item_num = len(item_list)

    group_random_list = []
    for item in item_list:
        item, random_list, random_list_len = create_random_item(database_name, item_table_name, item)
        # print(item, random_list)
        for element in random_list:
            if element not in group_random_list:
                group_random_list.append(element)

    group_ramdom_list_len = len(group_random_list)

    return group, item_list, item_num, group_random_list, group_ramdom_list_len


# print(create_random_group('sample', 'group', 'item', 'J'))

