def write_new_sql(one_line):
    if 'utf8' in one_line:
        one_line = str(one_line).replace('utf8', 'utf8mb4')
    new_sql_path = '/home/wangkun/itfin_new.sql'
    with open(new_sql_path, 'a+') as f:
        f.write(one_line)


sql_path = '/home/wangkun/itfin.sql'

i = 1
with open(sql_path, 'r') as f:
    one_line = f.readline()
    while one_line:
        print(i)
        write_new_sql(one_line)
        i = i + 1
        one_line = f.readline()
