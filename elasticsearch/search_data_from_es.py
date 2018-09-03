from elasticsearch_dsl import connections, Search

if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])
    s = Search(index='test').query('match', title='标题')[0:3]
    response = s.execute()
    i=1
    for one in response:
        print(one)
        print(one.title)
        print('++++++++++++++++++++++++')
        i=i+1
    print(i)