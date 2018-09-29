one_dict_list = [{"type": 1, "content": 123123}, {"type": 0, "content": 1239993}]

for one_dict in one_dict_list:
    if one_dict.get("type") == 1:
        one_dict["content"] = 111111
        print(one_dict)

print(one_dict_list)
