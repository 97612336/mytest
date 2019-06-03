'''

字符A-Z可以编码为1-26。"A"->"1", "Z"->"26"
现在输入一个数字序列，计算有多少种方式可以解码成字符A-Z组成的序列。

例如：

输入：19
输出：2

输入：268
输出：2

输入：219
输出：3


'''


def how_many_ways(some_num):
    new_num_str = some_num.lstrip('0')
    length = len(new_num_str)
    if length == 0:
        return 0
    num_len_list = [x for x in range(length + 1)]
    num_len_list[0] = 1
    print(num_len_list)
    for i in range(length + 1):
        if i == 0:
            continue
        if some_num[i - 1] == '0':
            num_len_list[i] = 1
        else:
            num_len_list[i] = num_len_list[i - 1]
        if (i > 1 and int(some_num[i - 1]) <= 6 and int(some_num[i - 2]) == 2) or (
                i > 1 and int(some_num[i - 2]) == 1):
            num_len_list[i] += num_len_list[i - 2]
    print(num_len_list)
    return num_len_list[length]


some_num = '219'
res = how_many_ways(some_num)
print(res)
