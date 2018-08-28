# 得到所有的日志文件
def read_logs_file(file_path):
    with open(file_path, 'r') as f:
        res_str = f.read()

    logs_list = res_str.split("\n")
    return logs_list


# 解析一行的日志
def parse_one_log(one_log):
    tmp = {}
    columns_list = one_log.split(" ")
    # 获取ip
    tmp['ip'] = columns_list[0]
    # 获取请求方式
    tmp['method'] = str(columns_list[5]).strip("\"")
    # 获取请求状态码
    tmp['status'] = columns_list[8]
    # 获取请求方法
    tmp["url"] = columns_list[6]
    # 获取请求的时间
    time_str = columns_list[3].strip("[")
    time_str_list = time_str.split(":")
    log_time = time_str_list[1] + ":" + time_str_list[2] + ":" + time_str_list[3]
    month_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
                  "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                  "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    data_str_list = str(time_str_list[0]).split("/")
    log_year = data_str_list[2]
    log_month = month_dict.get(data_str_list[1])
    log_day = data_str_list[0]
    log_data_time = log_year + "-" + log_month + "-" + log_day + " " + log_time
    tmp["time"] = log_data_time
    # 开始获取用户客户端
    tmp_list = one_log.split("\"")
    tmp['client'] = tmp_list[5]
    return tmp


if __name__ == '__main__':
    file_path = "one_access.log"
    logs_list = read_logs_file(file_path)
    for one_log in logs_list:
        info = parse_one_log(one_log)
        print(info)