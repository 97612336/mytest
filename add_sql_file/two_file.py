import xlrd


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook('b.xlsx')

    sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
    rows_num = sheet2.nrows
    cols_num = sheet2.ncols

    list1 = []
    for r in range(rows_num):
        # 一行数据的实体类
        entity_dict = {}
        for c in range(cols_num):
            cell_value = sheet2.row_values(r)[c]
            if (cell_value is None or cell_value == ''):
                cell_value = (get_merged_cells_value(sheet2, r, c))
            the_key = 'column' + str(c + 1)
            entity_dict[the_key] = cell_value
        if 0 < r:
            list1.append(entity_dict)
    return list1


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

# 处理所有的单元文档


if __name__ == '__main__':
    subject_list = read_excel()
    i = 0
    for one_subject in subject_list:
        print(one_subject)
        i = i + 1
        print(i)
