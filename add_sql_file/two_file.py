import datetime

import pymysql
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
def do_all_list(one_list):
    format_data = {}
    for one in one_list:
        subject_id = one.get("column6")
        if subject_id == None:
            continue
        db_subject_id = int(subject_id)
        first_subject = one.get('column1')
        if first_subject:
            if "（" in first_subject:
                first_subject = str(first_subject).split("（")[0]
            elif "(" in first_subject:
                first_subject = str(first_subject).split("(")[0]
        second_subject = one.get("column2")
        if second_subject:
            if "（" in second_subject:
                second_subject = str(second_subject).split("（")[0]
            elif "(" in second_subject:
                second_subject = str(second_subject).split("(")[0]
        third_subject = one.get("column3")
        if third_subject:
            if "（" in third_subject:
                third_subject = str(third_subject).split("（")[0]
            elif "(" in third_subject:
                third_subject = str(third_subject).split("(")[0]
        fourth_subject = one.get("column4")
        if fourth_subject:
            if "（" in fourth_subject:
                fourth_subject = str(fourth_subject).split("（")[0]
            elif "(" in fourth_subject:
                fourth_subject = str(fourth_subject).split("(")[0]
        fifth_subject = one.get('column5')
        if fifth_subject:
            if "（" in fifth_subject:
                fifth_subject = str(fifth_subject).split("（")[0]
            elif "(" in fifth_subject:
                fifth_subject = str(fifth_subject).split("(")[0]
        updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 科目介绍
        subject_name = one.get("column9")
        hardness = 1
        if "简单" in subject_name:
            hardness = 1
        if "中等" in subject_name:
            hardness = 2
        if "困难" in subject_name:
            hardness = 3
        if subject_name:
            if "（" in subject_name:
                subject_name = str(subject_name).split("（")[0]
        intro_string = ""
        if subject_name:
            subject_name = subject_name.strip()
            intro_string = intro_string + "<h2>科目名称</h2><p>%s</p>" % (subject_name)
        subject_target = one.get("column10")
        if subject_target:
            subject_target = subject_target.strip()
            intro_string = intro_string + "<h2>科目目标</h2><p>%s</p>" % (subject_target)
        dongzuoyaoling = one.get("column11")
        if dongzuoyaoling:
            dongzuoyaoling = dongzuoyaoling.strip()
            intro_string = intro_string + "<h2>动作要领</h2><p>%s</p>" % (dongzuoyaoling)
        xunlianyaoqiu = one.get("column12")
        if xunlianyaoqiu:
            xunlianyaoqiu = xunlianyaoqiu.strip()
            intro_string = intro_string + "<h2>训练要求</h2><p>%s</p>" % (xunlianyaoqiu)
        changdiqicai = one.get("column13")
        if changdiqicai:
            changdiqicai = changdiqicai.strip()
            intro_string = intro_string + "<h2>场地器材</h2><p>%s</p>" % (changdiqicai)
        huxifangfa = one.get("column14")
        if huxifangfa:
            huxifangfa = huxifangfa.strip()
            intro_string = intro_string + "<h2>呼吸方法</h2><p>%s</p>" % (huxifangfa)
        changjianwenti = one.get("column15")
        if changjianwenti:
            changjianwenti = changjianwenti.strip()
            intro_string = intro_string + "<h2>常见问题</h2><p>%s</p>" % (changjianwenti)
        jiejuebanfa = one.get("column16")
        if jiejuebanfa:
            jiejuebanfa = jiejuebanfa.strip()
            intro_string = intro_string + "<h2>解决办法</h2><p>%s</p>" % (jiejuebanfa)
        print(intro_string)
        print("======================")
        # 图片地址json
        # 首先判断该科目是否有图片
        img_dict = {}
        img_name = one.get("column7")
        if not img_name == "无":
            img_num = 0
            # 根据当前的科目id发现该科目下的所有图片
            for one_tmp in one_list:
                if one_tmp.get("column6") == subject_id:
                    img_num = img_num + 1
            img_dict["1077"] = []
            img_dict['1920'] = []
            img_dict['607'] = []
            img_dict['883'] = []
            img_dict['img'] = []
            for i in range(img_num):
                img_head_url = 'http://115.29.66.237:9393/subject_imgs/'
                img_dict["1077"].append(img_head_url + "1077/" + str(subject_name) + str(i + 1) + "_1077.png")
                img_dict['1920'].append(img_head_url + "1920/" + str(subject_name) + str(i + 1) + "_1920.png")
                img_dict['607'].append(img_head_url + "607/" + str(subject_name) + str(i + 1) + "_607.png")
                img_dict["883"].append(img_head_url + "883/" + str(subject_name) + str(i + 1) + "_883.png")
                img_dict['img'].append(img_head_url + 'img/' + str(subject_name) + str(i + 1) + '.png')
        format_data[db_subject_id] = {
            "id": db_subject_id,
            "first_subject": first_subject,
            "second_subject": second_subject,
            "third_subject": third_subject,
            "fourth_subject": fourth_subject,
            "fifth_subject": fifth_subject,
            "photo_path": img_dict,
            "introduction": intro_string,
            "update_time": updatetime,
            "hardness": hardness
        }
    return format_data


# 生成sql
def create_sql_string(format_data):
    sql_string = ""
    for key, value in format_data.items():
        subject_id = value.get("id")
        print(subject_id)
        first_subject = value.get("first_subject")
        second_subject = value.get('second_subject')
        third_subject = value.get("third_subject")
        fourth_subject = value.get("fourth_subject")
        fifth_subject = value.get('fifth_subject')
        img_dict = value.get("photo_path")
        imgs_string = pymysql.escape_string(str(img_dict))
        introduction = value.get('introduction')
        update_time = value.get('update_time')
        hardness = value.get("hardness")
        one_sql = 'insert into subject(id,first_subject,second_subject,third_subject,fourth_subject,fifth_subject,photo_path,introduction,update_time,hardness) values("%s","%s","%s","%s","%s","%s","%s","%s","%s",%s);' % (
            subject_id, first_subject, second_subject, third_subject, fourth_subject, fifth_subject, imgs_string,
            introduction,
            update_time, hardness
        )
        one_row_sql = one_sql.replace("'", '"')
        sql_string = sql_string + one_row_sql
    return sql_string


# 写入文件
def write_sql_to_file(sql_string):
    with open("new_subject.sql", 'w') as f:
        f.write(sql_string)


if __name__ == '__main__':
    subject_list = read_excel()
    format_data = do_all_list(subject_list)
    sql_string = create_sql_string(format_data)
    write_sql_to_file(sql_string)
