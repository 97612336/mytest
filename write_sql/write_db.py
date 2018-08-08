import configparser
import os
import re
import time
import datetime
import pymysql
from decimal import Decimal
import json


# 得到连接数据库的connection
def get_db_connection():
    home = os.environ['HOME']
    inifile = '{}/.afsaas.cnf'.format(home)
    config = configparser.ConfigParser()
    config.read(inifile)
    user = config.get('client', 'user')
    password = config.get('client', 'password')
    host = config.get('client', 'host')
    config = {
        'host': host,
        'port': 3306,
        'user': user,
        'password': password,
        'db': 'cheyixiao',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)
    return connection


# 获取车易销数据库中所有车型id组成的列表
def get_all_cheyixiao_specs_id():
    db = get_db_connection()
    cursor = db.cursor()
    sql = 'select id from specs ;'
    cursor.execute(sql)
    res = cursor.fetchall()
    res_list = []
    for one in res:
        one_id = one.get("id")
        res_list.append(one_id)
    cursor.close()
    db.close()
    return res_list


# 根据车型id得到车型的配置,并写入配置到文件
def read_info_write_file(specs_id):
    db = get_db_connection()
    cursor = db.cursor()
    sql = "select * from afsaas.specs where id = %s" % specs_id
    cursor.execute(sql)
    res = cursor.fetchone()
    config_dict_str = res.get("config")
    config_dict = json.loads(config_dict_str)
    # 得到brands_name的值,string
    specs_sql = 'select series_id from specs where id =%s' % specs_id
    cursor.execute(specs_sql)
    specs_res = cursor.fetchone()
    series_id = specs_res.get("series_id")
    series_sql = 'select brand_id from series where id=%s' % series_id
    cursor.execute(series_sql)
    series_res = cursor.fetchone()
    brand_id = series_res.get("brand_id")
    brand_sql = 'select name from brands where id=%s' % brand_id
    cursor.execute(brand_sql)
    brand_res = cursor.fetchone()
    brands_name = brand_res.get("name")
    # 得到车型的价格,int实际价格
    guide_price = res.get("i2")
    if '~' in guide_price:
        price = int(Decimal(str(guide_price).split("万")[0]) * 10000)
    else:
        guide_price = Decimal(str(guide_price).replace("万", ""))
        price = int(guide_price * 10000)
    # 得到车的级别,string
    level_str = res.get("i4")
    if "微型" in level_str:
        level = 1
    elif "小型" in level_str:
        level = 2
    elif "紧凑型" in level_str:
        level = 3
    elif "中型" in level_str:
        level = 4
    elif "中大型" in level_str:
        level = 5
    elif "大型" in level_str:
        level = 6
    elif "跑车" in level_str:
        level = 7
    elif "SUV" in level_str:
        level = 8
    elif "MPV" in level_str:
        level = 9
    elif "微面" in level_str:
        level = 10
    elif "微卡" in level_str:
        level = 11
    elif "轻客" in level_str:
        level = 12
    elif "皮卡" in level_str:
        level = 13
    else:
        level = 0

    # 得到排量
    displacement_str = config_dict.get("i31")
    try:
        displacement_int = round(int(displacement_str) / 100) * 100
    except:
        displacement_int = 0
    if displacement_int == 0:
        displacement = 0
    elif displacement_int <= 1000:
        displacement = 1
    elif 1100 <= displacement_int <= 1600:
        displacement = 2
    elif 1700 <= displacement_int <= 2000:
        displacement = 3
    elif 2100 <= displacement_int <= 2500:
        displacement = 4
    elif 2600 <= displacement_int <= 3000:
        displacement = 5
    elif 3100 <= displacement_int <= 4000:
        displacement = 6
    elif displacement_int > 4000:
        displacement = 7
    else:
        displacement = 0
    # 得到座位数
    seat_str = config_dict.get("i27")
    try:
        seat_int = int(seat_str)
        if seat_int == 2:
            seat_num = 1
        elif seat_int == 4:
            seat_num = 2
        elif seat_int == 5:
            seat_num = 3
        elif seat_int == 6:
            seat_num = 4
        elif seat_int == 7:
            seat_num = 5
        else:
            seat_num = 6
    except:
        seat_num = 6
    # 得到结构数
    structure_str = config_dict.get("i25")
    structure_str2 = config_dict.get("i8")
    if not structure_str:
        structure_str = ""
    if not structure_str2:
        structure_str2 = ""
    if "两厢" in structure_str or "两厢" in structure_str2:
        structure = 1
    elif "三厢" in structure_str or "三厢" in structure_str2:
        structure = 2
    elif "掀背" in structure_str or "掀背" in structure_str2:
        structure = 3
    elif "旅行版" in structure_str or "旅行版" in structure_str2:
        structure = 4
    elif "硬顶敞篷车" in structure_str or "硬顶敞篷车" in structure_str2:
        structure = 5
    elif "软顶敞篷车" in structure_str or "软顶敞篷车" in structure_str2:
        structure = 6
    elif "硬顶跑车" in structure_str or "硬顶跑车" in structure_str2:
        structure = 7
    elif "客车" in structure_str or "客车" in structure_str2:
        structure = 8
    elif "货车" in structure_str or "货车" in structure_str2:
        structure = 9
    else:
        structure = 0
    # 得到能源数
    energy_str = config_dict.get("i47")
    if not energy_str:
        energy_str = ""
    if "汽油" in energy_str:
        energy = 1
    elif "柴油" in energy_str:
        energy = 2
    elif "油电混合" in energy_str:
        energy = 3
    elif "纯电动" in energy_str:
        energy = 4
    elif "插电式混合动力" in energy_str:
        energy = 5
    elif "增程式" in energy_str:
        energy = 6
    else:
        energy = 0
    # 得到变速箱
    gbox_str = res.get("i6")
    if not gbox_str:
        gbox_str = ""
    if "手动" in gbox_str:
        gbox = 1
    else:
        gbox = 2
    # 得到天窗
    skylight_str1 = config_dict.get("i106")
    skylight_str2 = config_dict.get("i107")
    if not skylight_str1:
        skylight_str1 = ""
    if not skylight_str2:
        skylight_str2 = ""
    if "●" in skylight_str1 or "●" in skylight_str2:
        skylight = 1
    else:
        skylight = 0
    # 得到电动座椅调节参数
    e_contr_seat_str = config_dict.get("i133")
    if not e_contr_seat_str:
        e_contr_seat_str = ""
    if "●" in e_contr_seat_str:
        e_contr_seat = 1
    else:
        e_contr_seat = 0
    # 得到gps参数
    gps_str = config_dict.get("i145")
    if not gps_str:
        gps_str = ""
    if "●" in gps_str:
        gps = 1
    else:
        gps = 0
    # 得到esp参数
    esp_str = config_dict.get("i96")
    if not esp_str:
        esp_str = ""
    if "●" in esp_str:
        esp = 1
    else:
        esp = 0
    # 得到氙气大灯参数
    hid_str1 = config_dict.get("i157")
    hid_str2 = config_dict.get("i158")
    if not hid_str1:
        hid_str1 = ""
    if not hid_str2:
        hid_str2 = ""
    if "氙气" in hid_str1 or "氙气" in hid_str2:
        hid = 1
    else:
        hid = 0
    # 得到真皮座椅参数
    leather_seat_str = config_dict.get("i128")
    if not leather_seat_str:
        leather_seat_str = ""
    if "真皮" in leather_seat_str:
        leather_seat = 1
    else:
        leather_seat = 0
    # 获取定速巡航的参数
    dlcc_str = config_dict.get("i122")
    if not dlcc_str:
        dlcc_str = ""
    if "●" in dlcc_str:
        dlcc = 1
    else:
        dlcc = 0
    # 获取全自动空调参数
    auto_air_cond_str = config_dict.get("i182")
    if not auto_air_cond_str:
        auto_air_cond_str = ""
    if "自动" in auto_air_cond_str:
        auto_air_cond = 1
    else:
        auto_air_cond = 0
    # 获取倒车影像参数
    revers_img_str = config_dict.get("i124")
    if not revers_img_str:
        revers_img_str = ""
    if "●" in revers_img_str:
        revers_img = 1
    else:
        revers_img = 0
    # 获取无钥匙启动参数
    keyless_go_str = config_dict.get("i90")
    if not keyless_go_str:
        keyless_go_str = ""
    if "●" in keyless_go_str:
        keyless_go = 1
    else:
        keyless_go = 0
    # 获取座椅加热的参数
    seat_heat_str = config_dict.get("i138")
    if not seat_heat_str:
        seat_heat_str = ""
    if "●" in seat_heat_str:
        seat_heat = 1
    else:
        seat_heat = 0
    # 获取自动泊车参数
    auto_park_str = config_dict.get("i98")
    if not auto_park_str:
        auto_park_str = ""
    if "●" in auto_park_str:
        auto_park = 1
    else:
        auto_park = 0
    # 获取进气方式参数
    intake_mode_str = config_dict.get("i33")
    if not intake_mode_str:
        intake_mode_str = ""
    if "自然吸气" in intake_mode_str:
        intake_mode = 1
    elif "涡轮增压" in intake_mode_str:
        intake_mode = 2
    elif "机械增压" in intake_mode_str:
        intake_mode = 3
    else:
        intake_mode = 0
    # 获取驱动方式参数
    drive_mode_str = config_dict.get("i66")
    if not drive_mode_str:
        drive_mode_str = ""
    if "前驱" in drive_mode_str:
        drive_mode = 1
    elif "后驱" in drive_mode_str:
        drive_mode = 2
    elif "四驱" in drive_mode_str:
        drive_mode = 3
    else:
        drive_mode = 0
    # 把数据重新组合成一个对象,返回
    tmp = {}
    tmp['id'] = specs_id
    tmp['brands_name'] = brands_name
    tmp['price'] = price
    tmp['level'] = level
    tmp['displacement'] = displacement
    tmp['seat_num'] = seat_num
    tmp['structure'] = structure
    tmp['energy'] = energy
    tmp['gbox'] = gbox
    tmp['skylight'] = skylight
    tmp['e_contr_seat'] = e_contr_seat
    tmp['gps'] = gps
    tmp['esp'] = esp
    tmp['hid'] = hid
    tmp['leather_seat'] = leather_seat
    tmp['dlcc'] = dlcc
    tmp['auto_air_cond'] = auto_air_cond
    tmp['revers_img'] = revers_img
    tmp['keyless_go'] = keyless_go
    tmp['seat_heat'] = seat_heat
    tmp['auto_park'] = auto_park
    tmp["intake_mode"] = intake_mode
    tmp['drive_mode'] = drive_mode
    return tmp


# 根据字典,执行写入文件的操作
def write_to_sql_file(one_dict):


    pass


if __name__ == '__main__':
    specs_id_list = get_all_cheyixiao_specs_id()
    for one in specs_id_list:
        info_dict = read_info_write_file(one)
        write_to_sql_file(info_dict)