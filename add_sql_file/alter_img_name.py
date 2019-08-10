from add_sql_file.two_file import read_excel

file_path = "/home/wangkun/Desktop/图片1/"

list1 = read_excel()
dict1 = {}
for one in list1:
    subject_id = one.get("column6")
    print(subject_id)
    subject_name = one.get("column7")
    print(subject_name)
    dict1[subject_id] = subject_name
print(dict1)
