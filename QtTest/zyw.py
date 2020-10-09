# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:zyw.py
@time:2020/09/30
"""

# coding=gbk
from sys import argv
from os import listdir,system

sql_list = ['sys_department.sql', 'sys_dictionary.sql', 'sys_menu.sql', 't_panel_element.sql',
            't_panel_element_category.sql', 'sys_role.sql', 'sys_role_menu.sql']


def run_structure(*args):
    db_host, db_port, db_user, db_password, db_name, run_mode = args
    sql_storage_path = r'C:\mysqlscript' if run_mode == 1 else r'C:\mysqlscript_data'
    base_sql = f"mysql -h {db_host} -p {db_port} -u {db_user} -p {db_password} {db_name} < {sql_storage_path}"
    file_list = [i if i in sql_list else None for i in listdir(sql_storage_path) if run_mode != 1]
    mysqldata_list = [f"{base_sql} {i}" for i in file_list]
    list(map(system, mysqldata_list))


if __name__ == '__main__':
    run_structure(argv[1:])
