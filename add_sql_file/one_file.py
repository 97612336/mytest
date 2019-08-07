import json

import pymysql

sql_str = '''
insert into subject(first_subject,second_subject,third_subject,fourth_subject,params) 
values("科目一","科目二","科目三","科目四","[1,2,3,4,5]");
'''
# -*- coding: utf-8 -*-
import xlrd


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook('a.xlsx')

    sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
    rows_num = sheet2.nrows
    cols_num = sheet2.ncols

    list1 = []
    list2 = []
    for r in range(rows_num):
        # 一行数据的实体类
        entity_dict = {}
        for c in range(cols_num):
            cell_value = sheet2.row_values(r)[c]
            if (cell_value is None or cell_value == ''):
                cell_value = (get_merged_cells_value(sheet2, r, c))
            the_key = 'column' + str(c + 1)
            entity_dict[the_key] = cell_value
        if 2 < r < 12:
            list1.append(entity_dict)
        elif r > 12:
            list2.append(entity_dict)
    return list1, list2


def get_merged_cells(sheet):
    """
    获取所有的合并单元格，格式如下：
    [(4, 5, 2, 4), (5, 6, 2, 4), (1, 4, 3, 4)]
    (4, 5, 2, 4) 的含义为：行 从下标4开始，到下标5（不包含）  列 从下标2开始，到下标4（不包含），为合并单元格
    :param sheet:
    :return:
    """
    return sheet.merged_cells


def get_merged_cells_value(sheet, row_index, col_index):
    """
    先判断给定的单元格，是否属于合并单元格；
    如果是合并单元格，就返回合并单元格的内容
    :return:
    """
    merged = get_merged_cells(sheet)
    for (rlow, rhigh, clow, chigh) in merged:
        if (row_index >= rlow and row_index < rhigh):
            if (col_index >= clow and col_index < chigh):
                cell_value = sheet.cell_value(rlow, clow)
                return cell_value
    return None


# 根据获取到的list,重新组合数据
def get_sql_from_list(one_list, type):
    sql = ""
    for one_row_dict in one_list:
        column1 = one_row_dict.get("column1")
        column2 = one_row_dict.get("column2")
        column3 = one_row_dict.get("column3")
        column4 = one_row_dict.get("column4")
        column5 = one_row_dict.get("column5")
        column6 = one_row_dict.get("column6")

        if not column2:
            break

        if type == 1:
            params = {}
            if column3:
                params['args_one'] = column3
            if column4:
                params['args_two'] = column4
            if column5:
                params['args_three'] = column5
            if column6:
                params['args_four']: column6
            params_str = str(params)
            res = pymysql.escape_string(params_str)
            sql_one = 'insert into subject(second_subject,third_subject,params) values("%s","%s","%s");' % (
                column1, column2, res
            )
            res_sql = sql_one.replace("'", '"')
            sql = sql + res_sql
        else:
            params = {}
            if column4:
                params["args_one"] = column4
            if column5:
                params['args_two'] = column5
            if column6:
                params['args_three'] = column6
            params_str = str(params)
            res = pymysql.escape_string(params_str)
            if column3:
                sql_one = 'insert into subject(second_subject,third_subject,fourth_subject,params) values("%s","%s","%s","%s");' % (
                    column1, column2, column3, res
                )
            else:
                sql_one = 'insert into subject(second_subject,third_subject,params) values("%s","%s","%s");' % (
                    column1, column2, res
                )
            res_sql = sql_one.replace("'", '"')
            sql = sql + res_sql
    return sql


if __name__ == "__main__":
    list1, list2 = read_excel()
    sql1 = get_sql_from_list(list1, 1)
    sql2 = get_sql_from_list(list2, 2)
    res_sql = sql1 + sql2
    with open("subject.sql", 'w') as f:
        f.write(res_sql)
