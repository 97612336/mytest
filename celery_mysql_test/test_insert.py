from tasks import insert_data

for i in range(999999 * 999999):
    print(i)
    insert_data.delay('张三' + str(i))

# insert_data.delay('张三' + str(1))
